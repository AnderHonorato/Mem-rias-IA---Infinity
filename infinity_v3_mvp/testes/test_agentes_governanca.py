"""Testes dos contratos de agentes, revisão independente e ferramenta segura."""
import json
import os
import tempfile
import unittest
from pathlib import Path

from infinity_v3.auditoria import RegistroAuditoria, ErroAuditoria
from infinity_v3.catalogo_agentes import AGENTES, CRITICOS, criticos_exigidos
from infinity_v3.execucao_supervisionada import Supervisao, TarefaSupervisionada
from infinity_v3.ferramentas import Ferramenta, PoliticaFerramentas, ExecutorControlado, AcaoNaoAutorizada
from infinity_v3.orquestrador import OrquestradorLocal, Tarefa, ErroDePlano


class TesteGovernanca(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self.tmp.name)
        self.chave = b"sintetica-de-teste-" * 3

    def tearDown(self):
        self.tmp.cleanup()

    def test_catalogo_12_agentes_6_criticos_sem_conflito(self):
        self.assertEqual(12, len(AGENTES))
        self.assertEqual(6, len(CRITICOS))
        self.assertFalse(set(AGENTES) & set(CRITICOS))
        self.assertEqual(2, criticos_exigidos("alto"))

    def test_alto_risco_exige_dois_criticos_reais_registrados(self):
        orq = OrquestradorLocal(
            agentes={"backend": lambda x: {"ok": True}},
            criticos={"critico_corretude": lambda x: (True, "ok"),
                     "critico_seguranca": lambda x: (True, "ok")})
        supervisao = Supervisao(orq)
        with self.assertRaises(ErroDePlano):
            supervisao.executar([TarefaSupervisionada(Tarefa("A", "backend", {},
                criticos=("critico_corretude",)), "alto")])
        r = supervisao.executar([TarefaSupervisionada(Tarefa("A", "backend", {},
                criticos=("critico_corretude", "critico_seguranca")), "alto")])
        self.assertEqual("aprovada", r[0].estado)
        self.assertEqual(2, len(r[0].pareceres))

    def test_recusa_critico_duplicado(self):
        orq = OrquestradorLocal(agentes={"backend": lambda x: {"ok": True}},
            criticos={"critico_corretude": lambda x: (True, "ok")})
        with self.assertRaises(ErroDePlano):
            Supervisao(orq).executar([TarefaSupervisionada(Tarefa("A", "backend", {},
                criticos=("critico_corretude", "critico_corretude")))])

    def test_auditoria_hmac_verificavel_sem_dados_brutos(self):
        caminho = self.raiz / "auditoria.jsonl"
        registro = RegistroAuditoria(caminho, chave=self.chave)
        primeiro = registro.registrar(tarefa="A", agente="backend", estado="aprovada", revisores=2)
        segundo = registro.registrar(tarefa="B", agente="qa", estado="bloqueada", revisores=0)
        self.assertEqual(segundo, registro.verificar())
        outro = RegistroAuditoria(caminho, chave=self.chave)
        self.assertEqual(segundo, outro.verificar())
        texto = caminho.read_text()
        self.assertNotIn("código", texto)
        self.assertIn(primeiro, texto)

    def test_auditoria_detecta_alteracao(self):
        caminho = self.raiz / "auditoria.jsonl"
        registro = RegistroAuditoria(caminho, chave=self.chave)
        registro.registrar(tarefa="A", agente="backend", estado="aprovada", revisores=2)
        conteudo = caminho.read_text().replace('"aprovada"', '"reprovada"')
        caminho.write_text(conteudo)
        with self.assertRaises(ErroAuditoria):
            registro.verificar()
        with self.assertRaises(ErroAuditoria):
            RegistroAuditoria(caminho, chave=self.chave)

    def test_auditoria_rejeita_chave_curta_e_campos_nao_id(self):
        with self.assertRaises(ErroAuditoria):
            RegistroAuditoria(self.raiz / "evento.jsonl", chave=b"chave-curta")
        registro = RegistroAuditoria(self.raiz / "evento.jsonl", chave=self.chave)
        with self.assertRaises(ErroAuditoria):
            registro.registrar(tarefa="minha senha: abcdef", agente="backend", estado="aprovada", revisores=1)

    @unittest.skipUnless(os.name == "posix", "Permissões POSIX")
    def test_auditoria_arquivo_posix_so_dono(self):
        caminho = self.raiz / "evento.jsonl"
        registro = RegistroAuditoria(caminho, chave=self.chave)
        registro.registrar(tarefa="A", agente="qa", estado="aprovada", revisores=1)
        self.assertEqual(0o600, caminho.stat().st_mode & 0o777)

    def test_supervisao_registra_resultados_sem_entradas(self):
        caminho = self.raiz / "auditoria.jsonl"
        auditoria = RegistroAuditoria(caminho, chave=self.chave)
        orq = OrquestradorLocal(agentes={"backend": lambda e: {"mensagem": e["privado"]}},
            criticos={"critico_corretude": lambda x: (True, "ok")})
        tarefas = [TarefaSupervisionada(Tarefa("A", "backend", {"privado": "NAO_GRAVAR_ESSE_TEXTO"},
             criticos=("critico_corretude",)))]
        r = Supervisao(orq, auditoria).executar(tarefas)
        self.assertEqual("aprovada", r[0].estado)
        self.assertNotIn("NAO_GRAVAR_ESSE_TEXTO", caminho.read_text())


