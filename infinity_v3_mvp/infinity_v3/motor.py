"""Memória local demonstrativa: SQLite + FTS5, consentimento e isolamento.

Este módulo NÃO sincroniza dados privados ao GitHub ou a outras IAs.
O banco deve ficar em diretório privado, fora de qualquer repositório público.
"""
from __future__ import annotations

import hashlib
import os
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .seguranca import exigir_sem_segredos


class ErroDeValidacao(ValueError):
    """Entrada inválida ou operação não permitida."""


class ErroDeAcesso(PermissionError):
    """Registro ausente ou não autorizado para o solicitante."""


def agora_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def texto_valido(valor: str, campo: str, limite: int) -> str:
    if not isinstance(valor, str) or not valor.strip() or len(valor) > limite:
        raise ErroDeValidacao(f"{campo} deve conter de 1 a {limite} caracteres")
    return valor.strip()


def resumo_digital(*partes: str) -> str:
    normalizadas = [" ".join(parte.casefold().split()) for parte in partes]
    return hashlib.sha256("\x1f".join(normalizadas).encode("utf-8")).hexdigest()


class MotorMemoria:
    """Protótipo de armazenamento isolado com índice FTS5 local."""

    def __init__(self, caminho_banco: str | Path) -> None:
        if str(caminho_banco) == ":memory:":
            raise ErroDeValidacao("Use um banco temporário em arquivo para testes")
        self.caminho = Path(caminho_banco).expanduser().resolve()
        self.caminho.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.conexao = sqlite3.connect(str(self.caminho), isolation_level=None)
        self.conexao.row_factory = sqlite3.Row
        self.conexao.execute("PRAGMA foreign_keys = ON")
        self.conexao.execute("PRAGMA secure_delete = ON")
        self.conexao.execute("PRAGMA busy_timeout = 5000")
        self.conexao.execute("PRAGMA journal_mode = WAL")
        self._inicializar()
        if os.name == "posix":
            self.caminho.chmod(0o600)

    def __enter__(self) -> MotorMemoria:
        return self

    def __exit__(self, *_: object) -> None:
        self.fechar()

    def fechar(self) -> None:
        self.conexao.close()

    def _inicializar(self) -> None:
        self.conexao.executescript("""
            CREATE TABLE IF NOT EXISTS memorias (
                id TEXT PRIMARY KEY,
                usuario TEXT NOT NULL,
                escopo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                titulo TEXT NOT NULL,
                conteudo TEXT NOT NULL,
                origem TEXT NOT NULL,
                confianca TEXT NOT NULL,
                sensibilidade TEXT NOT NULL,
                status TEXT NOT NULL CHECK (status IN ('revisao','ativo','substituido','arquivado')),
                impressao_digital TEXT NOT NULL,
                substitui TEXT REFERENCES memorias(id),
                criado_em TEXT NOT NULL,
                atualizado_em TEXT NOT NULL,
                valido_ate TEXT
            );
            CREATE UNIQUE INDEX IF NOT EXISTS idx_memoria_unica
                ON memorias(usuario, escopo, impressao_digital)
                WHERE status IN ('revisao','ativo');
            CREATE INDEX IF NOT EXISTS idx_memorias_acesso
                ON memorias(usuario, escopo, status, valido_ate);
            CREATE TABLE IF NOT EXISTS eventos (
                id TEXT PRIMARY KEY,
                memoria_id TEXT NOT NULL REFERENCES memorias(id),
                usuario TEXT NOT NULL,
                acao TEXT NOT NULL,
                ocorreu_em TEXT NOT NULL,
                justificativa_hash TEXT
            );
            CREATE VIRTUAL TABLE IF NOT EXISTS indice_memorias
                USING fts5(id UNINDEXED, titulo, conteudo, tokenize='unicode61 remove_diacritics 2');
            CREATE TRIGGER IF NOT EXISTS memoria_inserida AFTER INSERT ON memorias BEGIN
                INSERT INTO indice_memorias(id,titulo,conteudo)
                VALUES (new.id,new.titulo,new.conteudo);
            END;
            CREATE TRIGGER IF NOT EXISTS memoria_alterada AFTER UPDATE ON memorias BEGIN
                DELETE FROM indice_memorias WHERE id = old.id;
                INSERT INTO indice_memorias(id,titulo,conteudo)
                VALUES (new.id,new.titulo,new.conteudo);
            END;
            CREATE TRIGGER IF NOT EXISTS memoria_excluida AFTER DELETE ON memorias BEGIN
                DELETE FROM indice_memorias WHERE id = old.id;
            END;
        """)
        # Migração aditiva para arquivos de protótipos já existentes.
        colunas = {r[1] for r in self.conexao.execute("PRAGMA table_info(eventos)")}
        if "justificativa_hash" not in colunas:
            self.conexao.execute("ALTER TABLE eventos ADD COLUMN justificativa_hash TEXT")

    def _evento(self, memoria_id: str, usuario: str, acao: str, justificativa_hash: str | None = None) -> None:
        # Não registrar o conteúdo das memórias em logs.
        self.conexao.execute(
            "INSERT INTO eventos (id, memoria_id, usuario, acao, ocorreu_em, justificativa_hash) VALUES (?,?,?,?,?,?)",
            (str(uuid.uuid4()), memoria_id, usuario, acao, agora_utc(), justificativa_hash),
        )

    def _registro(self, id: str, usuario: str) -> sqlite3.Row:
        r = self.conexao.execute(
            "SELECT * FROM memorias WHERE id=? AND usuario=?", (id, usuario)
        ).fetchone()
        if r is None:
            raise ErroDeAcesso("Memória inexistente ou sem autorização")
        return r

    def registrar(
        self, *, usuario: str, escopo: str, titulo: str, conteudo: str,
        origem: str, categoria: str = "fato", confianca: str = "observada",
        sensibilidade: str = "interna", aprovado: bool = False,
        valido_ate: str | None = None,
    ) -> str:
        usuario = texto_valido(usuario, "usuario", 128)
        escopo = texto_valido(escopo, "escopo", 160)
        titulo = texto_valido(titulo, "titulo", 300)
        conteudo = texto_valido(conteudo, "conteudo", 100000)
        origem = texto_valido(origem, "origem", 1000)
        try:
            exigir_sem_segredos(titulo, conteudo, origem)
        except ValueError as exc:
            raise ErroDeValidacao(str(exc)) from exc
        categoria = texto_valido(categoria, "categoria", 64)
        if sensibilidade not in {"publica", "interna", "pessoal"}:
            raise ErroDeValidacao("Segredos e dados altamente sensíveis não são aceitos")
        if confianca not in {"confirmada", "observada", "referenciada", "inferida", "incerta"}:
            raise ErroDeValidacao("Confiança inválida")
        if valido_ate is not None:
            try:
                vencimento = datetime.fromisoformat(valido_ate)
                if vencimento.tzinfo is None:
                    raise ValueError("data sem fuso")
            except ValueError as e:
                raise ErroDeValidacao("valido_ate precisa de ISO8601 com fuso") from e
            valido_ate = vencimento.astimezone(timezone.utc).isoformat()
        digital = resumo_digital(titulo, conteudo, categoria)
        existente = self.conexao.execute(
            """SELECT id FROM memorias WHERE usuario=? AND escopo=? AND impressao_digital=?
                AND status IN ('revisao','ativo')""", (usuario, escopo, digital)
        ).fetchone()
        if existente:
            return str(existente[0])
        id_novo, instante = str(uuid.uuid4()), agora_utc()
        status = "ativo" if aprovado else "revisao"
        with self.conexao:
            self.conexao.execute("""
                INSERT INTO memorias
                (id, usuario, escopo, categoria, titulo, conteudo, origem,
                 confianca, sensibilidade, status, impressao_digital,
                 substitui, criado_em, atualizado_em, valido_ate)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (id_novo, usuario, escopo, categoria, titulo, conteudo, origem,
                  confianca, sensibilidade, status, digital, None, instante, instante,
                  valido_ate))
            self._evento(id_novo, usuario, "registrada_ativa" if aprovado else "candidata")
        return id_novo

    def aprovar(self, *, usuario: str, memoria_id: str) -> None:
        usuario = texto_valido(usuario, "usuario", 128)
        registro = self._registro(memoria_id, usuario)
        if registro["status"] != "revisao":
            raise ErroDeValidacao("Somente candidata em revisão pode ser aprovada")
        with self.conexao:
            self.conexao.execute(
                "UPDATE memorias SET status='ativo', atualizado_em=? WHERE id=?",
                (agora_utc(), memoria_id),
            )
            self._evento(memoria_id, usuario, "aprovada")

    def corrigir(self, *, usuario: str, memoria_id: str, conteudo_corrigido: str,
                justificativa: str) -> str:
        usuario = texto_valido(usuario, "usuario", 128)
        justificativa = texto_valido(justificativa, "justificativa", 1000)
        conteudo_corrigido = texto_valido(conteudo_corrigido, "conteudo_corrigido", 100000)
        try:
            exigir_sem_segredos(conteudo_corrigido, justificativa)
        except ValueError as exc:
            raise ErroDeValidacao(str(exc)) from exc
        antigo = self._registro(memoria_id, usuario)
        if antigo["status"] != "ativo":
            raise ErroDeValidacao("Apenas memória ativa pode ser corrigida")
        if conteudo_corrigido == antigo["conteudo"]:
            return memoria_id
        novo_id, instante = str(uuid.uuid4()), agora_utc()
        digital = resumo_digital(antigo["titulo"], conteudo_corrigido, antigo["categoria"])
        existe = self.conexao.execute(
            """SELECT id FROM memorias WHERE usuario=? AND escopo=?
                AND impressao_digital=? AND status IN ('ativo','revisao')""",
            (usuario, antigo["escopo"], digital),
        ).fetchone()
        if existe:
            raise ErroDeValidacao("A correção já existe como memória separada")
        with self.conexao:
            self.conexao.execute(
                "UPDATE memorias SET status='substituido', atualizado_em=? WHERE id=?",
                (instante, memoria_id),
            )
            self.conexao.execute("""
                INSERT INTO memorias
                (id, usuario, escopo, categoria, titulo, conteudo, origem, confianca,
                 sensibilidade, status, impressao_digital, substitui,
                 criado_em, atualizado_em, valido_ate)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (novo_id, usuario, antigo["escopo"], antigo["categoria"],
                  antigo["titulo"], conteudo_corrigido, antigo["origem"],
                  "confirmada", antigo["sensibilidade"], "ativo", digital,
                  memoria_id, instante, instante, antigo["valido_ate"]))
            self._evento(memoria_id, usuario, "substituida")
            # A justificativa é auditável por hash, sem persistir dados sensíveis em logs.
            self._evento(novo_id, usuario, "correcao_confirmada", resumo_digital(justificativa))
        return novo_id

    def arquivar(self, *, usuario: str, memoria_id: str) -> None:
        usuario = texto_valido(usuario, "usuario", 128)
        memoria = self._registro(memoria_id, usuario)
        if memoria["status"] == "arquivado":
            return
        with self.conexao:
            self.conexao.execute(
                "UPDATE memorias SET status='arquivado', atualizado_em=? WHERE id=?",
                (agora_utc(), memoria_id),
            )
            self._evento(memoria_id, usuario, "arquivada")

    def buscar(self, *, usuario: str, escopos: list[str], consulta: str,
               limite: int = 10) -> list[dict[str, Any]]:
        usuario = texto_valido(usuario, "usuario", 128)
        if not isinstance(escopos, list) or not 1 <= len(escopos) <= 30 or any(not isinstance(e, str) or not e.strip() or len(e) > 160 for e in escopos):
            raise ErroDeValidacao("Informe de 1 a 30 escopos válidos")
        if not isinstance(limite, int) or not 1 <= limite <= 50:
            raise ErroDeValidacao("limite deve ser inteiro entre 1 e 50")
        if not isinstance(consulta, str) or len(consulta) > 2000:
            raise ErroDeValidacao("consulta inválida")
        # Termos sempre protegidos por aspas: sintaxe FTS do usuário não vira comando.
        palavras = re.findall(r"\w+", consulta, re.UNICODE)[:30]
        if not palavras:
            return []
        expressao = " OR ".join(f'"{p}"' for p in palavras)
        escopos_limpos = sorted(set(escopos))
        marcadores = ",".join("?" for _ in escopos_limpos)
        consulta_sql = f"""
            SELECT m.id, m.titulo, m.conteudo, m.escopo, m.categoria,
                   m.confianca, m.origem, m.criado_em, m.substitui,
                   bm25(indice_memorias) AS pontuacao
            FROM indice_memorias
            JOIN memorias m ON m.id = indice_memorias.id
            WHERE indice_memorias MATCH ?
              AND m.usuario = ? AND m.escopo IN ({marcadores})
              AND m.status = 'ativo'
              AND (m.valido_ate IS NULL OR m.valido_ate > ?)
            ORDER BY pontuacao ASC, m.atualizado_em DESC
            LIMIT ?
        """
        linhas = self.conexao.execute(
            consulta_sql, [expressao, usuario, *escopos_limpos, agora_utc(), limite]
        ).fetchall()
        return [dict(linha) for linha in linhas]

    def contar_eventos(self, *, usuario: str) -> int:
        usuario = texto_valido(usuario, "usuario", 128)
        return int(self.conexao.execute(
            "SELECT COUNT(*) FROM eventos WHERE usuario=?", (usuario,)
        ).fetchone()[0])

    def excluir_definitivamente(self, *, usuario: str, memoria_id: str) -> None:
        """Remove registro local e auditoria; não apaga backups ou blocos SSD.

        O chamador deve estar autenticado e autorizado. Não oferece garantia
        forense de eliminação completa (WAL, backups e cópias externas).
        """
        usuario = texto_valido(usuario, "usuario", 128)
        self._registro(memoria_id, usuario)
        with self.conexao:
            self.conexao.execute("UPDATE memorias SET substitui=NULL WHERE substitui=? AND usuario=?", (memoria_id, usuario))
            self.conexao.execute("DELETE FROM eventos WHERE memoria_id=? AND usuario=?", (memoria_id, usuario))
            self.conexao.execute("DELETE FROM memorias WHERE id=? AND usuario=?", (memoria_id, usuario))
        self.conexao.execute("PRAGMA wal_checkpoint(TRUNCATE)")

    def excluir_tudo_do_usuario(self, *, usuario: str, confirmacao: str) -> int:
        """Apaga todas as memórias locais do usuário e seus eventos.

        Requer confirmação exata e uma camada superior que autentique o usuário.
        """
        usuario = texto_valido(usuario, "usuario", 128)
        if confirmacao != "EXCLUIR TODOS OS MEUS DADOS":
            raise ErroDeValidacao("Confirmação de exclusão ausente")
        with self.conexao:
            total = self.conexao.execute("SELECT count(*) FROM memorias WHERE usuario=?", (usuario,)).fetchone()[0]
            self.conexao.execute("DELETE FROM eventos WHERE usuario=?", (usuario,))
            # Auto-referências substitui: remover todos os ids de uma vez funciona no SQLite.
            self.conexao.execute("DELETE FROM memorias WHERE usuario=?", (usuario,))
        self.conexao.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        return total
