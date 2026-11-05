import threading
import unittest
from infinity_v3.orquestrador import Tarefa, ErroDePlano
from infinity_v3.orquestracao_paralela import OrquestradorParaleloLocal
from infinity_v3.execucao_supervisionada import Supervisao, TarefaSupervisionada
from infinity_v3.ferramentas import Ferramenta, PoliticaFerramentas, ExecutorControlado, AcaoNaoAutorizada
from infinity_v3.auditoria import RegistroAuditoria
import tempfile
from pathlib import Path


class TesteParalelo(unittest.TestCase):
    def test_independentes_podem_trabalhar_juntos(self):
        barreira = threading.Barrier(2, timeout=3)
        orq = OrquestradorParaleloLocal(maximo_paralelo=2,
            agentes={"backend": lambda entrada: {"concluiu": barreira.wait() is not None},
                     "qa": lambda entrada: {"concluiu": barreira.wait() is not None}},
            criticos={"critico_corretude": lambda s: (True, "passou")})
        r = orq.executar([
            Tarefa("A", "backend", {}, criticos=("critico_corretude",)),
            Tarefa("B", "qa", {}, criticos=("critico_corretude",)),
        ])
        self.assertEqual(["aprovada", "aprovada"], [x.estado for x in r])

    def test_dependencias_e_bloqueios(self):
        orq = OrquestradorParaleloLocal(maximo_paralelo=3,
            agentes={"qa": lambda e: {"rejeitado": True}, "backend": lambda e: {"ok": True}},
            criticos={"critico_corretude": lambda s: (not s.get("rejeitado", False), "checado")})
        r = orq.executar([
            Tarefa("A", "qa", {}, criticos=("critico_corretude",)),
            Tarefa("B", "backend", {}, depende_de=("A",), criticos=("critico_corretude",))])
        self.assertEqual(["reprovada", "bloqueada"], [x.estado for x in r])

    def test_ciclo_recusado(self):
        orq = OrquestradorParaleloLocal(maximo_paralelo=2,
            agentes={"qa": lambda e: {}}, criticos={"critico_corretude": lambda s: (True, "ok")})
        with self.assertRaises(ErroDePlano):
            orq.executar([Tarefa("A", "qa", {}, depende_de=("B",), criticos=("critico_corretude",)),
                Tarefa("B", "qa", {}, depende_de=("A",), criticos=("critico_corretude",))])

    def test_criticos_nao_compartilham_mutacoes(self):
        def primeiro(saida):
            saida["aninhado"]["segredo"] = 42
            return True, "ok"
        def segundo(saida):
            return "segredo" not in saida["aninhado"], "isolado"
        orq = OrquestradorParaleloLocal(maximo_paralelo=1,
            agentes={"backend": lambda entrada: {"aninhado": {}}},
            criticos={"critico_corretude": primeiro, "critico_seguranca": segundo})
        r = orq.executar([Tarefa("A", "backend", {}, criticos=("critico_corretude", "critico_seguranca"))])
        self.assertEqual("aprovada", r[0].estado)

    def test_confirmacao_de_uso_unico_com_threads(self):
        gateway = ExecutorControlado([Ferramenta("escrever", "escrita", lambda e: {"ok": True})])
        politica = PoliticaFerramentas(frozenset({"escrever"}), permite_escrever=True,
            confirmacoes=frozenset({"permitido-uma-vez"}), simular=False)
        estados = []
        def operar():
            try:
                gateway.executar(nome="escrever", entrada={}, politica=politica,
                    id_confirmacao="permitido-uma-vez")
                estados.append("ok")
            except AcaoNaoAutorizada:
                estados.append("bloqueado")
        threads = [threading.Thread(target=operar) for _ in range(8)]
        for t in threads: t.start()
        for t in threads: t.join(timeout=3)
        self.assertEqual(1, estados.count("ok"))
        self.assertEqual(7, estados.count("bloqueado"))

    def test_ids_invalidos_nao_executam_antes_da_auditoria(self):
        chamadas = []
        with tempfile.TemporaryDirectory() as tmp:
            audit = RegistroAuditoria(Path(tmp) / "auditoria.jsonl", chave=b"ficticia" * 8)
            orq = OrquestradorParaleloLocal(agentes={"backend": lambda e: chamadas.append(1) or {}},
                criticos={"critico_corretude": lambda s: (True, "ok")})
            with self.assertRaises(ErroDePlano):
                Supervisao(orq, audit).executar([TarefaSupervisionada(Tarefa(
                    "id contendo dados privados", "backend", {}, criticos=("critico_corretude",)))])
            self.assertEqual([], chamadas)

if __name__ == "__main__":
    unittest.main()
