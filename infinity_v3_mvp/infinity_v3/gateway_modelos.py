"""Adaptadores reais HTTP para LLMs, sempre opt-in e sem secrets em código.

A classe não é uma integração dentro do ChatGPT; é um cliente Python privado.
Nenhuma requisição é feita até o host criar uma política explícita de permissão.
"""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from threading import Lock
from typing import Any, Callable, Literal

Provedor = Literal["openai", "anthropic", "ollama"]
Classificacao = Literal["publica", "interna", "sensivel"]

_URLS = {
    "openai": "https://api.openai.com/v1/responses",
    "anthropic": "https://api.anthropic.com/v1/messages",
    "ollama": "http://127.0.0.1:11434/api/chat",
}
_CREDENCIAIS = {"openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY"}
_ID_MODELO = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_.:/-]{0,110}$")
_LIMITE_HTTP = 2 * 1024 * 1024


class ErroGateway(RuntimeError):
    """Falha sem vazamento de prompt, cabeçalhos ou resposta da API."""


class ErroPermissao(ErroGateway):
    pass


@dataclass(frozen=True)
class ConfiguracaoModelo:
    provedor: Provedor
    modelo: str
    preco_entrada_mil: float = 0.0
    preco_saida_mil: float = 0.0

    def __post_init__(self) -> None:
        if self.provedor not in _URLS or not isinstance(self.modelo, str) or not _ID_MODELO.fullmatch(self.modelo) or "://" in self.modelo:
            raise ValueError("Provedor ou identificador de modelo inválido")
        if not all(isinstance(p, (int, float)) and 0 <= p < 10000 for p in
                   (self.preco_entrada_mil, self.preco_saida_mil)):
            raise ValueError("Estimativas de preço inválidas")


@dataclass(frozen=True)
class PermissaoChamada:
    rede_habilitada: bool = False
    nuvem_habilitada: bool = False
    chamadas_pagas_habilitadas: bool = False
    dados_internos_habilitados: bool = False
    teto_por_chamada: float = 0.0
    teto_por_sessao: float = 0.0
    limite_chamadas: int = 0

    def __post_init__(self) -> None:
        if self.teto_por_chamada < 0 or self.teto_por_sessao < 0 or self.limite_chamadas < 0:
            raise ValueError("Limites não podem ser negativos")


@dataclass(frozen=True)
class SolicitacaoModelo:
    instrucao: str
    entrada: str
    classificacao: Classificacao = "publica"
    max_tokens_saida: int = 512

    def __post_init__(self) -> None:
        if (not isinstance(self.instrucao, str) or not self.instrucao.strip() or
                not isinstance(self.entrada, str) or not self.entrada.strip() or
                len(self.instrucao) > 8000 or len(self.entrada) > 20000):
            raise ValueError("Solicitação ausente ou muito longa")
        if self.classificacao not in {"publica", "interna", "sensivel"}:
            raise ValueError("Classificação desconhecida")
        if not isinstance(self.max_tokens_saida, int) or not 32 <= self.max_tokens_saida <= 4096:
            raise ValueError("Limite de geração inválido")


@dataclass(frozen=True)
class RespostaModelo:
    texto: str
    provedor: Provedor
    modelo: str
    tokens_entrada: int | None
    tokens_saida: int | None
    custo_reservado: float


# Cada transporte recebe URL, headers, body e timeout. Injeção só para testes/host confiável.
Transporte = Callable[[str, dict[str, str], dict[str, Any], int], dict[str, Any]]


class _SemRedirecionamentos(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req: Any, fp: Any, code: Any, msg: Any, headers: Any, newurl: Any) -> None:
        raise ErroGateway("Redirecionamento de rede recusado")


def transporte_http(url: str, headers: dict[str, str], corpo: dict[str, Any], timeout: int) -> dict[str, Any]:
    """URL fixa por provedor e sem redirects: mitiga SSRF e vazamentos por redirecionamento."""
    if url not in _URLS.values():
        raise ErroGateway("Destino de rede não autorizado")
    pedido = urllib.request.Request(url, data=json.dumps(corpo).encode("utf-8"),
                                     headers=headers, method="POST")
    cliente = urllib.request.build_opener(urllib.request.ProxyHandler({}), _SemRedirecionamentos())
    try:
        with cliente.open(pedido, timeout=timeout) as resposta:
            dados = resposta.read(_LIMITE_HTTP + 1)
            if len(dados) > _LIMITE_HTTP:
                raise ErroGateway("Resposta excede o tamanho permitido")
            resultado = json.loads(dados)
            if not isinstance(resultado, dict):
                raise ErroGateway("Resposta inválida do provedor")
            return resultado
    except ErroGateway:
        raise
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError, OSError) as e:
        # Nunca retornar corpo de erro, URL de usuário, stack nem dados de autenticação.
        raise ErroGateway(f"Falha de transporte: {type(e).__name__}") from None


