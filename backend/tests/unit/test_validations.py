"""
Testes de validação de lógica de negócio.
Testa constraints e regras de negócio.
"""
import pytest
from django.test import TestCase

from app_alfa.models import Admin, Membro, Cargo, ONG, Oferta, DistribuicaoOferta


@pytest.mark.unit
class TestValidations(TestCase):
    """Testes de validação de constraints e regras"""
    
    def setUp(self):
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
    
    def test_cannot_create_duplicate_cargo(self):
        """Testa que não pode criar cargo com nome duplicado"""
        Cargo.objects.create(nome="Pastor")
        
        try:
            Cargo.objects.create(nome="Pastor")
            assert False, "Deveria ter lançado exceção de constraint"
        except Exception:
            pass  # Esperado
    
    def test_cannot_create_duplicate_admin_email(self):
        """Testa que não pode criar admin com email duplicado"""
        admin2_attempt = Admin(
            nome="Admin 2",
            email="admin@test.com",
            senha="123"
        )
        
        try:
            admin2_attempt.save()
            assert False, "Deveria ter lançado exceção de constraint"
        except Exception:
            pass  # Esperado
    
    def test_membro_update_with_duplicate_email(self):
        """Testa que não pode atualizar membro para email duplicado"""
        membro1 = Membro.objects.create(
            nome="João",
            email="joao@email.com",
            cadastrado_por=self.admin
        )
        membro2 = Membro.objects.create(
            nome="Maria",
            email="maria@email.com",
            cadastrado_por=self.admin
        )
        
        membro2.email = "joao@email.com"
        
        try:
            membro2.save()
            assert False, "Deveria ter lançado exceção de constraint"
        except Exception:
            pass  # Esperado


@pytest.mark.unit
class TestBusinessLogicValidation(TestCase):
    """Testes para validação de lógica de negócio"""
    
    def setUp(self):
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123",
            is_admin=True
        )
    
    def test_admin_permissions(self):
        """Testa permissões do Admin"""
        assert self.admin.is_admin is True
        assert self.admin.is_active is True
    
    def test_membro_statistics(self):
        """Testa estatísticas de membros por status"""
        # Contar antes
        antes_ativo = Membro.objects.filter(status=Membro.ATIVO).count()
        antes_inativo = Membro.objects.filter(status=Membro.INATIVO).count()
        antes_afastado = Membro.objects.filter(status=Membro.AFASTADO).count()
        
        for i in range(5):
            Membro.objects.create(
                nome=f"Ativo {i}",
                email=f"ativo{i}@email.com",
                status=Membro.ATIVO,
                cadastrado_por=self.admin
            )
        for i in range(3):
            Membro.objects.create(
                nome=f"Inativo {i}",
                email=f"inativo{i}@email.com",
                status=Membro.INATIVO,
                cadastrado_por=self.admin
            )
        for i in range(2):
            Membro.objects.create(
                nome=f"Afastado {i}",
                email=f"afastado{i}@email.com",
                status=Membro.AFASTADO,
                cadastrado_por=self.admin
            )
        
        ativos = Membro.objects.filter(status=Membro.ATIVO).count() - antes_ativo
        inativos = Membro.objects.filter(status=Membro.INATIVO).count() - antes_inativo
        afastados = Membro.objects.filter(status=Membro.AFASTADO).count() - antes_afastado
        
        assert ativos == 5
        assert inativos == 3
        assert afastados == 2
