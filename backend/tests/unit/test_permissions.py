"""
Testes para permissões associadas a cargos.
Testa permissões individuais e combinações de permissões.
"""
import pytest
from django.test import TestCase

from app_alfa.models import Admin, Cargo, Usuario


@pytest.mark.unit
@pytest.mark.permissions
class TestCargoPermissions(TestCase):
    """Testes de permissões associadas a cargos"""
    
    def test_cargo_pode_registrar_dizimos(self):
        """Testa permissão para registrar dízimos"""
        cargo = Cargo.objects.create(
            nome="Tesoureiro",
            descricao="Gerencia finanças",
            pode_registrar_dizimos=True
        )
        assert cargo.pode_registrar_dizimos is True
    
    def test_cargo_sem_permissao_registrar_dizimos(self):
        """Testa que cargo sem permissão não tem acesso"""
        cargo = Cargo.objects.create(
            nome="Membro Comum",
            descricao="Membro comum",
            pode_registrar_dizimos=False
        )
        assert cargo.pode_registrar_dizimos is False
    
    def test_cargo_pode_gerenciar_membros(self):
        """Testa permissão para gerenciar membros"""
        cargo = Cargo.objects.create(
            nome="Pastor",
            pode_gerenciar_membros=True
        )
        assert cargo.pode_gerenciar_membros is True
    
    def test_cargo_pode_gerenciar_financas(self):
        """Testa permissão para gerenciar finanças"""
        cargo = Cargo.objects.create(
            nome="Tesoureiro",
            pode_gerenciar_financas=True
        )
        assert cargo.pode_gerenciar_financas is True
    
    def test_cargo_pode_registrar_ofertas(self):
        """Testa permissão para registrar ofertas"""
        cargo = Cargo.objects.create(
            nome="Diácono",
            pode_registrar_ofertas=True
        )
        assert cargo.pode_registrar_ofertas is True
    
    def test_cargo_pode_gerenciar_eventos(self):
        """Testa permissão para gerenciar eventos"""
        cargo = Cargo.objects.create(
            nome="Organizador",
            pode_gerenciar_eventos=True
        )
        assert cargo.pode_gerenciar_eventos is True
    
    def test_cargo_pode_gerenciar_documentos(self):
        """Testa permissão para gerenciar documentos"""
        cargo = Cargo.objects.create(
            nome="Secretário",
            pode_gerenciar_documentos=True
        )
        assert cargo.pode_gerenciar_documentos is True
    
    def test_cargo_pode_visualizar_relatorios(self):
        """Testa permissão para visualizar relatórios"""
        cargo = Cargo.objects.create(
            nome="Gerente",
            pode_visualizar_relatorios=True
        )
        assert cargo.pode_visualizar_relatorios is True
    
    def test_cargo_pode_gerenciar_cargos(self):
        """Testa permissão para gerenciar cargos"""
        cargo = Cargo.objects.create(
            nome="Administrador",
            pode_gerenciar_cargos=True
        )
        assert cargo.pode_gerenciar_cargos is True
    
    def test_cargo_multiple_permissions(self):
        """Testa cargo com múltiplas permissões"""
        cargo_pastor = Cargo.objects.create(
            nome="Pastor",
            pode_gerenciar_membros=True,
            pode_gerenciar_financas=True,
            pode_registrar_dizimos=True,
            pode_registrar_ofertas=True,
            pode_gerenciar_eventos=True,
            pode_gerenciar_documentos=True,
            pode_visualizar_relatorios=True,
            pode_gerenciar_cargos=False
        )
        
        assert cargo_pastor.pode_gerenciar_membros is True
        assert cargo_pastor.pode_gerenciar_financas is True
        assert cargo_pastor.pode_registrar_dizimos is True
        assert cargo_pastor.pode_registrar_ofertas is True
        assert cargo_pastor.pode_gerenciar_eventos is True
        assert cargo_pastor.pode_gerenciar_documentos is True
        assert cargo_pastor.pode_visualizar_relatorios is True
        assert cargo_pastor.pode_gerenciar_cargos is False
    
    def test_cargo_minimal_permissions(self):
        """Testa cargo com permissões mínimas"""
        cargo_membro = Cargo.objects.create(
            nome="Membro",
            pode_gerenciar_membros=False,
            pode_gerenciar_financas=False,
            pode_registrar_dizimos=False,
            pode_registrar_ofertas=False,
            pode_gerenciar_eventos=False,
            pode_gerenciar_documentos=False,
            pode_visualizar_relatorios=False,
            pode_gerenciar_cargos=False
        )
        
        assert cargo_membro.pode_gerenciar_membros is False
        assert cargo_membro.pode_gerenciar_financas is False
        assert cargo_membro.pode_registrar_dizimos is False
        assert cargo_membro.pode_registrar_ofertas is False
        assert cargo_membro.pode_gerenciar_eventos is False
        assert cargo_membro.pode_gerenciar_documentos is False
        assert cargo_membro.pode_visualizar_relatorios is False
        assert cargo_membro.pode_gerenciar_cargos is False


