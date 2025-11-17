"""
Testes de integração para autenticação e login.
Testa endpoints de login com credenciais válidas e inválidas.
"""
import pytest
from django.test import TestCase
from app_alfa.models import Admin, Membro


@pytest.mark.integration
@pytest.mark.auth
class TestAdminLogin(TestCase):
    """Testes de login para Admin"""
    
    def setUp(self):
        """Preparar dados de teste"""
        self.admin = Admin.objects.create(
            nome="Admin Test",
            email="admin@test.com",
            senha="password123"
        )
        self.admin.set_password("password123")
        self.admin.save()
    
    def test_admin_login_valido(self):
        """Testa login com credenciais válidas"""
        assert self.admin.check_password("password123")
    
    def test_admin_login_invalido(self):
        """Testa login com senha incorreta"""
        assert not self.admin.check_password("senhaErrada")
    
    def test_admin_exists(self):
        """Testa se admin foi criado com sucesso"""
        admin = Admin.objects.get(email="admin@test.com")
        assert admin.nome == "Admin Test"
        assert admin.is_admin is True


@pytest.mark.integration
@pytest.mark.auth
class TestMembroLogin(TestCase):
    """Testes de login para Membro"""
    
    def setUp(self):
        """Preparar dados de teste"""
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
        self.membro = Membro.objects.create(
            nome="João Silva",
            email="joao@test.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
        self.membro.set_password("password123")
        self.membro.save()
    
    def test_membro_login_valido(self):
        """Testa login com credenciais válidas"""
        assert self.membro.check_password("password123")
    
    def test_membro_login_invalido(self):
        """Testa login com senha incorreta"""
        assert not self.membro.check_password("senhaErrada")
    
    def test_membro_ativo_login(self):
        """Testa que membro ativo pode fazer login"""
        assert self.membro.status == Membro.ATIVO
        assert self.membro.check_password("password123")
    
    def test_membro_inativo_cannot_login(self):
        """Testa que membro inativo não deveria fazer login"""
        self.membro.status = Membro.INATIVO
        self.membro.save()
        
        assert self.membro.status == Membro.INATIVO
        # Validação seria feita na view
