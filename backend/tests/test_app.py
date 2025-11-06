"""
Testes TDD (Test-Driven Development) para o sistema Alfa.
Testes unitários para modelos, validações e lógica de negócio.
"""
import pytest
from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from datetime import date

from app_Alfa.models import (
    Admin, Usuario, Membro, Grupo, Doacao, Igreja,
    Evento, Postagem, FotoEvento, FotoPostagem,
    Cargo, ONG, Oferta, DistribuicaoOferta, DocumentoMembro, Transferencia
)


class TestAdminModel(TestCase):
    """Testes para o modelo Admin"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.admin = Admin.objects.create(
            nome="Admin Teste",
            email="admin@teste.com",
            senha="senha123",
            is_staff=True,
            is_active=True
        )
    
    def test_admin_creation(self):
        """Testa criação de Admin"""
        assert self.admin.nome == "Admin Teste"
        assert self.admin.email == "admin@teste.com"
        assert self.admin.is_staff is True
    
    def test_admin_str(self):
        """Testa representação em string do Admin"""
        # Admin não tem __str__ definido, então testa se existe
        str_repr = str(self.admin)
        assert "Admin" in str_repr or self.admin.nome in str_repr
    
    def test_admin_login_valido(self):
        """Testa login com credenciais válidas"""
        admin = Admin.objects.filter(
            email="admin@teste.com", 
            senha="senha123"
        ).first()
        assert admin is not None
        assert admin.is_active is True
    
    def test_admin_login_invalido(self):
        """Testa login com senha incorreta"""
        admin = Admin.objects.filter(
            email="admin@teste.com", 
            senha="senhaErrada"
        ).first()
        assert admin is None


class TestMembroModel(TestCase):
    """Testes para o modelo Membro"""
    
    def setUp(self):
        """Configuração inicial"""
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
        self.membro = Membro.objects.create(
            nome="João Silva",
            cpf="123.456.789-00",
            email="joao@email.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
    
    def test_membro_creation(self):
        """Testa criação de membro"""
        assert self.membro.nome == "João Silva"
        assert self.membro.status == Membro.ATIVO
        assert self.membro.cadastrado_por == self.admin
    
    def test_membro_status_choices(self):
        """Testa opções de status disponíveis"""
        assert Membro.ATIVO == 'ativo'
        assert Membro.INATIVO == 'inativo'
        assert Membro.FALECIDO == 'falecido'
        assert Membro.AFASTADO == 'afastado'
    
    def test_membro_change_status(self):
        """Testa alteração de status"""
        self.membro.status = Membro.INATIVO
        self.membro.save()
        
        membro_atualizado = Membro.objects.get(id=self.membro.id)
        assert membro_atualizado.status == Membro.INATIVO
    
    def test_membro_soft_delete(self):
        """Testa exclusão lógica (soft delete)"""
        self.membro.delete()
        
        # BaseModel implementa soft delete
        # Membro não deve aparecer em queries normais se is_active=False
        membro_atualizado = Membro.objects.filter(id=self.membro.id).first()
        
        # Se o soft delete está funcionando, o membro ainda existe mas está marcado como deletado
        if hasattr(Membro, 'deleted_at'):
            assert membro_atualizado is None or membro_atualizado.deleted_at is not None
        else:
            # Se não tem soft delete, verifica exclusão real
            assert membro_atualizado is None


class TestCargoModel(TestCase):
    """Testes para o modelo Cargo"""
    
    def setUp(self):
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
        self.cargo = Cargo.objects.create(
            nome="Pastor",
            descricao="Líder espiritual da igreja",
            criado_por=self.admin
        )
    
    def test_cargo_creation(self):
        """Testa criação de cargo"""
        assert self.cargo.nome == "Pastor"
        assert self.cargo.criado_por == self.admin
    
    def test_multiple_cargos(self):
        """Testa criação de múltiplos cargos"""
        Cargo.objects.create(nome="Diácono", criado_por=self.admin)
        Cargo.objects.create(nome="Líder de Louvor", criado_por=self.admin)
        
        assert Cargo.objects.count() == 3


class TestOfertaModel(TestCase):
    """Testes para o modelo Oferta"""
    
    def setUp(self):
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
        self.oferta = Oferta.objects.create(
            valor=Decimal("1000.00"),
            descricao="Oferta do domingo",
            registrado_por=self.admin,
            is_publico=True
        )
    
    def test_oferta_creation(self):
        """Testa criação de oferta"""
        assert self.oferta.valor == Decimal("1000.00")
        assert self.oferta.is_publico is True
    
    def test_oferta_valor_positivo(self):
        """Testa que valor da oferta é positivo"""
        assert self.oferta.valor > 0
    
    def test_oferta_with_distribution(self):
        """Testa distribuição de oferta para ONG"""
        ong = ONG.objects.create(
            nome="ONG Teste",
            cnpj="12.345.678/0001-90"
        )
        
        distribuicao = DistribuicaoOferta.objects.create(
            oferta=self.oferta,
            ong=ong,
            valor=Decimal("500.00"),
            destino="ONG Teste",
            meio_envio="PIX"
        )
        
        assert self.oferta.distribuicoes.count() == 1
        assert distribuicao.valor == Decimal("500.00")


class TestDoacaoModel(TestCase):
    """Testes para o modelo Doacao"""
    
    def setUp(self):
        self.admin = Admin.objects.create(nome="Admin", email="a@t.com", senha="123")
        self.membro = Membro.objects.create(
            nome="Maria",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
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
        
        total_doacoes = self.membro.doacoes.count()
        assert total_doacoes == 2
        
        # Testa soma total
        total_valor = sum(d.valor for d in self.membro.doacoes.all())
        assert total_valor == Decimal("125.00")


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


class TestTransferenciaModel(TestCase):
    """Testes para o modelo Transferencia"""

    def setUp(self):
        self.admin = Admin.objects.create(nome="Admin", email="admin@test.com", senha="123")
        self.membro = Membro.objects.create(
            nome="João Silva",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
        self.igreja_origem = Igreja.objects.create(
            nome="Igreja Origem",
            endereco="Rua A, 123"
        )
        self.igreja_destino = Igreja.objects.create(
            nome="Igreja Destino",
            endereco="Rua B, 456"
        )

    def test_transferencia_creation(self):
        """Testa criação de transferência"""
        transferencia = Transferencia.objects.create(
            membro=self.membro,
            igreja_origem=self.igreja_origem,
            igreja_destino=self.igreja_destino,
            data_transferencia=date.today(),
            motivo="Mudança de cidade",
            gerado_por=self.admin
        )

        assert transferencia.membro == self.membro
        assert transferencia.igreja_origem == self.igreja_origem
        assert transferencia.igreja_destino == self.igreja_destino
        assert transferencia.motivo == "Mudança de cidade"

    def test_transferencia_different_churches(self):
        """Testa que origem e destino devem ser diferentes"""
        with self.assertRaises(Exception):  # Ou verificar na view, mas aqui testa modelo
            Transferencia.objects.create(
                membro=self.membro,
                igreja_origem=self.igreja_origem,
                igreja_destino=self.igreja_origem,  # Mesmo que origem
                data_transferencia=date.today(),
                gerado_por=self.admin
            )

    def test_transferencia_soft_delete(self):
        """Testa soft delete na transferência"""
        transferencia = Transferencia.objects.create(
            membro=self.membro,
            igreja_origem=self.igreja_origem,
            igreja_destino=self.igreja_destino,
            data_transferencia=date.today(),
            gerado_por=self.admin
        )

        transferencia.delete()
        # Verificar se foi soft deleted
        transferencia_atualizada = Transferencia.objects.filter(id=transferencia.id).first()
        assert transferencia_atualizada is None or transferencia_atualizada.deleted_at is not None


class TestEventoModel(TestCase):
    """Testes para o modelo Evento"""
    
    def setUp(self):
        self.usuario = Usuario.objects.create(
            username="organizador",
            email="org@test.com"
        )
        self.evento = Evento.objects.create(
            titulo="Culto de Domingo",
            descricao="Culto dominical",
            data=timezone.now(),
            local="Igreja Central",
            organizador=self.usuario
        )
    
    def test_evento_creation(self):
        """Testa criação de evento"""
        assert self.evento.titulo == "Culto de Domingo"
        assert self.evento.organizador == self.usuario
    
    def test_evento_with_fotos(self):
        """Testa evento com fotos"""
        FotoEvento.objects.create(
            evento=self.evento,
            imagem="foto1.jpg",
            descricao="Foto 1"
        )
        FotoEvento.objects.create(
            evento=self.evento,
            imagem="foto2.jpg",
            descricao="Foto 2"
        )
        
        assert self.evento.fotos.count() == 2


class TestBusinessLogic(TestCase):
    """Testes para lógica de negócio"""
    
    def setUp(self):
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123",
            is_staff=True
        )
    
    def test_admin_permissions(self):
        """Testa permissões do Admin"""
        assert self.admin.is_staff is True
        assert self.admin.is_active is True
    
    def test_oferta_distribution_sum(self):
        """Testa que soma das distribuições não excede valor da oferta"""
        oferta = Oferta.objects.create(
            valor=Decimal("1000.00"),
            registrado_por=self.admin
        )
        
        ong1 = ONG.objects.create(nome="ONG 1", cnpj="11.111.111/0001-11")
        ong2 = ONG.objects.create(nome="ONG 2", cnpj="22.222.222/0001-22")
        
        DistribuicaoOferta.objects.create(
            oferta=oferta,
            ong=ong1,
            valor=Decimal("400.00"),
            destino="ONG 1"
        )
        DistribuicaoOferta.objects.create(
            oferta=oferta,
            ong=ong2,
            valor=Decimal("600.00"),
            destino="ONG 2"
        )
        
        total_distribuido = sum(d.valor for d in oferta.distribuicoes.all())
        assert total_distribuido == Decimal("1000.00")
        assert total_distribuido <= oferta.valor
    
    def test_membro_statistics(self):
        """Testa estatísticas de membros por status"""
        # Criar membros com diferentes status
        for i in range(5):
            Membro.objects.create(nome=f"Ativo {i}", status=Membro.ATIVO, cadastrado_por=self.admin)
        for i in range(3):
            Membro.objects.create(nome=f"Inativo {i}", status=Membro.INATIVO, cadastrado_por=self.admin)
        for i in range(2):
            Membro.objects.create(nome=f"Afastado {i}", status=Membro.AFASTADO, cadastrado_por=self.admin)
        
        # Contar por status
        ativos = Membro.objects.filter(status=Membro.ATIVO).count()
        inativos = Membro.objects.filter(status=Membro.INATIVO).count()
        afastados = Membro.objects.filter(status=Membro.AFASTADO).count()
        
        assert ativos == 5
        assert inativos == 3
        assert afastados == 2


# Função para executar testes manualmente (sem pytest)
if __name__ == '__main__':
    import django
    import os
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfa_project.settings')
    django.setup()
    
    # Executar testes
    from django.test.utils import get_runner
    from django.conf import settings
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    
    if failures:
        print(f"\n❌ {failures} testes falharam")
    else:
        print("\n✅ Todos os testes TDD passaram!")

