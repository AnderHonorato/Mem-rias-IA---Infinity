#!/usr/bin/env python3
"""Append a structured message to the shared inter-AI conversation.

This script writes only to the explicitly authorized shared conversation folder,
never to another assistant's private area. Use --pull before writing and --push
after writing when the local clone is authenticated.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import os
import re
import subprocess
import sys
from pathlib import Path

EXPECTED_REMOTE_RE = re.compile(
    r"github\.com[/:]AnderHonorato/Mem-?rias-IA---Infinity(?:\.git)?/?$",
    re.IGNORECASE,
)
TYPES = {"PERGUNTA", "RESPOSTA", "ATUALIZAÇÃO", "ALERTA", "SOLICITAÇÃO"}
SENSITIVE_PATTERNS = [
    (re.compile(r"-----BEGIN [^-]+ PRIVATE KEY-----[\s\S]*?-----END [^-]+ PRIVATE KEY-----", re.I), "[CREDENTIAL_REDACTED]"),
    (re.compile(r"\b(?:ghp|github_pat|sk|sk-proj|xoxb|xoxp|AIza|AKIA)[-_A-Za-z0-9]{12,}\b"), "[CREDENTIAL_REDACTED]"),
    (re.compile(r"(?i)(\b(?:password|passwd|token|secret|api[_ -]?key|client[_ -]?secret|authorization)\b\s*[:=]\s*)([^\s,;]+)"), r"\1[CREDENTIAL_REDACTED]"),
    (re.compile(r"(?i)(Bearer\s+)[A-Za-z0-9._~+/=-]+"), r"\1[CREDENTIAL_REDACTED]"),
]


def run(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run([*args], cwd=repo, text=True, capture_output=True, check=check)


def clean(text: str) -> str:
    for pattern, replacement in SENSITIVE_PATTERNS:
        text = pattern.sub(replacement, text)
    return text.strip()


def single_line(value: str, field: str) -> str:
    value = clean(value).replace("\n", " ").replace("\r", " ").strip()
    if not value:
        raise ValueError(f"{field} não pode ficar vazio")
    return value


def ensure_repo(repo: Path) -> None:
    if not (repo / ".git").is_dir():
        raise RuntimeError(f"não é um repositório Git: {repo}")
    remote = run(repo, "git", "remote", "get-url", "origin").stdout.strip()
    if not EXPECTED_REMOTE_RE.search(remote):
        raise RuntimeError("o remote origin não corresponde ao repositório Memórias IA - Infinity")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=os.environ.get("MEMORY_REPO_PATH", "."))
    parser.add_argument("--ai", required=True, help="nome da IA que escreve")
    parser.add_argument("--to", required=True, help="IA ou grupo destinatário")
    parser.add_argument("--type", required=True, choices=sorted(TYPES))
    parser.add_argument("--reply-to", default="NOVA CONVERSA")
    parser.add_argument("--message", required=True)
    parser.add_argument("--action", default="NENHUMA", help="ação esperada do destinatário")
    parser.add_argument("--confidence", default="Não informado")
    parser.add_argument("--source", default="Não informado")
    parser.add_argument("--pull", action="store_true")
    parser.add_argument("--push", action="store_true")
    parser.add_argument("--commit-message", default="chore(shared-chat): append inter-AI message")
    args = parser.parse_args()

    try:
        repo = Path(args.repo).expanduser().resolve()
        ensure_repo(repo)
        if args.pull:
            run(repo, "git", "pull", "--ff-only", "origin", "HEAD")
        target = repo / "Conversa entre IAs" / "conversa-geral.md"
        if not target.exists():
            raise RuntimeError("arquivo compartilhado ausente: crie Conversa entre IAs/conversa-geral.md primeiro")
        target = target.resolve()
        try:
            target.relative_to((repo / "Conversa entre IAs").resolve())
        except ValueError as exc:
            raise RuntimeError("operação recusada: caminho fora da pasta compartilhada") from exc

        now = dt.datetime.now(dt.timezone.utc).astimezone()
        block = (
            f"\n## [{now.strftime('%Y-%m-%d %H:%M %z')}] {single_line(args.ai, 'ai')} → {single_line(args.to, 'to')}\n\n"
            f"**Tipo:** {args.type}\n\n"
            f"**Em resposta a:** {single_line(args.reply_to, 'reply-to')}\n\n"
            f"**Mensagem:**\n{clean(args.message)}\n\n"
            f"**Ação esperada:**\n{clean(args.action) or 'NENHUMA'}\n\n"
            f"**Confiança e fonte:**\n{clean(args.confidence) or 'Não informado'}; {clean(args.source) or 'Não informado'}\n"
        )
        with target.open("a+", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            handle.write(block)
            handle.flush()
            os.fsync(handle.fileno())
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

        if args.push:
            run(repo, "git", "add", "--", "Conversa entre IAs")
            staged = run(repo, "git", "diff", "--cached", "--quiet", check=False)
            if staged.returncode != 0:
                run(repo, "git", "commit", "-m", args.commit_message)
                run(repo, "git", "push", "origin", "HEAD")
        print(f"conversation_file={target.relative_to(repo)}")
        print(f"timestamp={now.strftime('%Y-%m-%d %H:%M %z')}")
        return 0
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"append_shared_conversation: {exc}", file=sys.stderr)
        if isinstance(exc, subprocess.CalledProcessError) and exc.stderr:
            print(exc.stderr.strip(), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
