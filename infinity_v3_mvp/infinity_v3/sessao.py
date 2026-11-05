"""Fachada de escopos e privilégios para um processo de confiança.

NÃO é autenticação de rede: somente código servidor autenticado pode instanciar
esta classe com identidade e escopos reais. Nunca passe um objeto motor cru a
controladores web ou LLMs.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .motor import MotorMemoria, ErroDeAcesso


@dataclass(frozen=True)
class SessaoMemoria:
    motor: MotorMemoria
    usuario: str
    escopos: frozenset[str]
    pode_escrever: bool = False
    pode_excluir: bool = False

    def _exigir_escopo(self, escopo: str) -> None:
        if escopo not in self.escopos:
            raise ErroDeAcesso("Escopo indisponível")

    def _exigir_registro(self, memoria_id: str) -> None:
        registro = self.motor._registro(memoria_id, self.usuario)
        self._exigir_escopo(str(registro["escopo"]))

    def buscar(self, *, consulta: str, escopos: list[str] | None = None, limite: int = 10) -> list[dict[str, Any]]:
        selecionar = sorted(self.escopos) if escopos is None else escopos
        for escopo in selecionar:
            self._exigir_escopo(escopo)
        if not selecionar:
            return []
        return self.motor.buscar(usuario=self.usuario, escopos=selecionar, consulta=consulta, limite=limite)

    def registrar(self, *, escopo: str, titulo: str, conteudo: str, origem: str, **opcoes: Any) -> str:
        if not self.pode_escrever:
            raise ErroDeAcesso("Escrita indisponível")
        self._exigir_escopo(escopo)
        opcoes.pop("usuario", None)
        opcoes.pop("aprovado", None)  # força revisão antes da publicação
        return self.motor.registrar(usuario=self.usuario, escopo=escopo, titulo=titulo,
                                     conteudo=conteudo, origem=origem, aprovado=False, **opcoes)

    def aprovar(self, *, memoria_id: str) -> None:
        if not self.pode_escrever:
            raise ErroDeAcesso("Escrita indisponível")
        self._exigir_registro(memoria_id)
        self.motor.aprovar(usuario=self.usuario, memoria_id=memoria_id)

    def corrigir(self, *, memoria_id: str, conteudo_corrigido: str, justificativa: str) -> str:
        if not self.pode_escrever:
            raise ErroDeAcesso("Escrita indisponível")
        self._exigir_registro(memoria_id)
        return self.motor.corrigir(usuario=self.usuario, memoria_id=memoria_id,
            conteudo_corrigido=conteudo_corrigido, justificativa=justificativa)

    def excluir(self, *, memoria_id: str) -> None:
        if not self.pode_excluir:
            raise ErroDeAcesso("Exclusão indisponível")
        self._exigir_registro(memoria_id)
        self.motor.excluir_definitivamente(usuario=self.usuario, memoria_id=memoria_id)

    def excluir_meus_dados(self, *, confirmacao: str) -> int:
        if not self.pode_excluir:
            raise ErroDeAcesso("Exclusão indisponível")
        # Restringir a exclusão aos escopos autorizados, sem apagar outros escopos.
        if not self.escopos:
            raise ErroDeAcesso("Escopos indisponíveis")
        if confirmacao != "EXCLUIR TODOS OS MEUS DADOS":
            raise ErroDeAcesso("Confirmação ausente")
        total = 0
        ids = self.motor.conexao.execute(
            f"SELECT id FROM memorias WHERE usuario=? AND escopo IN ({','.join('?' for _ in self.escopos)})",
            [self.usuario, *sorted(self.escopos)]).fetchall()
        for registro in ids:
            self.excluir(memoria_id=str(registro[0]))
            total += 1
        return total
