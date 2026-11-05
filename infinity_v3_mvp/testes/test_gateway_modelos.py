"""Nenhum teste dispara tráfego de rede nem usa credenciais reais."""
import os
import unittest
from unittest.mock import patch

from infinity_v3.gateway_modelos import (
    ConfiguracaoModelo, ErroGateway, ErroPermissao, GatewayModelos,
    PermissaoChamada, SolicitacaoModelo, transporte_http,
)
from infinity_v3.agentes_modelos import Atribuicao, PreparadorAgentes
from infinity_v3.orquestrador import Tarefa


class TesteGateway(unittest.TestCase):
    def setUp(self):
        self.chamadas = []
        def mock(url, cabecalhos, corpo, timeout):
            self.chamadas.append((url, cabecalhos, corpo, timeout))
            if "openai.com" in url:
                return {"output": [{"type": "message", "content": [
                    {"type": "output_text", "text": "Resposta verificada"}]}],
                    "usage": {"input_tokens": 12, "output_tokens": 7}}
            if "anthropic.com" in url:
                return {"content": [{"type": "text", "text": "Resposta Claude"}],
                        "usage": {"input_tokens": 15, "output_tokens": 8}}
            return {"message": {"content": "Resposta local"},
                    "prompt_eval_count": 4, "eval_count": 10}
        self.gateway = GatewayModelos(transporte=mock)
        self.local = ConfiguracaoModelo("ollama", "modelo-local")
        self.oa = ConfiguracaoModelo("openai", "modelo-openai", .01, .02)
        self.an = ConfiguracaoModelo("anthropic", "modelo-claude", .02, .04)
        self.publico = SolicitacaoModelo("Responda em português", "Teste sintético")
        self.pago = PermissaoChamada(True, True, True, False, 1, 2, 4)

    def test_inicialmente_bloqueado(self):
        with self.assertRaises(ErroPermissao):
            self.gateway.responder(self.local, self.publico, PermissaoChamada())
        self.assertEqual([], self.chamadas)

    def test_nuvem_necessita_permissao_custo_credencial(self):
        with self.assertRaises(ErroPermissao):
            self.gateway.responder(self.oa, self.publico,
                PermissaoChamada(rede_habilitada=True, limite_chamadas=1))
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
            with self.assertRaises(ErroPermissao):
                self.gateway.responder(self.oa, self.publico, self.pago)
        self.assertEqual([], self.chamadas)

    def test_ollama_local_autorizado(self):
        permissao = PermissaoChamada(rede_habilitada=True, limite_chamadas=2)
        r = self.gateway.responder(self.local, self.publico, permissao)
        self.assertEqual("Resposta local", r.texto)
        self.assertEqual("http://127.0.0.1:11434/api/chat", self.chamadas[0][0])
        self.assertEqual(False, self.chamadas[0][2]["stream"])
        self.assertNotIn("Authorization", self.chamadas[0][1])

    def test_openai_payload_e_parse(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "chave-ficticia-do-teste"}):
            resposta = self.gateway.responder(self.oa, self.publico, self.pago)
        self.assertEqual("Resposta verificada", resposta.texto)
        self.assertEqual((12, 7), (resposta.tokens_entrada, resposta.tokens_saida))
        self.assertEqual(False, self.chamadas[0][2]["store"])
        self.assertEqual("Bearer chave-ficticia-do-teste", self.chamadas[0][1]["Authorization"])
        self.assertEqual((1, resposta.custo_reservado), self.gateway.resumo_contagem)

    def test_anthropic_payload_e_parse(self):
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "chave-ficticia-do-teste"}):
            resposta = self.gateway.responder(self.an, self.publico, self.pago)
        self.assertEqual("Resposta Claude", resposta.texto)
        self.assertEqual("2026-10-21", self.chamadas[0][1]["anthropic-version"])
        self.assertEqual(1, len(self.chamadas[0][2]["messages"]))

    def test_dado_sensivel_nunca_nuvem(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "chave-ficticia-do-teste"}):
            with self.assertRaises(ErroPermissao):
                self.gateway.responder(self.oa,
                    SolicitacaoModelo("Instrução", "Segredo fictício", "sensivel"), self.pago)
        self.assertEqual([], self.chamadas)

    def test_dado_interno_precisa_permissao_especifica(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "chave-ficticia-do-teste"}):
            with self.assertRaises(ErroPermissao):
                self.gateway.responder(self.oa,
                    SolicitacaoModelo("Instrução", "Projeto interno", "interna"), self.pago)
        self.assertEqual([], self.chamadas)

    def test_precos_e_budget_nao_podem_burlar(self):
        sem_preco = ConfiguracaoModelo("openai", "modelo-openai")
        with patch.dict(os.environ, {"OPENAI_API_KEY": "chave-ficticia-do-teste"}):
            with self.assertRaises(ErroPermissao):
                self.gateway.responder(sem_preco, self.publico, self.pago)
            with self.assertRaises(ErroPermissao):
                self.gateway.responder(self.oa, self.publico,
                    PermissaoChamada(True, True, True, False, .000001, .000001, 3))
        self.assertEqual([], self.chamadas)

    def test_limite_de_chamadas_sem_desvio(self):
        pol = PermissaoChamada(rede_habilitada=True, limite_chamadas=1)
        self.gateway.responder(self.local, self.publico, pol)
        with self.assertRaises(ErroPermissao):
            self.gateway.responder(self.local, self.publico, pol)
        self.assertEqual(1, len(self.chamadas))

    def test_nunca_aceitar_destino_arbitrario(self):
        with self.assertRaises(ErroGateway):
            transporte_http("http://192.168.0.1/admin", {}, {}, 1)

    def test_exception_dos_transportes_nao_vaza_segredo(self):
        def falha(*args):
            raise RuntimeError("minha-chave-ficticia-que-nao-deve-aparecer")
        gw = GatewayModelos(transporte=falha)
        with self.assertRaises(ErroGateway) as ctx:
            gw.responder(self.local, self.publico,
                PermissaoChamada(rede_habilitada=True, limite_chamadas=1))
        self.assertNotIn("minha-chave", str(ctx.exception))

    def test_resposta_malformada_bloqueada(self):
        gw = GatewayModelos(transporte=lambda *_: {"output": []})
        with patch.dict(os.environ, {"OPENAI_API_KEY": "chave-ficticia-do-teste"}):
            with self.assertRaises(ErroGateway):
                gw.responder(self.oa, self.publico, self.pago)

    def test_modelo_nunca_usa_endpoint_personalizado(self):
        with self.assertRaises(ValueError):
            ConfiguracaoModelo("openai", "https://servidor-invalido.local/responses")


