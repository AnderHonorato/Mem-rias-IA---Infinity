"""Registro mínimo de decisões operacionais, com cadeia HMAC e sem dados brutos.

A chave deve vir de um gerenciador de segredos do HOST; nunca commitar.
O hash protege integridade, mas não substitui controles de acesso ou SIEM.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path


class ErroAuditoria(ValueError):
    pass


class RegistroAuditoria:
    def __init__(self, caminho: str | Path, *, chave: bytes) -> None:
        if not isinstance(chave, bytes) or len(chave) < 32:
            raise ErroAuditoria("Chave HMAC inválida ou curta")
        self.caminho = Path(caminho).resolve()
        self.caminho.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.chave = chave
        self.lock = threading.Lock()
        self._anterior = "0" * 64
        if self.caminho.exists():
            self._anterior = self.verificar()

    def registrar(self, *, tarefa: str, agente: str, estado: str, revisores: int) -> str:
        for campo, valor in {"tarefa": tarefa, "agente": agente, "estado": estado}.items():
            if not isinstance(valor, str) or not 1 <= len(valor) <= 100 or not all(c.isalnum() or c in "-_" for c in valor):
                raise ErroAuditoria(f"{campo} contém caracteres inválidos")
        if not isinstance(revisores, int) or not 0 <= revisores <= 20:
            raise ErroAuditoria("Quantidade de revisores inválida")
        with self.lock:
            evento = {"tarefa": tarefa, "agente": agente, "estado": estado,
                      "revisores": revisores, "em_utc": datetime.now(timezone.utc).isoformat(),
                      "anterior": self._anterior}
            dados = json.dumps(evento, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            assinatura = hmac.new(self.chave, dados.encode("utf-8"), hashlib.sha256).hexdigest()
            evento["assinatura"] = assinatura
            linha = json.dumps(evento, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
            fd = os.open(self.caminho, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
            try:
                if os.name == "posix":
                    os.fchmod(fd, 0o600)
                with os.fdopen(fd, "a", encoding="utf-8") as arquivo:
                    arquivo.write(linha)
                    arquivo.flush()
                    os.fsync(arquivo.fileno())
            except BaseException:
                # fdopen é dono do descriptor após ter sido chamado; não reabrir.
                raise
            self._anterior = assinatura
            return assinatura

    def verificar(self) -> str:
        anterior = "0" * 64
        if not self.caminho.exists():
            return anterior
        with self.caminho.open("r", encoding="utf-8") as arquivo:
            for numero, linha in enumerate(arquivo, start=1):
                try:
                    registro = json.loads(linha)
                    assinatura = registro.pop("assinatura")
                    if registro.get("anterior") != anterior:
                        raise ErroAuditoria("Cadeia de auditoria alterada")
                    dados = json.dumps(registro, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                    esperado = hmac.new(self.chave, dados.encode(), hashlib.sha256).hexdigest()
                    if not hmac.compare_digest(esperado, assinatura):
                        raise ErroAuditoria("Assinatura de auditoria inválida")
                    anterior = assinatura
                except (ValueError, KeyError, TypeError) as exc:
                    raise ErroAuditoria(f"Auditoria inválida na linha {numero}") from exc
        return anterior
