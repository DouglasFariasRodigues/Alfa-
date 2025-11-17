"""
Testes de integração para registro e gerenciamento de membros.
"""
import pytest
from django.test import TestCase
from app_alfa.models import Admin, Membro


@pytest.mark.integration
class TestRegisterMembros(TestCase):
    """Testes para registro de membros"""
    
    def setUp(self):
        """Preparar dados de teste"""
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
    
    def test_register_membro(self):
        """Testa registro de um novo membro"""
        membro = Membro.objects.create(
            nome="João Silva",
            email="joao@test.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
        
        assert membro.nome == "João Silva"
        assert membro.email == "joao@test.com"
        assert membro.cadastrado_por == self.admin
    
    def test_register_multiplos_membros(self):
        """Testa registro de múltiplos membros"""
        count_inicial = Membro.objects.count()
        
        for i in range(5):
            Membro.objects.create(
                nome=f"Membro {i}",
                email=f"membro{i}@test.com",
                status=Membro.ATIVO,
                cadastrado_por=self.admin
            )
        
        count_final = Membro.objects.count()
        assert count_final - count_inicial == 5


@pytest.mark.integration
class TestManageMembersStatus(TestCase):
    """Testes para gerenciamento de status de membros"""
    
    def setUp(self):
        """Preparar dados de teste"""
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
        self.membro = Membro.objects.create(
            nome="João",
            email="joao@test.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
    
    def test_membro_change_status_to_inactive(self):
        """Testa mudança de status para inativo"""
        self.membro.status = Membro.INATIVO
        self.membro.save()
        
        membro_atualizado = Membro.objects.get(id=self.membro.id)
        assert membro_atualizado.status == Membro.INATIVO
    
    def test_membro_change_status_to_falecido(self):
        """Testa mudança de status para falecido"""
        self.membro.status = Membro.FALECIDO
        self.membro.save()
        
        membro_atualizado = Membro.objects.get(id=self.membro.id)
        assert membro_atualizado.status == Membro.FALECIDO
    
    def test_membro_change_status_to_afastado(self):
        """Testa mudança de status para afastado"""
        self.membro.status = Membro.AFASTADO
        self.membro.save()
        
        membro_atualizado = Membro.objects.get(id=self.membro.id)
        assert membro_atualizado.status == Membro.AFASTADO
    
    def test_membro_return_to_ativo(self):
        """Testa mudança de status de volta para ativo"""
        self.membro.status = Membro.INATIVO
        self.membro.save()
        
        self.membro.status = Membro.ATIVO
        self.membro.save()
        
        membro_atualizado = Membro.objects.get(id=self.membro.id)
        assert membro_atualizado.status == Membro.ATIVO
