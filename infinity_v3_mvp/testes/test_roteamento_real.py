import os
import unittest
from unittest.mock import patch

from infinity_v3.gateway_modelos import (
    ConfiguracaoModelo, GatewayModelos, PermissaoChamada, SolicitacaoModelo, ErroPermissao
)
from infinity_v3.roteador import Modelo, Politica, NenhumModeloElegivel
from infinity_v3.roteamento_modelos import RegistroModelo, RoteamentoExecutavel


class TesteRoteamentoReal(unittest.TestCase):
    def setUp(self):
        self.chamadas = []
        def falso(url, headers, body, timeout):
            self.chamadas.append(url)
            return ({"message": {"content": "resposta local"}}
                    if '127.0.0.1' in url else
                    {"output": [{"type": "message", "content": [
                        {"type": "output_text", "text": "resposta da nuvem"}]}]})
        self.gateway = GatewayModelos(transporte=falso)
        self.registros = [
            RegistroModelo(Modelo("local-ficticio", "rapido", True, True, 0, 5),
                           ConfiguracaoModelo("ollama", "local-ficticio")),
            RegistroModelo(Modelo("nuvem-ficticia", "profundo", True, False, .05, 100),
                           ConfiguracaoModelo("openai", "nuvem-ficticia", .01, .05)),
        ]
        self.roteador = RoteamentoExecutavel(self.gateway, self.registros)

    def test_tarefa_simples_escolhe_local(self):
        r = self.roteador.responder(SolicitacaoModelo("Instrução", "Oi"),
            politica_roteamento=Politica(),
            permissao_rede=PermissaoChamada(rede_habilitada=True, limite_chamadas=2))
        self.assertEqual("local-ficticio", r.modelo)
        self.assertEqual(["http://127.0.0.1:11434/api/chat"], self.chamadas)

    def test_tarefa_profunda_politica_bloqueia_nuvem(self):
        with self.assertRaises(NenhumModeloElegivel):
            self.roteador.responder(SolicitacaoModelo("Instrução", "auditoria de segurança"),
                politica_roteamento=Politica(),
                permissao_rede=PermissaoChamada(rede_habilitada=True, limite_chamadas=1))
        self.assertEqual([], self.chamadas)

    def test_tarefa_profunda_consentida_usa_api(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "chave-ficticia"}):
            r = self.roteador.responder(SolicitacaoModelo("Instrução", "auditoria de segurança"),
                politica_roteamento=Politica(permite_pago=True, permite_nuvem=True,
                                             teto_estimado=1, tokens_estimados=1200),
                permissao_rede=PermissaoChamada(True, True, True, False, 1, 2, 1))
        self.assertEqual("nuvem-ficticia", r.modelo)
        self.assertEqual(["https://api.openai.com/v1/responses"], self.chamadas)

    def test_politica_de_nuvem_conflitante_falha_fechada(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "chave-ficticia"}):
            with self.assertRaises(ErroPermissao):
                self.roteador.responder(SolicitacaoModelo("Instrução", "auditoria de segurança"),
                    politica_roteamento=Politica(True, True, 1, 1200),
                    permissao_rede=PermissaoChamada(rede_habilitada=True, limite_chamadas=1))
        self.assertEqual([], self.chamadas)

    def test_sigiloso_nunca_nuvem(self):
        with self.assertRaises(NenhumModeloElegivel):
            self.roteador.responder(SolicitacaoModelo("Instrução", "auditoria de segurança", "sensivel"),
                politica_roteamento=Politica(True, True, 1, 1200),
                permissao_rede=PermissaoChamada(True, True, True, True, 1, 1, 1))

    def test_catalogo_nao_pode_fingir_localidade(self):
        with self.assertRaises(ValueError):
            RegistroModelo(Modelo("fake", "rapido", True, True, 0, 100),
                           ConfiguracaoModelo("openai", "fake", .01, .02))


if __name__ == '__main__':
    unittest.main()