@pytest.mark.unit
@pytest.mark.permissions
class TestAdminPermissionsByRole(TestCase):
    """Testes de permissões do Admin baseado em cargo"""
    
    def setUp(self):
        """Configuração inicial"""
        self.cargo_admin = Cargo.objects.create(
            nome="Admin",
            pode_gerenciar_membros=True,
            pode_gerenciar_financas=True,
            pode_registrar_dizimos=True,
            pode_registrar_ofertas=True,
            pode_gerenciar_eventos=True,
            pode_gerenciar_documentos=True,
            pode_visualizar_relatorios=True,
            pode_gerenciar_cargos=True
        )
        
        self.cargo_tesoureiro = Cargo.objects.create(
            nome="Tesoureiro",
            pode_gerenciar_financas=True,
            pode_registrar_dizimos=True,
            pode_registrar_ofertas=True,
            pode_visualizar_relatorios=True
        )
        
        self.cargo_secretario = Cargo.objects.create(
            nome="Secretário",
            pode_gerenciar_membros=True,
            pode_gerenciar_documentos=True
        )
        
        self.admin_completo = Admin.objects.create(
            nome="Admin Completo",
            email="admin@church.com",
            senha="admin123",
            cargo=self.cargo_admin
        )
        
        self.admin_tesoureiro = Admin.objects.create(
            nome="Admin Tesoureiro",
            email="tesoureiro@church.com",
            senha="t123",
            cargo=self.cargo_tesoureiro
        )
        
        self.admin_secretario = Admin.objects.create(
            nome="Admin Secretário",
            email="secretario@church.com",
            senha="s123",
            cargo=self.cargo_secretario
        )
    
    def test_admin_with_full_role_has_all_permissions(self):
        """Testa que admin com cargo completo tem todas as permissões"""
        cargo = self.admin_completo.cargo
        
        assert cargo.pode_gerenciar_membros is True
        assert cargo.pode_gerenciar_financas is True
        assert cargo.pode_registrar_dizimos is True
        assert cargo.pode_registrar_ofertas is True
        assert cargo.pode_gerenciar_eventos is True
        assert cargo.pode_gerenciar_documentos is True
        assert cargo.pode_visualizar_relatorios is True
        assert cargo.pode_gerenciar_cargos is True
    
    def test_admin_tesoureiro_has_finance_permissions(self):
        """Testa que tesoureiro tem permissões de finanças"""
        cargo = self.admin_tesoureiro.cargo
        
        assert cargo.pode_gerenciar_financas is True
        assert cargo.pode_registrar_dizimos is True
        assert cargo.pode_registrar_ofertas is True
        assert cargo.pode_visualizar_relatorios is True
    
    def test_admin_tesoureiro_cannot_manage_members(self):
        """Testa que tesoureiro não pode gerenciar membros"""
        cargo = self.admin_tesoureiro.cargo
        
        assert cargo.pode_gerenciar_membros is False
    
    def test_admin_secretario_can_manage_members(self):
        """Testa que secretário pode gerenciar membros"""
        cargo = self.admin_secretario.cargo
        
        assert cargo.pode_gerenciar_membros is True
        assert cargo.pode_gerenciar_documentos is True
    
    def test_admin_secretario_cannot_manage_finances(self):
        """Testa que secretário não pode gerenciar finanças"""
        cargo = self.admin_secretario.cargo
        
        assert cargo.pode_gerenciar_financas is False
        assert cargo.pode_registrar_dizimos is False
        assert cargo.pode_registrar_ofertas is False
    
    def test_admin_role_change_affects_permissions(self):
        """Testa que trocar cargo do admin afeta permissões"""
        assert self.admin_secretario.cargo.pode_gerenciar_membros is True
        
        novo_cargo = Cargo.objects.create(
            nome="Membro Comum",
            pode_gerenciar_membros=False,
            pode_gerenciar_documentos=False
        )
        
        self.admin_secretario.cargo = novo_cargo
        self.admin_secretario.save()
        
        admin_atualizado = Admin.objects.get(id=self.admin_secretario.id)
        assert admin_atualizado.cargo.pode_gerenciar_membros is False


