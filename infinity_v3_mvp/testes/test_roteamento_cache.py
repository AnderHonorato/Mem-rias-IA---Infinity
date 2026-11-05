import unittest
from infinity_v3.roteador import Modelo, Politica, Roteador, NenhumModeloElegivel
from infinity_v3.cache import CachePublico


class TesteRoteador(unittest.TestCase):
    def setUp(self):
        self.r = Roteador([
            Modelo("local-rapido", "rapido", True, True, 0, 50),
            Modelo("local-profundo", "profundo", True, True, 0, 300),
            Modelo("nuvem-rapido", "rapido", True, False, 0.02, 30),
            Modelo("nuvem-profundo", "profundo", False, False, 0.5, 80),
        ])

    def test_rapido_simples(self):
        x = self.r.escolher("Qual é a saudação?", Politica())
        self.assertEqual("local-rapido", x.modelo)

    def test_profundo_para_seguranca(self):
        x = self.r.escolher("Faça auditoria de segurança", Politica())
        self.assertEqual("local-profundo", x.modelo)

    def test_nao_envia_sigilo_para_nuvem(self):
        x = self.r.escolher("uma pergunta simples", Politica(permite_nuvem=True, permite_pago=True, teto_estimado=10), sigiloso=True)
        self.assertTrue(x.modelo.startswith("local"))

    def test_recusa_nao_conectado(self):
        with self.assertRaises(NenhumModeloElegivel):
            self.r.escolher("auditando", Politica(permite_nuvem=True, permite_pago=True, teto_estimado=10), preferido="nuvem-profundo")

    def test_limite_custo_e_consentimento(self):
        r = Roteador([Modelo("remoto", "rapido", True, False, 0.1, 1)])
        with self.assertRaises(NenhumModeloElegivel):
            r.escolher("oi", Politica(permite_nuvem=True))
        with self.assertRaises(NenhumModeloElegivel):
            r.escolher("oi", Politica(permite_nuvem=True, permite_pago=True, teto_estimado=0.01))
        self.assertEqual("remoto", r.escolher("oi", Politica(permite_nuvem=True, permite_pago=True, teto_estimado=0.5)).modelo)

    def test_preferido_nao_permitido_sem_nuvem(self):
        with self.assertRaises(NenhumModeloElegivel):
            self.r.escolher("oi", Politica(), preferido="nuvem-rapido")


class TesteCache(unittest.TestCase):
    def setUp(self):
        self.tempo = 0
        self.cache = CachePublico(capacidade=2, ttl_segundos=10, relogio=lambda: self.tempo)

    def test_ttl_e_invalida(self):
        self.cache.guardar("a", 10, sensibilidade="publica")
        self.assertEqual(10, self.cache.obter("a", sensibilidade="publica"))
        self.tempo = 11
        self.assertIsNone(self.cache.obter("a", sensibilidade="publica"))

    def test_somente_publico(self):
        self.assertFalse(self.cache.guardar("sem-classe", "dado potencialmente privado"))
        self.assertIsNone(self.cache.obter("sem-classe"))
        self.assertFalse(self.cache.guardar("segredo", "privado", sensibilidade="pessoal"))
        self.assertIsNone(self.cache.obter("segredo", sensibilidade="pessoal"))

    def test_evita_objeto_compartilhado_mutavel(self):
        entrada = ["a"]
        self.cache.guardar("k", entrada, sensibilidade="publica")
        entrada.append("b")
        saida = self.cache.obter("k", sensibilidade="publica")
        self.assertEqual(["a"], saida)
        saida.append("c")
        self.assertEqual(["a"], self.cache.obter("k", sensibilidade="publica"))

    def test_lru(self):
        self.cache.guardar("a", 1, sensibilidade="publica")
        self.cache.guardar("b", 2, sensibilidade="publica")
        self.cache.obter("a", sensibilidade="publica")
        self.cache.guardar("c", 3, sensibilidade="publica")
        self.assertIsNone(self.cache.obter("b", sensibilidade="publica"))
        self.assertEqual(1, self.cache.obter("a", sensibilidade="publica"))

    def test_chave_tem_versao_da_fonte(self):
        k1 = self.cache.chave(consulta="oi", escopo="global", revisao_fonte="a")
        k2 = self.cache.chave(consulta="oi", escopo="global", revisao_fonte="b")
        self.assertNotEqual(k1, k2)
        self.assertNotIn("oi", k1)

if __name__ == "__main__":
    unittest.main()
