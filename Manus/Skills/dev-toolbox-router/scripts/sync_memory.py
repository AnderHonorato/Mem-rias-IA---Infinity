#!/usr/bin/env python3
"""Safely append Manus memory entries inside the designated GitHub repository.

The script deliberately writes only below <repo>/Manus and never logs credential
values. It can optionally pull, commit, and push, but never force-pushes.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import subprocess
import sys
from pathlib import Path

EXPECTED_REMOTE_RE = re.compile(
    r"github\.com[/:]AnderHonorato/Mem-?rias-IA---Infinity(?:\.git)?/?$",
    re.IGNORECASE,
)
CATEGORIES = {
    "conversas",
    "preferencias",
    "projetos",
    "decisoes",
    "contexto",
    "aprendizados",
    "tarefas",
    "seguranca",
}
SENSITIVE_PATTERNS = [
    (re.compile(r"-----BEGIN [^-]+ PRIVATE KEY-----[\s\S]*?-----END [^-]+ PRIVATE KEY-----", re.I), "[CREDENTIAL_REDACTED]"),
    (re.compile(r"\b(?:ghp|github_pat|sk|sk-proj|xoxb|xoxp|AIza|AKIA)[-_A-Za-z0-9]{12,}\b"), "[CREDENTIAL_REDACTED]"),
    (re.compile(r"(?i)(\b(?:password|passwd|token|secret|api[_ -]?key|client[_ -]?secret|authorization)\b\s*[:=]\s*)([^\s,;]+)"), r"\1[CREDENTIAL_REDACTED]"),
    (re.compile(r"(?i)(Bearer\s+)[A-Za-z0-9._~+/=-]+"), r"\1[CREDENTIAL_REDACTED]"),
]


def run(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run([*args], cwd=repo, text=True, capture_output=True, check=check)


def redact(text: str) -> str:
    for pattern, replacement in SENSITIVE_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def safe_slug(value: str) -> str:
    value = re.sub(r"[^0-9A-Za-zÀ-ÿ._-]+", "-", value.strip())
    value = re.sub(r"-+", "-", value).strip("-.")
    if not value or value in {".", ".."}:
        raise ValueError("título inválido")
    return value[:80]


def ensure_repo(repo: Path) -> None:
    if not (repo / ".git").is_dir():
        raise RuntimeError(f"não é um repositório Git: {repo}")
    remote = run(repo, "git", "remote", "get-url", "origin").stdout.strip()
    if not EXPECTED_REMOTE_RE.search(remote):
        raise RuntimeError("o remote origin não corresponde ao repositório Memórias IA - Infinity")
    (repo / "Manus").mkdir(exist_ok=True)


def within_manus(repo: Path, target: Path) -> Path:
    manus = (repo / "Manus").resolve()
    target = target.resolve()
    try:
        target.relative_to(manus)
    except ValueError as exc:
        raise RuntimeError("operação recusada: o caminho está fora de Manus/") from exc
    return target


def read_content(args: argparse.Namespace) -> str:
    if args.content_file:
        content = Path(args.content_file).read_text(encoding="utf-8")
    else:
        content = args.content or ""
    content = redact(content).strip()
    if not content:
        raise ValueError("conteúdo vazio; forneça --content ou --content-file")
    return content


def append_entry(repo: Path, category: str, title: str, content: str) -> Path:
    if category not in CATEGORIES:
        raise ValueError(f"categoria inválida: {category}")
    now = dt.datetime.now(dt.timezone.utc).astimezone()
    month = now.strftime("%Y-%m")
    target = within_manus(repo, repo / "Manus" / "Memorias" / category / f"{month}.md")
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text(f"# Memórias — {category} — {month}\n\n", encoding="utf-8")
    session_id = safe_slug(title)
    block = (
        f"\n## {now.strftime('%Y-%m-%d %H:%M %z')} — {session_id}\n\n"
        f"{content}\n"
    )
    with target.open("a", encoding="utf-8") as handle:
        handle.write(block)
    return target


def rebuild_index(repo: Path) -> Path:
    index = within_manus(repo, repo / "Manus" / "Memorias" / "INDEX.md")
    root = index.parent
    rows = []
    for category in sorted(CATEGORIES):
        folder = root / category
        files = sorted(folder.glob("*.md")) if folder.is_dir() else []
        for path in files:
            if path.name.lower() == "readme.md":
                continue
            rel = path.relative_to(repo).as_posix()
            rows.append(f"| {category} | [{path.name}]({rel}) | {path.stat().st_size} bytes |")
    text = (
        "# Índice de Memórias da Manus\n\n"
        "Este índice é regenerado pelo script `sync_memory.py`. Todos os caminhos abaixo permanecem dentro de `Manus/Memorias/`.\n\n"
        "| Categoria | Arquivo | Tamanho |\n|---|---|---:|\n"
        + ("\n".join(rows) if rows else "| — | Nenhuma entrada ainda | — |")
        + "\n"
    )
    index.parent.mkdir(parents=True, exist_ok=True)
    index.write_text(text, encoding="utf-8")
    return index


def git_sync(repo: Path, push: bool, commit_message: str | None) -> None:
    run(repo, "git", "add", "--", "Manus")
    staged = run(repo, "git", "diff", "--cached", "--quiet", check=False)
    if staged.returncode == 0:
        return
    if commit_message:
        run(repo, "git", "commit", "-m", commit_message)
    if push:
        run(repo, "git", "push", "origin", "HEAD")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=os.environ.get("MEMORY_REPO_PATH", "."), help="caminho do clone local autorizado")
    parser.add_argument("--category", choices=sorted(CATEGORIES), default="conversas")
    parser.add_argument("--title", required=True)
    parser.add_argument("--content")
    parser.add_argument("--content-file")
    parser.add_argument("--pull", action="store_true", help="atualizar com git pull --ff-only antes de escrever")
    parser.add_argument("--push", action="store_true", help="enviar somente o conteúdo de Manus para origin")
    parser.add_argument("--commit-message", default="chore(manus): update shared memory")
    args = parser.parse_args()

    try:
        repo = Path(args.repo).expanduser().resolve()
        ensure_repo(repo)
        if args.pull:
            run(repo, "git", "pull", "--ff-only", "origin", "HEAD")
        content = read_content(args)
        target = append_entry(repo, args.category, args.title, content)
        index = rebuild_index(repo)
        git_sync(repo, args.push, args.commit_message)
        print(f"memory_file={target.relative_to(repo)}")
        print(f"index_file={index.relative_to(repo)}")
        return 0
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"sync_memory: {exc}", file=sys.stderr)
        if isinstance(exc, subprocess.CalledProcessError) and exc.stderr:
            print(exc.stderr.strip(), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