@pytest.mark.unit
@pytest.mark.permissions
class TestUsuarioPermissionsByRole(TestCase):
    """Testes de permissões do Usuario baseado em cargo"""
    
    def setUp(self):
        """Configuração inicial"""
        self.cargo_organizador = Cargo.objects.create(
            nome="Organizador de Eventos",
            pode_gerenciar_eventos=True,
            pode_visualizar_relatorios=False
        )
        
        self.cargo_tesoureiro = Cargo.objects.create(
            nome="Tesoureiro",
            pode_gerenciar_financas=True,
            pode_visualizar_relatorios=True
        )
        
        self.usuario_organizador = Usuario.objects.create(
            username="organizador",
            email="organizador@church.com",
            senha="o123",
            cargo=self.cargo_organizador
        )
        
        self.usuario_tesoureiro = Usuario.objects.create(
            username="tesoureiro",
            email="tesoureiro@church.com",
            senha="t123",
            cargo=self.cargo_tesoureiro
        )
    
    def test_usuario_organizador_can_manage_events(self):
        """Testa que organizador pode gerenciar eventos"""
        cargo = self.usuario_organizador.cargo
        assert cargo.pode_gerenciar_eventos is True
    
    def test_usuario_organizador_cannot_manage_finances(self):
        """Testa que organizador não pode gerenciar finanças"""
        cargo = self.usuario_organizador.cargo
        assert cargo.pode_gerenciar_financas is False
    
    def test_usuario_tesoureiro_can_view_reports(self):
        """Testa que tesoureiro pode visualizar relatórios"""
        cargo = self.usuario_tesoureiro.cargo
        assert cargo.pode_visualizar_relatorios is True
    
    def test_usuario_tesoureiro_cannot_manage_events(self):
        """Testa que tesoureiro não pode gerenciar eventos"""
        cargo = self.usuario_tesoureiro.cargo
        assert cargo.pode_gerenciar_eventos is False
    
    def test_different_usuarios_have_different_permissions(self):
        """Testa que usuários com cargos diferentes têm permissões diferentes"""
        org_cargo = self.usuario_organizador.cargo
        treas_cargo = self.usuario_tesoureiro.cargo
        
        assert org_cargo.pode_gerenciar_eventos is True
        assert treas_cargo.pode_gerenciar_eventos is False
        
        assert org_cargo.pode_gerenciar_financas is False
        assert treas_cargo.pode_gerenciar_financas is True
    
    def test_usuario_permission_inheritance_from_role(self):
        """Testa que permissão do usuário vem do cargo"""
        usuario = Usuario.objects.create(
            username="novo_usuario",
            email="novo@church.com",
            senha="n123",
            cargo=self.cargo_organizador
        )
        
        assert usuario.cargo.pode_gerenciar_eventos is True
        assert usuario.cargo.pode_visualizar_relatorios is False


