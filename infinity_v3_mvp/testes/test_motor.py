"""Testes com dados fictícios. Nenhuma memória pessoal real é utilizada."""
import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from infinity_v3.motor import MotorMemoria, ErroDeAcesso, ErroDeValidacao


class TestesMotorMemoria(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.motor = MotorMemoria(Path(self.tmp.name) / "memorias.db")

    def tearDown(self):
        self.motor.fechar()
        self.tmp.cleanup()

    def inserir(self, **alteracoes):
        campos = dict(usuario="usuario_a", escopo="projeto:alpha", titulo="Preferência de código",
                      conteudo="Preferir testes automatizados no Python", origem="feedback-validado")
        campos.update(alteracoes)
        return self.motor.registrar(**campos)

    def test_registro_pendente_so_aparece_apos_aprovacao(self):
        ident = self.inserir()
        self.assertEqual([], self.motor.buscar(usuario="usuario_a", escopos=["projeto:alpha"], consulta="Python"))
        self.motor.aprovar(usuario="usuario_a", memoria_id=ident)
        self.assertEqual(ident, self.motor.buscar(usuario="usuario_a", escopos=["projeto:alpha"], consulta="Python")[0]["id"])

    def test_deduplicacao_de_registro(self):
        ident = self.inserir()
        self.assertEqual(ident, self.inserir())
        self.assertEqual(1, self.motor.contar_eventos(usuario="usuario_a"))

    def test_isolamento_entre_usuarios_e_escopos(self):
        ident = self.inserir(aprovado=True)
        self.assertFalse(self.motor.buscar(usuario="usuario_b", escopos=["projeto:alpha"], consulta="Python"))
        self.assertFalse(self.motor.buscar(usuario="usuario_a", escopos=["projeto:beta"], consulta="Python"))
        with self.assertRaises(ErroDeAcesso):
            self.motor.aprovar(usuario="usuario_b", memoria_id=ident)

    def test_correcao_preserva_historico(self):
        velho = self.inserir(aprovado=True)
        novo = self.motor.corrigir(usuario="usuario_a", memoria_id=velho,
                                  conteudo_corrigido="Preferir testes unitários em Python 3.12",
                                  justificativa="Correção explícita")
        self.assertNotEqual(velho, novo)
        resultados = self.motor.buscar(usuario="usuario_a", escopos=["projeto:alpha"], consulta="Python")
        self.assertEqual([novo], [x["id"] for x in resultados])
        self.assertEqual(velho, resultados[0]["substitui"])
        self.assertEqual(3, self.motor.contar_eventos(usuario="usuario_a"))

    def test_remocao_de_busca_apos_arquivar(self):
        ident = self.inserir(aprovado=True)
        self.motor.arquivar(usuario="usuario_a", memoria_id=ident)
        self.assertEqual([], self.motor.buscar(usuario="usuario_a", escopos=["projeto:alpha"], consulta="Python"))

    def test_vencimento(self):
        ontem = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        self.inserir(aprovado=True, valido_ate=ontem)
        self.assertFalse(self.motor.buscar(usuario="usuario_a", escopos=["projeto:alpha"], consulta="Python"))

    def test_segredo_rejeitado(self):
        with self.assertRaises(ErroDeValidacao):
            self.inserir(sensibilidade="segredo")

    def test_tentativa_de_injecao_fts_nao_altera_banco(self):
        self.inserir(aprovado=True)
        self.motor.buscar(usuario="usuario_a", escopos=["projeto:alpha"], consulta='Python" OR *:')
        self.assertEqual(1, len(self.motor.buscar(usuario="usuario_a", escopos=["projeto:alpha"], consulta="Python")))

    def test_injecao_sql_na_identidade_nao_dá_acesso(self):
        self.inserir(aprovado=True)
        self.assertEqual([], self.motor.buscar(usuario="' OR 1=1--", escopos=["projeto:alpha"], consulta="Python"))

    def test_fonte_e_id_presentes_no_retorno(self):
        self.inserir(aprovado=True)
        x = self.motor.buscar(usuario="usuario_a", escopos=["projeto:alpha"], consulta="Python")[0]
        self.assertEqual("feedback-validado", x["origem"])
        self.assertTrue(x["id"])


if __name__ == "__main__":
    unittest.main()
