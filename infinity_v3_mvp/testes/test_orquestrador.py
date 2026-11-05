import unittest
from infinity_v3.orquestrador import OrquestradorLocal, Tarefa, ErroDePlano


class TestesOrquestrador(unittest.TestCase):
    def setUp(self):
        self.orq = OrquestradorLocal(
            agentes={
                "pesquisador": lambda entrada: {"relatorio": entrada["tema"]},
                "implementador": lambda entrada: {"codigo": entrada["codigo"]},
            },
            criticos={
                "critico_conteudo": lambda saida: (bool(saida), "conteúdo conferido"),
                "critico_codigo": lambda saida: ("codigo" not in saida or "seguro" in saida["codigo"], "código revisado"),
            },
        )

    def test_agentes_e_criticos_executam(self):
        r = self.orq.executar([
            Tarefa("A", "pesquisador", {"tema": "memória FTS5"}, criticos=("critico_conteudo",)),
            Tarefa("B", "implementador", {"codigo": "seguro"}, depende_de=("A",),
                   criticos=("critico_conteudo", "critico_codigo")),
        ])
        self.assertEqual(["aprovada", "aprovada"], [x.estado for x in r])
        self.assertEqual(2, len(r[1].pareceres))

    def test_critico_reprova_e_dependente_bloqueia(self):
        r = self.orq.executar([
            Tarefa("B", "implementador", {"codigo": "seguro"}, depende_de=("A",), criticos=("critico_codigo",)),
            Tarefa("A", "implementador", {"codigo": "sem validação"}, criticos=("critico_codigo",)),
        ])
        self.assertEqual("reprovada", r[1].estado)
        self.assertEqual("bloqueada", r[0].estado)

    def test_ciclo_falha_explicitamente(self):
        with self.assertRaises(ErroDePlano):
            self.orq.executar([
                Tarefa("A", "pesquisador", {}, depende_de=("B",), criticos=("critico_conteudo",)),
                Tarefa("B", "pesquisador", {}, depende_de=("A",), criticos=("critico_conteudo",)),
            ])

    def test_nao_executa_sem_critico(self):
        with self.assertRaises(ErroDePlano):
            self.orq.executar([Tarefa("A", "pesquisador", {"tema": "teste"})])

    def test_agente_inexistente_nao_finge_execucao(self):
        with self.assertRaises(ErroDePlano):
            self.orq.executar([Tarefa("A", "llm_desconhecido", {}, criticos=("critico_conteudo",))])


if __name__ == "__main__":
    unittest.main()
