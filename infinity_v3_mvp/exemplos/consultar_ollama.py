"""Consulta demonstrativa ao Ollama local, mediante consentimento explícito.

Não há nenhuma conexão ou chamada sem a flag --autorizo-rede-local.
Não carregue memória privada, nem dados pessoais neste exemplo.
"""
from __future__ import annotations

import argparse
from infinity_v3.gateway_modelos import (
    ConfiguracaoModelo, GatewayModelos, PermissaoChamada, SolicitacaoModelo, ErroGateway,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verificar Ollama local em modo opt-in")
    parser.add_argument("--modelo", required=True, help="Modelo já instalado no Ollama local")
    parser.add_argument("--autorizo-rede-local", action="store_true")
    args = parser.parse_args()
    if not args.autorizo_rede_local:
        print("SEM EXECUÇÃO: passe --autorizo-rede-local para autorizar uma requisição ao Ollama.")
        return 2
    try:
        resposta = GatewayModelos().responder(
            ConfiguracaoModelo("ollama", args.modelo),
            SolicitacaoModelo("Responda em português, em uma frase.",
                             "O que é um teste automatizado?", classificacao="publica", max_tokens_saida=96),
            PermissaoChamada(rede_habilitada=True, limite_chamadas=1),
        )
    except ErroGateway as exc:
        print(f"Falha controlada: {exc}")
        return 1
    print(resposta.texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
