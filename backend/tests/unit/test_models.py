"""
Testes unitários para os modelos Django.
Testes de criação, leitura e validação básica de modelos.
"""
import pytest
from django.test import TestCase
from decimal import Decimal
from django.utils import timezone

from app_alfa.models import (
    Admin, Membro, Cargo, Oferta, Doacao, 
    DocumentoMembro, Usuario, ONG, Transacao, Evento, FotoEvento
)


@pytest.mark.unit
class TestAdminModel(TestCase):
    """Testes para o modelo Admin"""
    
    def test_admin_creation(self):
        """Testa criação de Admin"""
        admin = Admin.objects.create(
            nome="Admin Teste",
            email="admin@teste.com",
            senha="senha123",
            is_admin=True
        )
        assert admin.nome == "Admin Teste"
        assert admin.email == "admin@teste.com"
        assert admin.is_admin is True
    
    def test_admin_login_valido(self):
        """Testa login com credenciais válidas"""
        admin_test = Admin.objects.create(
            nome="Test",
            email="test@test.com",
            senha="password123"
        )
        assert admin_test.check_password("password123")
    
    def test_admin_login_invalido(self):
        """Testa login com senha incorreta"""
        admin_test = Admin.objects.create(
            nome="Test",
            email="test2@test.com",
            senha="password123"
        )
        assert not admin_test.check_password("senhaErrada")


