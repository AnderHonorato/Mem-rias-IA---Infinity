"""Liga o roteador determinístico ao gateway HTTP; não agenda chamadas sozinho."""
from __future__ import annotations

from dataclasses import dataclass

from .gateway_modelos import (
    ConfiguracaoModelo, GatewayModelos, PermissaoChamada,
    RespostaModelo, SolicitacaoModelo,
)
from .roteador import Modelo, Politica, Roteador


@dataclass(frozen=True)
class RegistroModelo:
    catalogo: Modelo
    conexao: ConfiguracaoModelo

    def __post_init__(self) -> None:
        if self.catalogo.local != (self.conexao.provedor == "ollama"):
            raise ValueError("Localidade declarada não corresponde ao destino")
        if self.catalogo.nome != self.conexao.modelo:
            raise ValueError("Nome de catálogo difere do modelo configurado")
        if self.catalogo.custo_estimado_por_mil_tokens < 0:
            raise ValueError("Preço do catálogo é inválido")


@dataclass(frozen=True)
class DecisaoDeRoteamento:
    modelo: str
    provedor: str
    justificativa: str
    resposta: RespostaModelo


class RoteamentoExecutavel:
    def __init__(self, gateway: GatewayModelos, registros: list[RegistroModelo]) -> None:
        if not registros:
            raise ValueError("Informe ao menos um modelo")
        self.gateway = gateway
        self.registros = {r.catalogo.nome: r for r in registros}
        if len(self.registros) != len(registros):
            raise ValueError("Modelos duplicados")
        self.roteador = Roteador([r.catalogo for r in registros])

    def responder(self, solicitacao: SolicitacaoModelo, *, politica_roteamento: Politica,
                  permissao_rede: PermissaoChamada, preferido: str | None = None) -> DecisaoDeRoteamento:
        # O roteador escolhe por classe, mas o gateway revalida custos/rede/privacidade.
        escolha = self.roteador.escolher(
            solicitacao.entrada, politica_roteamento,
            preferido=preferido, sigiloso=(solicitacao.classificacao == "sensivel"))
        registro = self.registros[escolha.modelo]
        resposta = self.gateway.responder(registro.conexao, solicitacao, permissao_rede)
        return DecisaoDeRoteamento(
            modelo=escolha.modelo, provedor=registro.conexao.provedor,
            justificativa=escolha.motivo, resposta=resposta)
