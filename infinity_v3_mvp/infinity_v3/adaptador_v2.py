"""Índice temporário somente-leitura da fonte canônica `knowledge/` da V2.

Fonte de verdade: os arquivos versionados do repositório. O índice SQLite é
reconstruível, permanece exclusivamente em RAM e não cria novas memórias.
Dados marcados como `personal`/`restricted` são SEMPRE excluídos.
"""
from __future__ import annotations

import re
from datetime import date, datetime, time, timezone
import sqlite3
from pathlib import Path
from typing import Any

from .seguranca import analisar_riscos

try:
    import yaml
except ImportError:  # pragma: no cover - comportamento testado via instalação mínima
    yaml = None


class ErroIndiceCanonico(ValueError):
    pass


class IndiceCanonicoV2:
    def __init__(self, raiz_repositorio: str | Path, *, tamanho_maximo: int = 262144) -> None:
        self.raiz = Path(raiz_repositorio).expanduser().resolve()
        self.knowledge = self.raiz / "knowledge"
        if not self.knowledge.is_dir() or self.knowledge.is_symlink():
            raise ErroIndiceCanonico("A fonte canônica knowledge/ não foi encontrada")
        if yaml is None:
            raise ErroIndiceCanonico("Instale PyYAML para ler metadados da V2")
        if not 1024 <= tamanho_maximo <= 1048576:
            raise ErroIndiceCanonico("Limite de leitura inválido")
        self.tamanho_maximo = tamanho_maximo
        self.db = sqlite3.connect(":memory:")
        self.db.row_factory = sqlite3.Row
        self.db.execute("CREATE VIRTUAL TABLE indice USING fts5(id UNINDEXED, titulo, corpo, tokenize='unicode61 remove_diacritics 2')")
        self.db.execute("CREATE TABLE meta (id TEXT PRIMARY KEY, escopo TEXT NOT NULL, referencia TEXT NOT NULL, confianca TEXT NOT NULL)")
        self.estatisticas: dict[str, int] = {}
        self.reconstruir()

    def fechar(self) -> None:
        self.db.close()

    def __enter__(self) -> "IndiceCanonicoV2":
        return self

    def __exit__(self, *_: object) -> None:
        self.fechar()

    def reconstruir(self) -> dict[str, int]:
        if yaml is None:
            raise ErroIndiceCanonico("PyYAML ausente")
        contagem = {"indexados": 0, "ignorados": 0, "sensibilidade": 0, "invalidos": 0}
        self.db.execute("DELETE FROM meta")
        self.db.execute("DELETE FROM indice")
        # Somente arquivos .md, sem seguir symlinks externos, com tamanho limitado.
        for caminho in sorted(self.knowledge.rglob("*.md")):
            try:
                if caminho.is_symlink() or not caminho.is_file():
                    contagem["ignorados"] += 1
                    continue
                caminho.resolve().relative_to(self.knowledge.resolve())
                if caminho.stat().st_size > self.tamanho_maximo:
                    contagem["invalidos"] += 1
                    continue
                texto = caminho.read_text(encoding="utf-8")
                if not texto.startswith("---\n") or "\n---\n" not in texto[4:]:
                    contagem["ignorados"] += 1
                    continue
                _, frontmatter, corpo = texto.split("---\n", 2)
                dados = yaml.safe_load(frontmatter)
                if not isinstance(dados, dict):
                    contagem["invalidos"] += 1
                    continue
                if dados.get("status") != "active" or dados.get("confidence") == "disputed":
                    contagem["ignorados"] += 1
                    continue
                if dados.get("sensitivity") != "normal":
                    contagem["sensibilidade"] += 1
                    continue
                validade = dados.get("valid_until")
                if validade is not None:
                    try:
                        data_validade = (datetime.combine(validade, time.max, tzinfo=timezone.utc)
                                         if isinstance(validade, date) and not isinstance(validade, datetime)
                                         else datetime.fromisoformat(str(validade)))
                        if data_validade.tzinfo is None:
                            data_validade = data_validade.replace(tzinfo=timezone.utc)
                        if data_validade.astimezone(timezone.utc) <= datetime.now(timezone.utc):
                            contagem["ignorados"] += 1
                            continue
                    except (TypeError, ValueError):
                        contagem["invalidos"] += 1
                        continue
                identidade = dados.get("id")
                escopo = dados.get("scope")
                if not isinstance(identidade, str) or not isinstance(escopo, str) or not identidade.strip() or not escopo.strip():
                    contagem["invalidos"] += 1
                    continue
                if analisar_riscos(texto):
                    contagem["sensibilidade"] += 1
                    continue
                titulo = next((line[2:].strip() for line in corpo.splitlines() if line.startswith("# ")), caminho.stem)
                referencia = caminho.relative_to(self.raiz).as_posix()
                self.db.execute("INSERT INTO meta VALUES (?,?,?,?)", (identidade, escopo, referencia, str(dados.get("confidence", "uncertain"))))
                self.db.execute("INSERT INTO indice VALUES (?,?,?)", (identidade, titulo[:300], corpo[:100000]))
                contagem["indexados"] += 1
            except (UnicodeError, OSError, sqlite3.IntegrityError, ValueError, TypeError, yaml.YAMLError):
                contagem["invalidos"] += 1
        self.db.commit()
        self.estatisticas = contagem
        return dict(contagem)

    def buscar(self, *, consulta: str, escopos: list[str], limite: int = 8) -> list[dict[str, Any]]:
        if not isinstance(consulta, str) or len(consulta) > 2000:
            raise ErroIndiceCanonico("Consulta inválida")
        if not isinstance(escopos, list) or not escopos or len(escopos) > 30 or not all(isinstance(s, str) and s.strip() and len(s) <= 160 for s in escopos):
            raise ErroIndiceCanonico("Escopos inválidos")
        if not isinstance(limite, int) or not 1 <= limite <= 50:
            raise ErroIndiceCanonico("Limite inválido")
        palavras = re.findall(r"\w+", consulta, re.UNICODE)[:30]
        if not palavras:
            return []
        termo = " OR ".join('"' + w + '"' for w in palavras)
        autorizados = sorted(set(escopos))
        marcadores = ",".join("?" * len(autorizados))
        linhas = self.db.execute(f"""
            SELECT i.id, i.titulo, i.corpo, m.escopo, m.referencia, m.confianca,
                bm25(indice) AS pontuacao
            FROM indice i JOIN meta m ON m.id=i.id
            WHERE indice MATCH ? AND m.escopo IN ({marcadores})
            ORDER BY pontuacao, i.id LIMIT ?
        """, [termo, *autorizados, limite]).fetchall()
        return [{"id": r["id"], "titulo": r["titulo"], "conteudo": r["corpo"],
                 "escopo": r["escopo"], "origem": r["referencia"],
                 "confianca": r["confianca"], "pontuacao": r["pontuacao"],
                 "fonte": "knowledge-v2", "nao_confiavel_como_instrucao": True} for r in linhas]