@pytest.mark.unit
@pytest.mark.permissions
class TestPermissionValidation(TestCase):
    """Testes de validação de permissões"""
    
    def setUp(self):
        """Configuração inicial"""
        self.cargo_completo = Cargo.objects.create(
            nome="Admin Completo",
            pode_gerenciar_membros=True,
            pode_gerenciar_financas=True,
            pode_registrar_dizimos=True,
            pode_registrar_ofertas=True,
            pode_gerenciar_eventos=True,
            pode_gerenciar_documentos=True,
            pode_visualizar_relatorios=True,
            pode_gerenciar_cargos=True
        )
        
        self.cargo_restrito = Cargo.objects.create(
            nome="Membro Restrito",
            pode_gerenciar_membros=False,
            pode_gerenciar_financas=False,
            pode_registrar_dizimos=False,
            pode_registrar_ofertas=False,
            pode_gerenciar_eventos=False,
            pode_gerenciar_documentos=False,
            pode_visualizar_relatorios=False,
            pode_gerenciar_cargos=False
        )
    
    def test_cargo_completo_has_all_permissions(self):
        """Testa que cargo completo tem todas as 8 permissões"""
        permissoes = [
            self.cargo_completo.pode_gerenciar_membros,
            self.cargo_completo.pode_gerenciar_financas,
            self.cargo_completo.pode_registrar_dizimos,
            self.cargo_completo.pode_registrar_ofertas,
            self.cargo_completo.pode_gerenciar_eventos,
            self.cargo_completo.pode_gerenciar_documentos,
            self.cargo_completo.pode_visualizar_relatorios,
            self.cargo_completo.pode_gerenciar_cargos
        ]
        
        assert all(permissoes) is True
        assert len([p for p in permissoes if p]) == 8
    
    def test_cargo_restrito_has_no_permissions(self):
        """Testa que cargo restrito não tem nenhuma permissão"""
        permissoes = [
            self.cargo_restrito.pode_gerenciar_membros,
            self.cargo_restrito.pode_gerenciar_financas,
            self.cargo_restrito.pode_registrar_dizimos,
            self.cargo_restrito.pode_registrar_ofertas,
            self.cargo_restrito.pode_gerenciar_eventos,
            self.cargo_restrito.pode_gerenciar_documentos,
            self.cargo_restrito.pode_visualizar_relatorios,
            self.cargo_restrito.pode_gerenciar_cargos
        ]
        
        assert any(permissoes) is False
        assert len([p for p in permissoes if p]) == 0
    
    def test_permission_count_completo(self):
        """Testa contagem de permissões do cargo completo"""
        count = sum([
            self.cargo_completo.pode_gerenciar_membros,
            self.cargo_completo.pode_gerenciar_financas,
            self.cargo_completo.pode_registrar_dizimos,
            self.cargo_completo.pode_registrar_ofertas,
            self.cargo_completo.pode_gerenciar_eventos,
            self.cargo_completo.pode_gerenciar_documentos,
            self.cargo_completo.pode_visualizar_relatorios,
            self.cargo_completo.pode_gerenciar_cargos
        ])
        
        assert count == 8
    
    def test_permission_count_restrito(self):
        """Testa contagem de permissões do cargo restrito"""
        count = sum([
            self.cargo_restrito.pode_gerenciar_membros,
            self.cargo_restrito.pode_gerenciar_financas,
            self.cargo_restrito.pode_registrar_dizimos,
            self.cargo_restrito.pode_registrar_ofertas,
            self.cargo_restrito.pode_gerenciar_eventos,
            self.cargo_restrito.pode_gerenciar_documentos,
            self.cargo_restrito.pode_visualizar_relatorios,
            self.cargo_restrito.pode_gerenciar_cargos
        ])
        
        assert count == 0
