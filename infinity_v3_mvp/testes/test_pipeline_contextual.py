import json
import unittest
from unittest.mock import patch

from infinity_v3.gateway_modelos import ConfiguracaoModelo, GatewayModelos, ErroPermissao, PermissaoChamada
from infinity_v3.roteador import Modelo, Politica, NenhumModeloElegivel
from infinity_v3.roteamento_modelos import RegistroModelo, RoteamentoExecutavel
from infinity_v3.pipeline_contextual import PipelineContextual


class FakeBuscadorCanonico:
    def __init__(self):
        self.chamadas = []
    def buscar(self, **args):
        self.chamadas.append(args)
        return [{"id": "PREF-2026-000001", "titulo": "Pref", "conteudo": "Preferir respostas curtas e claras com referências.",
                 "escopo": "global", "origem": "knowledge/preferencias/ficticia.md"}]


class FakeBuscadorLocal:
    def __init__(self):
        self.chamadas = []
    def buscar(self, **args):
        self.chamadas.append(args)
        return [{"id": "local-1", "titulo": "Segredo fictício", "conteudo": "Informação local sintética não publicável.",
                 "escopo": "projeto:teste", "origem": "db-local"}]


class TestePipeline(unittest.TestCase):
    def setUp(self):
        self.chamadas = []
        def falso(url, headers, body, timeout):
            self.chamadas.append((url, body))
            if '127.0.0.1' in url:
                return {"message": {"content": "Resposta baseada nos registros"}}
            return {"output": [{"type": "message", "content": [
                {"type": "output_text", "text": "Resposta na nuvem"}]}]}
        self.gateway = GatewayModelos(transporte=falso)
        registros = [
            RegistroModelo(Modelo("local-sintetico", "profundo", True, True, 0, 5),
                           ConfiguracaoModelo("ollama", "local-sintetico")),
            RegistroModelo(Modelo("nuvem-sintetica", "profundo", True, False, .1, 100),
                           ConfiguracaoModelo("openai", "nuvem-sintetica", .01, .04)),
        ]
        self.roteador = RoteamentoExecutavel(self.gateway, registros)
        self.canonico = FakeBuscadorCanonico()
        self.local = FakeBuscadorLocal()
        self.pipeline = PipelineContextual(roteador=self.roteador, indice_canonico=self.canonico,
                                           motor_local=self.local)
        self.permite_local = PermissaoChamada(rede_habilitada=True, limite_chamadas=4)

    def _responder(self, **kw):
        args = dict(pergunta="respostas curtas", usuario_autenticado="usuario-sintetico",
                    escopos_canonicos=["global"], escopos_locais=[],
                    politica_roteamento=Politica(), permissao_rede=self.permite_local)
        args.update(kw)
        return self.pipeline.responder(**args)

    def test_canonico_rebaixado_interno_e_nao_exfiltra(self):
        r = self._responder(classificacao_pergunta="publica")
        self.assertEqual("interna", r.classificacao_efetiva)
        self.assertEqual(1, r.total_trechos)
        self.assertEqual("ollama", r.provedor)
        self.assertIn("knowledge/preferencias/ficticia.md", r.referencias)
        corpo = self.chamadas[0][1]
        self.assertIn("memorias_nao_confiaveis", corpo["messages"][1]["content"])

    def test_local_forca_sensivel_mesmo_entrada_publica(self):
        r = self._responder(escopos_locais=["projeto:teste"], classificacao_pergunta="publica")
        self.assertEqual("sensivel", r.classificacao_efetiva)
        self.assertEqual("ollama", r.provedor)
        self.assertEqual("usuario-sintetico", self.local.chamadas[0]["usuario"])

    def test_sem_local_disponivel_bloqueia_nuvem_para_dado_sensivel(self):
        nuvem = RoteamentoExecutavel(self.gateway, [
            RegistroModelo(Modelo("nuvem-sintetica", "profundo", True, False, .1, 50),
                           ConfiguracaoModelo("openai", "nuvem-sintetica", .01, .04))])
        pipeline = PipelineContextual(roteador=nuvem, indice_canonico=self.canonico,
                                      motor_local=self.local)
        with self.assertRaises(NenhumModeloElegivel):
            pipeline.responder(pergunta="respostas curtas", usuario_autenticado="teste",
                escopos_canonicos=["global"], escopos_locais=["projeto:teste"],
                politica_roteamento=Politica(permite_pago=True, permite_nuvem=True, teto_estimado=2),
                permissao_rede=PermissaoChamada(True, True, True, True, 2, 2, 3),
                classificacao_pergunta="publica")
        self.assertEqual([], self.chamadas)

    def test_sem_consentimento_de_rede_negado(self):
        with self.assertRaises(ErroPermissao):
            self._responder(permissao_rede=PermissaoChamada())
        self.assertEqual([], self.chamadas)

    def test_escopos_invalidos_nao_consultam_banco(self):
        with self.assertRaises(ValueError):
            self._responder(escopos_locais="global")
        self.assertEqual([], self.local.chamadas)
        self.assertEqual([], self.canonico.chamadas)


if __name__ == '__main__':
    unittest.main()