class TesteAgentesLLM(unittest.TestCase):
    def test_agente_mais_critico_aprovam_em_simulacao_http(self):
        chamadas = []
        def falso(url, headers, body, timeout):
            chamadas.append(body)
            texto = ('{"aprovado": true, "justificativa": "Evidência revisada"}'
                     if "revisor" in body.get("instructions", "") else "Relatório sintético")
            return {"output": [{"type": "message", "content": [{"type": "output_text", "text": texto}]}]}
        gw = GatewayModelos(transporte=falso)
        config = ConfiguracaoModelo("openai", "modelo-ficticio", .01, .01)
        perm = PermissaoChamada(True, True, True, True, 1, 2, 3)
        with patch.dict(os.environ, {"OPENAI_API_KEY": "chave-testes-ficticia"}):
            grupo = PreparadorAgentes(gw, agentes={"backend": Atribuicao(config, perm)},
                criticos={"critico_corretude": Atribuicao(config, perm)})
            motor = grupo.orquestrador(maximo_paralelo=1)
            resultados = motor.executar([Tarefa(id="caso-1", agente="backend",
                entrada={"objetivo": "Descrever a interface", "classificacao": "publica"},
                criticos=("critico_corretude",))])
        self.assertEqual("aprovada", resultados[0].estado)
        self.assertEqual(2, len(chamadas))
        self.assertEqual(2, gw.resumo_contagem[0])

    def test_critico_json_invalido_nao_aprova(self):
        def falso(*args):
            return {"message": {"content": "aprovar sem JSON"}}
        gw = GatewayModelos(transporte=falso)
        pol = PermissaoChamada(rede_habilitada=True, limite_chamadas=2)
        con = Atribuicao(ConfiguracaoModelo("ollama", "local-fake"), pol)
        grupo = PreparadorAgentes(gw, agentes={"backend": con},
                                  criticos={"critico_seguranca": con})
        resultados = grupo.orquestrador().executar([Tarefa(id="id-1", agente="backend",
            entrada={"objetivo": "Relatório", "classificacao": "publica"},
            criticos=("critico_seguranca",))])
        self.assertEqual("reprovada", resultados[0].estado)

    def test_classificacao_nao_informada_falha_fechada(self):
        gw = GatewayModelos(transporte=lambda *_: {"message": {"content": "sim"}})
        pol = PermissaoChamada(rede_habilitada=True, limite_chamadas=2)
        c = Atribuicao(ConfiguracaoModelo("ollama", "ficticio"), pol)
        grupo = PreparadorAgentes(gw, agentes={"backend": c},
                                  criticos={"critico_seguranca": c})
        r = grupo.orquestrador().executar([Tarefa(id="id-1", agente="backend",
            entrada={"objetivo": "Relatório"}, criticos=("critico_seguranca",))])
        self.assertEqual("erro", r[0].estado)
        self.assertEqual((0, 0.0), gw.resumo_contagem)


if __name__ == "__main__":
    unittest.main()
