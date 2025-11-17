"""
Testes de integração para papéis e cargos.
Valida permissões e atribuições de cargos aos membros.
"""
import pytest
from django.test import TestCase

from app_alfa.models import Admin, Membro, Cargo, Usuario


@pytest.mark.integration
@pytest.mark.permissions
class TestCargoIntegration(TestCase):
    """Testes de integração para atribuição de cargos"""
    
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
    
    def test_assign_cargo_to_membro(self):
        """Testa atribuição de cargo a um membro"""
        cargo = Cargo.objects.create(
            nome="Pastor",
            descricao="Líder espiritual",
            pode_gerenciar_membros=True,
            pode_gerenciar_financas=True
        )
        
        self.membro.cargo = cargo
        self.membro.save()
        
        membro_atualizado = Membro.objects.get(id=self.membro.id)
        assert membro_atualizado.cargo == cargo
    
    def test_change_membro_cargo(self):
        """Testa mudança de cargo de um membro"""
        cargo1 = Cargo.objects.create(
            nome="Diácono",
            descricao="Assistente"
        )
        
        cargo2 = Cargo.objects.create(
            nome="Tesoureiro",
            descricao="Finança"
        )
        
        self.membro.cargo = cargo1
        self.membro.save()
        assert self.membro.cargo == cargo1
        
        self.membro.cargo = cargo2
        self.membro.save()
        
        membro_atualizado = Membro.objects.get(id=self.membro.id)
        assert membro_atualizado.cargo == cargo2
    
    def test_remove_cargo_from_membro(self):
        """Testa remoção de cargo de um membro"""
        cargo = Cargo.objects.create(
            nome="Diácono",
            descricao="Assistente"
        )
        
        self.membro.cargo = cargo
        self.membro.save()
        assert self.membro.cargo == cargo
        
        self.membro.cargo = None
        self.membro.save()
        
        membro_atualizado = Membro.objects.get(id=self.membro.id)
        assert membro_atualizado.cargo is None


@pytest.mark.integration
@pytest.mark.permissions
class TestCargoPermissions(TestCase):
    """Testes de integração para permissões por cargo"""
    
    def setUp(self):
        """Preparar dados de teste"""
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
    
    def test_cargo_with_all_permissions(self):
        """Testa cargo com todas as permissões habilitadas"""
        cargo_admin = Cargo.objects.create(
            nome="Administrador",
            descricao="Controle total",
            pode_registrar_dizimos=True,
            pode_registrar_ofertas=True,
            pode_gerenciar_membros=True,
            pode_gerenciar_eventos=True,
            pode_gerenciar_financas=True,
            pode_gerenciar_cargos=True,
            pode_gerenciar_documentos=True,
            pode_visualizar_relatorios=True
        )
        
        # Verificar que todas as permissões estão habilitadas
        assert cargo_admin.pode_gerenciar_membros is True
        assert cargo_admin.pode_gerenciar_financas is True
        assert cargo_admin.pode_registrar_ofertas is True
        assert cargo_admin.pode_gerenciar_cargos is True
        assert cargo_admin.pode_gerenciar_eventos is True
        assert cargo_admin.pode_visualizar_relatorios is True
        assert cargo_admin.pode_registrar_dizimos is True
    
    def test_cargo_with_limited_permissions(self):
        """Testa cargo com permissões limitadas"""
        cargo_membro = Cargo.objects.create(
            nome="Membro Comum",
            descricao="Permissões básicas",
            pode_gerenciar_membros=False,
            pode_gerenciar_financas=False,
            pode_registrar_ofertas=True,
            pode_gerenciar_cargos=False,
            pode_gerenciar_eventos=False,
            pode_visualizar_relatorios=False,
            pode_registrar_dizimos=False
        )
        
        assert cargo_membro.pode_registrar_ofertas is True
        assert cargo_membro.pode_gerenciar_membros is False
        assert cargo_membro.pode_gerenciar_financas is False
    
    def test_membro_inherits_cargo_permissions(self):
        """Testa que membro herda permissões do cargo"""
        cargo = Cargo.objects.create(
            nome="Secretário",
            descricao="Administrativo",
            pode_gerenciar_membros=True,
            pode_registrar_ofertas=True,
            pode_gerenciar_financas=False
        )
        
        membro = Membro.objects.create(
            nome="João",
            email="joao@test.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin,
            cargo=cargo
        )
        
        cargo_atribuido = membro.cargo
        assert cargo_atribuido.pode_gerenciar_membros is True
        assert cargo_atribuido.pode_registrar_ofertas is True
        assert cargo_atribuido.pode_gerenciar_financas is False


@pytest.mark.integration
@pytest.mark.permissions
class TestUsuarioCargoPermissions(TestCase):
    """Testes de permissões para Usuários (staff)"""
    
    def setUp(self):
        """Preparar dados de teste"""
        self.cargo_staff = Cargo.objects.create(
            nome="Staff",
            descricao="Usuário Staff",
            pode_gerenciar_membros=True,
            pode_visualizar_relatorios=True
        )
    
    def test_usuario_with_cargo_permissions(self):
        """Testa usuário com cargo específico"""
        usuario = Usuario.objects.create(
            username="staff_user",
            email="staff@test.com",
            senha="123",
            cargo=self.cargo_staff
        )
        
        assert usuario.cargo == self.cargo_staff
        assert usuario.is_staff is True