@pytest.mark.unit
class TestMembroModel(TestCase):
    """Testes para o modelo Membro"""
    
    def setUp(self):
        """Configuração inicial"""
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
    
    def test_membro_creation(self):
        """Testa criação de membro"""
        membro = Membro.objects.create(
            nome="João Silva",
            cpf="123.456.789-00",
            email="joao@email.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
        assert membro.nome == "João Silva"
        assert membro.status == Membro.ATIVO
        assert membro.cadastrado_por == self.admin
    
    def test_membro_status_choices(self):
        """Testa opções de status disponíveis"""
        assert Membro.ATIVO == 'ativo'
        assert Membro.INATIVO == 'inativo'
        assert Membro.FALECIDO == 'falecido'
        assert Membro.AFASTADO == 'afastado'
    
    def test_membro_change_status(self):
        """Testa alteração de status"""
        membro = Membro.objects.create(
            nome="João Silva",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
        membro.status = Membro.INATIVO
        membro.save()
        
        membro_atualizado = Membro.objects.get(id=membro.id)
        assert membro_atualizado.status == Membro.INATIVO


@pytest.mark.unit
class TestCargoModel(TestCase):
    """Testes para o modelo Cargo"""
    
    def test_cargo_creation(self):
        """Testa criação de cargo"""
        cargo = Cargo.objects.create(
            nome="Pastor",
            descricao="Líder espiritual da igreja"
        )
        assert cargo.nome == "Pastor"
        assert cargo.descricao is not None
    
    def test_multiple_cargos(self):
        """Testa criação de múltiplos cargos"""
        Cargo.objects.create(nome="Diácono", descricao="Auxiliar")
        Cargo.objects.create(nome="Líder de Louvor", descricao="Louvor")
        Cargo.objects.create(nome="Pastor", descricao="Líder")
        
        assert Cargo.objects.count() == 3


@pytest.mark.unit
class TestOfertaModel(TestCase):
    """Testes para o modelo Oferta"""
    
    def setUp(self):
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
    
    def test_oferta_creation(self):
        """Testa criação de oferta"""
        oferta = Oferta.objects.create(
            valor=Decimal("1000.00"),
            descricao="Oferta do domingo",
            registrado_por=self.admin,
            is_publico=True
        )
        assert oferta.valor == Decimal("1000.00")
        assert oferta.is_publico is True
    
    def test_oferta_valor_positivo(self):
        """Testa que valor da oferta é positivo"""
        oferta = Oferta.objects.create(
            valor=Decimal("1000.00"),
            registrado_por=self.admin
        )
        assert oferta.valor > 0
    
    def test_oferta_with_distribution(self):
        """Testa distribuição de oferta para ONG"""
        from app_alfa.models import DistribuicaoOferta
        
        oferta = Oferta.objects.create(
            valor=Decimal("1000.00"),
            registrado_por=self.admin
        )
        
        ong = ONG.objects.create(
            nome="ONG Teste",
            cnpj="12.345.678/0001-90"
        )
        
        distribuicao = DistribuicaoOferta.objects.create(
            oferta=oferta,
            ong=ong,
            valor=Decimal("500.00"),
            destino="ONG Teste",
            meio_envio="PIX"
        )
        
        assert oferta.distribuicoes.count() == 1
        assert distribuicao.valor == Decimal("500.00")


@pytest.mark.unit
class TestDoacaoModel(TestCase):
    """Testes para o modelo Doacao"""
    
    def setUp(self):
        self.admin = Admin.objects.create(nome="Admin", email="a@t.com", senha="123")
        self.membro = Membro.objects.create(
            nome="Maria",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
        from app_alfa.models import Grupo
        self.grupo = Grupo.objects.create(
            nome="Missões",
            descricao="Grupo de missões"
        )
    
    def test_doacao_creation(self):
        """Testa criação de doação"""
        doacao = Doacao.objects.create(
            membro=self.membro,
            grupo=self.grupo,
            valor=Decimal("100.00"),
            tipo="doacao"
        )
        
        assert doacao.membro == self.membro
        assert doacao.valor == Decimal("100.00")
    
    def test_multiple_doacoes(self):
        """Testa múltiplas doações de um membro"""
        Doacao.objects.create(membro=self.membro, grupo=self.grupo, valor=Decimal("50.00"))
        Doacao.objects.create(membro=self.membro, grupo=self.grupo, valor=Decimal("75.00"))
        
        assert self.membro.doacoes.count() == 2
        total_valor = sum(d.valor for d in self.membro.doacoes.all())
        assert total_valor == Decimal("125.00")


@pytest.mark.unit
class TestDocumentoMembroModel(TestCase):
    """Testes para o modelo DocumentoMembro"""
    
    def setUp(self):
        self.admin = Admin.objects.create(nome="Admin", email="a@t.com", senha="123")
        self.membro = Membro.objects.create(
            nome="Carlos",
            cadastrado_por=self.admin
        )
    
    def test_cartao_membro(self):
        """Testa geração de cartão de membro"""
        documento = DocumentoMembro.objects.create(
            membro=self.membro,
            tipo=DocumentoMembro.CARTAO_MEMBRO,
            gerado_por=self.admin
        )
        
        assert documento.tipo == DocumentoMembro.CARTAO_MEMBRO
        assert documento.membro == self.membro
    
    def test_transferencia(self):
        """Testa geração de documento de transferência"""
        documento = DocumentoMembro.objects.create(
            membro=self.membro,
            tipo=DocumentoMembro.TRANSFERENCIA,
            gerado_por=self.admin
        )
        
        assert documento.tipo == DocumentoMembro.TRANSFERENCIA
    
    def test_multiple_documentos(self):
        """Testa múltiplos documentos por membro"""
        DocumentoMembro.objects.create(
            membro=self.membro,
            tipo=DocumentoMembro.CARTAO_MEMBRO,
            gerado_por=self.admin
        )
        DocumentoMembro.objects.create(
            membro=self.membro,
            tipo=DocumentoMembro.REGISTRO,
            gerado_por=self.admin
        )
        
        assert self.membro.documentos.count() == 2


@pytest.mark.unit
class TestEventoModel(TestCase):
    """Testes para o modelo Evento"""
    
    def setUp(self):
        self.usuario = Usuario.objects.create(
            username="organizador",
            email="org@test.com"
        )
    
    def test_evento_creation(self):
        """Testa criação de evento"""
        evento = Evento.objects.create(
            titulo="Culto de Domingo",
            descricao="Culto dominical",
            data=timezone.now(),
            local="Igreja Central",
            organizador=self.usuario
        )
        assert evento.titulo == "Culto de Domingo"
        assert evento.organizador == self.usuario
    
    def test_evento_with_fotos(self):
        """Testa evento com fotos"""
        evento = Evento.objects.create(
            titulo="Culto",
            descricao="Culto",
            data=timezone.now(),
            local="Igreja",
            organizador=self.usuario
        )
        
        FotoEvento.objects.create(
            evento=evento,
            imagem="foto1.jpg",
            descricao="Foto 1"
        )
        FotoEvento.objects.create(
            evento=evento,
            imagem="foto2.jpg",
            descricao="Foto 2"
        )
        
        assert evento.fotos.count() == 2


@pytest.mark.unit
class TestTransacaoModel(TestCase):
    """Testes para o modelo Transacao"""
    
    def setUp(self):
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
    
    def test_transacao_entrada_creation(self):
        """Testa criação de transação de entrada"""
        transacao = Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Dízimo",
            valor=Decimal("500.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        
        assert transacao.tipo == Transacao.ENTRADA
        assert transacao.valor == Decimal("500.00")
        assert transacao.categoria == "Dízimo"
    
    def test_transacao_saida_creation(self):
        """Testa criação de transação de saída"""
        transacao = Transacao.objects.create(
            tipo=Transacao.SAIDA,
            categoria="Despesa",
            valor=Decimal("100.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        
        assert transacao.tipo == Transacao.SAIDA
        assert transacao.valor == Decimal("100.00")
    
    def test_transacao_valor_positivo(self):
        """Testa que valor é positivo"""
        transacao = Transacao.objects.create(
            tipo=Transacao.ENTRADA,
            categoria="Dízimo",
            valor=Decimal("500.00"),
            data=timezone.now().date(),
            registrado_por=self.admin
        )
        
        assert transacao.valor > 0