def _extrair_texto(provedor: Provedor, resposta: dict[str, Any]) -> tuple[str, int | None, int | None]:
    try:
        if provedor == "openai":
            partes = [item["text"] for saida in resposta["output"] if saida.get("type") == "message"
                      for item in saida.get("content", []) if item.get("type") == "output_text"]
            uso = resposta.get("usage") or {}
            entrada, saida = uso.get("input_tokens"), uso.get("output_tokens")
        elif provedor == "anthropic":
            partes = [item["text"] for item in resposta["content"] if item.get("type") == "text"]
            uso = resposta.get("usage") or {}
            entrada, saida = uso.get("input_tokens"), uso.get("output_tokens")
        else:
            partes = [resposta["message"]["content"]]
            entrada, saida = resposta.get("prompt_eval_count"), resposta.get("eval_count")
        texto = "\n".join(partes).strip()
        if not texto or len(texto) > 100000:
            raise ValueError("Conteúdo vazio ou excessivo")
        for n in (entrada, saida):
            if n is not None and (not isinstance(n, int) or isinstance(n, bool) or n < 0):
                raise ValueError("Uso inválido")
        return texto, entrada, saida
    except (KeyError, TypeError, ValueError, AttributeError) as exc:
        raise ErroGateway("Formato da resposta do modelo inválido") from None


class GatewayModelos:
    """Sem persistência de credenciais. Cotas são por instância, não por dia/conta.

    Sem autorização explícita, a classe sequer invoca o transporte injetado.
    Reservas de preço são conservadoras porém NÃO asseguram teto de cobrança real.
    """

    def __init__(self, *, transporte: Transporte = transporte_http, timeout: int = 25) -> None:
        if not isinstance(timeout, int) or not 1 <= timeout <= 60:
            raise ValueError("Timeout fora do intervalo")
        self._transporte = transporte
        self._timeout = timeout
        self._chamadas = 0
        self._reservado = 0.0
        self._trava = Lock()

    def responder(self, modelo: ConfiguracaoModelo, pedido: SolicitacaoModelo,
                  permissao: PermissaoChamada) -> RespostaModelo:
        nuvem = modelo.provedor != "ollama"
        if not permissao.rede_habilitada:
            raise ErroPermissao("Rede desabilitada por padrão")
        if nuvem and not permissao.nuvem_habilitada:
            raise ErroPermissao("Envio para nuvem não autorizado")
        if nuvem and not permissao.chamadas_pagas_habilitadas:
            raise ErroPermissao("API paga não autorizada")
        if pedido.classificacao == "sensivel" and nuvem:
            raise ErroPermissao("Conteúdo sensível não pode sair do dispositivo")
        if pedido.classificacao == "interna" and nuvem and not permissao.dados_internos_habilitados:
            raise ErroPermissao("Conteúdo interno não autorizado para nuvem")
        if nuvem and modelo.preco_entrada_mil + modelo.preco_saida_mil <= 0:
            raise ErroPermissao("Preço não configurado; chamada paga bloqueada")
        # Reserva aproximada: tokenização real e política de cobrança variam por modelo.
        entrada_max = (len(pedido.entrada) + len(pedido.instrucao) + 2) // 3
        reserva = (entrada_max * modelo.preco_entrada_mil + pedido.max_tokens_saida * modelo.preco_saida_mil) / 1000
        reserva = round(reserva, 9)
        if nuvem and (reserva > permissao.teto_por_chamada or reserva > permissao.teto_por_sessao):
            raise ErroPermissao("Estimativa excede o orçamento autorizado")
        token = None
        if nuvem:
            token = os.environ.get(_CREDENCIAIS[modelo.provedor], "").strip()
            if not token or any(c.isspace() for c in token):
                raise ErroPermissao("Credencial de API não configurada")
        with self._trava:
            if self._chamadas >= permissao.limite_chamadas:
                raise ErroPermissao("Limite de chamadas da sessão atingido")
            if nuvem and self._reservado + reserva > permissao.teto_por_sessao:
                raise ErroPermissao("Orçamento da sessão atingido")
            self._chamadas += 1
            if nuvem:
                self._reservado += reserva
        cabecalhos = {"Content-Type": "application/json", "Accept": "application/json"}
        if modelo.provedor == "openai":
            cabecalhos["Authorization"] = "Bearer " + token
            corpo = {"model": modelo.modelo, "instructions": pedido.instrucao,
                     "input": pedido.entrada, "max_output_tokens": pedido.max_tokens_saida,
                     "store": False, "stream": False}
        elif modelo.provedor == "anthropic":
            cabecalhos["Authorization"] = "Bearer " + token
            cabecalhos["anthropic-version"] = "2026-10-21"
            corpo = {"model": modelo.modelo, "max_tokens": pedido.max_tokens_saida,
                     "system": pedido.instrucao,
                     "messages": [{"role": "user", "content": pedido.entrada}], "stream": False}
        else:
            corpo = {"model": modelo.modelo, "messages": [
                {"role": "system", "content": pedido.instrucao},
                {"role": "user", "content": pedido.entrada}],
                     "options": {"num_predict": pedido.max_tokens_saida}, "stream": False}
        try:
            retorno = self._transporte(_URLS[modelo.provedor], cabecalhos, corpo, self._timeout)
            if not isinstance(retorno, dict):
                raise ErroGateway("Resposta do transporte inválida")
            texto, entrada, saida = _extrair_texto(modelo.provedor, retorno)
            return RespostaModelo(texto, modelo.provedor, modelo.modelo, entrada, saida, reserva)
        except ErroGateway:
            raise
        except Exception as exc:
            raise ErroGateway(f"Falha no gateway: {type(exc).__name__}") from None

    @property
    def resumo_contagem(self) -> tuple[int, float]:
        """Somente contadores, sem prompts nem credenciais."""
        with self._trava:
            return self._chamadas, round(self._reservado, 9)
