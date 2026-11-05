import os
import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from infinity_v3.motor import MotorMemoria, ErroDeValidacao, ErroDeAcesso
from infinity_v3.sessao import SessaoMemoria
from infinity_v3.seguranca import analisar_riscos


class TesteSeguranca(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "seguro.db"
        self.motor = MotorMemoria(self.db)

    def tearDown(self):
        self.motor.fechar()
        self.tmp.cleanup()

    def gravar(self, **kwargs):
        campos = dict(usuario="uA", escopo="alpha", titulo="Regras", conteudo="Usar revisão e testes automatizados",
                     origem="comentario-confirmado", aprovado=True)
        campos.update(kwargs)
        return self.motor.registrar(**campos)

    def test_seguro_para_senha_credenciais_e_cpf(self):
        for dado in ("password: abcdefghij", "ghp_" + "A" * 40, "123.456.789-09"):
            with self.subTest(dado=dado[:4]):
                with self.assertRaises(ErroDeValidacao) as erro:
                    self.gravar(conteudo="Token de teste " + dado)
                self.assertNotIn(dado, str(erro.exception))
        self.assertTrue(analisar_riscos("AKIA"+"A"*16))

    def test_correcao_bloqueia_segredo(self):
        ident = self.gravar()
        with self.assertRaises(ErroDeValidacao):
            self.motor.corrigir(usuario="uA", memoria_id=ident, conteudo_corrigido="senha: abcdefghijkl", justificativa="ok")

    def test_sessao_aprovacao_nao_pula_sem_permissao(self):
        s = SessaoMemoria(self.motor, usuario="uA", escopos=frozenset({"alpha"}), pode_escrever=True)
        ident = s.registrar(escopo="alpha", titulo="Outra regra", conteudo="Revisar todos os artefatos",
                          origem="usuario", aprovado=True, usuario="uB")
        self.assertEqual([], s.buscar(consulta="artefatos"))
        s.aprovar(memoria_id=ident)
        self.assertEqual(1, len(s.buscar(consulta="artefatos")))
        self.assertEqual([], self.motor.buscar(usuario="uB", escopos=["alpha"], consulta="artefatos"))

    def test_sessao_nao_corrige_escopo_alheio(self):
        ident = self.gravar(escopo="beta")
        s = SessaoMemoria(self.motor, "uA", frozenset({"alpha"}), pode_escrever=True, pode_excluir=True)
        with self.assertRaises(ErroDeAcesso):
            s.corrigir(memoria_id=ident, conteudo_corrigido="Outra versão", justificativa="teste")
        with self.assertRaises(ErroDeAcesso):
            s.excluir(memoria_id=ident)
        with self.assertRaises(ErroDeAcesso):
            s.buscar(consulta="testes", escopos=["beta"])

    def test_exclusao_sem_autorizacao_bloqueada(self):
        ident = self.gravar()
        s = SessaoMemoria(self.motor, "uA", frozenset({"alpha"}))
        with self.assertRaises(ErroDeAcesso):
            s.excluir(memoria_id=ident)

    def test_exclusao_local_remove_indice_e_auditoria(self):
        ident = self.gravar()
        s = SessaoMemoria(self.motor, "uA", frozenset({"alpha"}), pode_excluir=True)
        s.excluir(memoria_id=ident)
        self.assertEqual([], s.buscar(consulta="testes"))
        self.assertEqual(0, self.motor.contar_eventos(usuario="uA"))

    def test_esquecimento_nao_apaga_outras_identidades_e_escopos(self):
        self.gravar()
        self.gravar(usuario="uB")
        self.gravar(escopo="beta")
        s = SessaoMemoria(self.motor, "uA", frozenset({"alpha"}), pode_excluir=True)
        with self.assertRaises(ErroDeAcesso):
            s.excluir_meus_dados(confirmacao="sim")
        self.assertEqual(1, s.excluir_meus_dados(confirmacao="EXCLUIR TODOS OS MEUS DADOS"))
        self.assertEqual([], s.buscar(consulta="testes"))
        self.assertEqual(1, len(self.motor.buscar(usuario="uB", escopos=["alpha"], consulta="testes")))
        self.assertEqual(1, len(self.motor.buscar(usuario="uA", escopos=["beta"], consulta="testes")))

    def test_justificativa_hash_na_auditoria(self):
        ident = self.gravar()
        novo = self.motor.corrigir(usuario="uA", memoria_id=ident,
            conteudo_corrigido="Usar revisão de pares e testes automatizados", justificativa="feedback de teste")
        linha = self.motor.conexao.execute("SELECT justificativa_hash FROM eventos WHERE memoria_id=? AND acao='correcao_confirmada'",(novo,)).fetchone()
        self.assertEqual(64, len(linha[0]))
        self.assertNotIn("feedback de teste", linha[0])

    def test_validade_em_fusos_normalizada(self):
        # Mesmo instante em +09:00 deve vencer em relação à consulta UTC.
        ontem = (datetime.now(timezone(timedelta(hours=9))) - timedelta(days=1)).isoformat()
        self.gravar(valido_ate=ontem)
        self.assertEqual([], self.motor.buscar(usuario="uA", escopos=["alpha"], consulta="testes"))

    @unittest.skipUnless(os.name == "posix", "Permissões POSIX")
    def test_arquivo_local_posix_somente_dono(self):
        self.assertEqual(0o600, self.db.stat().st_mode & 0o777)

    def test_limite_escopos_defensivo(self):
        self.gravar()
        with self.assertRaises(ErroDeValidacao):
            self.motor.buscar(usuario="uA", escopos=[str(x) for x in range(40)], consulta="testes")

if __name__ == "__main__":
    unittest.main()