class TesteFerramentas(unittest.TestCase):
    def setUp(self):
        self.chamadas = []
        self.gateway = ExecutorControlado([
            Ferramenta("ler", "leitura", lambda e: self._marcar("ler", e)),
            Ferramenta("escrever", "escrita", lambda e: self._marcar("escrever", e)),
            Ferramenta("apagar", "destrutiva", lambda e: self._marcar("apagar", e))],
            limite_por_instancia=10)

    def _marcar(self, nome, entrada):
        self.chamadas.append(nome)
        return {"feito": nome}

    def test_simulacao_padrao_nao_dispara_acao(self):
        p = PoliticaFerramentas(frozenset({"escrever"}), permite_escrever=True,
                               confirmacoes=frozenset({"confirmar-1"}))
        r = self.gateway.executar(nome="escrever", entrada={"texto": "sensível"},
                                  politica=p, id_confirmacao="confirmar-1")
        self.assertEqual("simulacao", r["estado"])
        self.assertEqual([], self.chamadas)
        self.assertNotIn("texto", str(r))

    def test_leitura_explicitamente_permitida(self):
        p = PoliticaFerramentas(frozenset({"ler"}), simular=False)
        self.assertEqual("ler", self.gateway.executar(nome="ler", entrada={}, politica=p)["feito"])

    def test_bloqueia_escrita_nao_autorizada(self):
        with self.assertRaises(AcaoNaoAutorizada):
            self.gateway.executar(nome="escrever", entrada={}, politica=PoliticaFerramentas(frozenset({"escrever"}), simular=False))
        self.assertEqual([], self.chamadas)

    def test_acao_exige_confirmacao_de_uso_unico(self):
        p = PoliticaFerramentas(frozenset({"escrever"}), permite_escrever=True,
                               confirmacoes=frozenset({"confirmar-1"}), simular=False)
        self.gateway.executar(nome="escrever", entrada={}, politica=p, id_confirmacao="confirmar-1")
        with self.assertRaises(AcaoNaoAutorizada):
            self.gateway.executar(nome="escrever", entrada={}, politica=p, id_confirmacao="confirmar-1")
        self.assertEqual(["escrever"], self.chamadas)

    def test_destrutivo_exige_dupla_permissao(self):
        p = PoliticaFerramentas(frozenset({"apagar"}), permite_escrever=True, simular=False,
                               confirmacoes=frozenset({"confirmar-2"}))
        with self.assertRaises(AcaoNaoAutorizada):
            self.gateway.executar(nome="apagar", entrada={}, politica=p, id_confirmacao="confirmar-2")
        self.assertEqual([], self.chamadas)

    def test_bloqueia_ferramenta_fora_allowlist(self):
        with self.assertRaises(AcaoNaoAutorizada):
            self.gateway.executar(nome="apagar", entrada={}, politica=PoliticaFerramentas(frozenset({"ler"})))

    def test_erro_nao_vaza_excecao_interna(self):
        gateway = ExecutorControlado([Ferramenta("falha", "leitura", lambda e: 1 / 0)])
        with self.assertRaises(RuntimeError) as exc:
            gateway.executar(nome="falha", entrada={"segredo": "do-not-print"},
                politica=PoliticaFerramentas(frozenset({"falha"}), simular=False))
        self.assertNotIn("do-not-print", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
