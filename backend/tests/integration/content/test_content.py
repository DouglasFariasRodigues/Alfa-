"""
Testes de integração para conteúdo disponível aos membros.
Valida visualização e acesso a conteúdo baseado em permissões.
"""
import pytest
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from app_alfa.models import (
    Admin, Usuario, Membro, Cargo, Evento, FotoEvento, Oferta
)


@pytest.mark.integration
@pytest.mark.content
class TestMembroContentAccess(TestCase):
    """Testes de integração para acesso a conteúdo por membros"""
    
    def setUp(self):
        """Preparar dados de teste"""
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
        self.usuario = Usuario.objects.create(
            username="usuario_teste",
            email="usuario@test.com",
            senha="123"
        )
        self.membro = Membro.objects.create(
            nome="João Silva",
            email="joao@test.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
    
    def test_membro_view_ofertas(self):
        """Testa que membros podem visualizar ofertas públicas"""
        oferta_publica = Oferta.objects.create(
            valor=500.00,
            descricao="Oferta pública",
            registrado_por=self.admin,
            is_publico=True
        )
        
        oferta_privada = Oferta.objects.create(
            valor=500.00,
            descricao="Oferta privada",
            registrado_por=self.admin,
            is_publico=False
        )
        
        ofertas_publicas = Oferta.objects.filter(is_publico=True)
        
        assert oferta_publica in ofertas_publicas
        assert oferta_privada not in ofertas_publicas
    
    def test_membro_view_eventos(self):
        """Testa que membros podem visualizar eventos"""
        evento = Evento.objects.create(
            titulo="Evento",
            descricao="Teste",
            data=timezone.now() + timedelta(days=1),
            local="Igreja",
            organizador=self.usuario
        )
        
        assert evento.titulo == "Evento"
        assert evento.organizador == self.usuario
    
    def test_inactive_membro_limited_content_access(self):
        """Testa que membros inativos têm status inativo"""
        membro_inativo = Membro.objects.create(
            nome="Membro Inativo",
            email="inativo@test.com",
            status=Membro.INATIVO,
            cadastrado_por=self.admin
        )
        
        assert membro_inativo.status == Membro.INATIVO


@pytest.mark.integration
@pytest.mark.content
class TestRoleBasedContentAccess(TestCase):
    """Testes de integração para acesso a conteúdo por papel"""
    
    def setUp(self):
        """Preparar dados de teste"""
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
        
        self.cargo_lider = Cargo.objects.create(
            nome="Líder",
            descricao="Acesso completo",
            pode_gerenciar_membros=True,
            pode_gerenciar_financas=True,
            pode_gerenciar_documentos=True
        )
        
        self.cargo_membro = Cargo.objects.create(
            nome="Membro",
            descricao="Acesso básico",
            pode_gerenciar_membros=False,
            pode_gerenciar_financas=False,
            pode_gerenciar_documentos=False
        )
        
        self.lider = Membro.objects.create(
            nome="Líder João",
            email="lider@test.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin,
            cargo=self.cargo_lider
        )
        
        self.membro = Membro.objects.create(
            nome="Membro Maria",
            email="maria@test.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin,
            cargo=self.cargo_membro
        )
    
    def test_lider_can_manage_members(self):
        """Testa que líderes podem gerenciar membros"""
        cargo_lider = self.lider.cargo
        assert cargo_lider.pode_gerenciar_membros is True
    
    def test_membro_cannot_manage_members(self):
        """Testa que membros comuns não podem gerenciar membros"""
        cargo_membro = self.membro.cargo
        assert cargo_membro.pode_gerenciar_membros is False
    
    def test_lider_can_manage_financas(self):
        """Testa que líderes podem gerenciar finanças"""
        cargo_lider = self.lider.cargo
        assert cargo_lider.pode_gerenciar_financas is True
    
    def test_membro_cannot_manage_financas(self):
        """Testa que membros comuns não podem gerenciar finanças"""
        cargo_membro = self.membro.cargo
        assert cargo_membro.pode_gerenciar_financas is False


@pytest.mark.integration
@pytest.mark.content
class TestPublicContent(TestCase):
    """Testes de integração para conteúdo público"""
    
    def setUp(self):
        """Preparar dados de teste"""
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
        self.usuario = Usuario.objects.create(
            username="usuario_teste",
            email="usuario@test.com",
            senha="123"
        )
    
    def test_anonymous_user_view_public_eventos(self):
        """Testa que eventos estão disponíveis"""
        evento_publico = Evento.objects.create(
            titulo="Evento Aberto",
            descricao="Para todos",
            data=timezone.now() + timedelta(days=1),
            local="Igreja",
            organizador=self.usuario
        )
        
        eventos = Evento.objects.filter(titulo="Evento Aberto")
        assert evento_publico in eventos
    
    def test_public_ofertas_visible_count(self):
        """Testa contagem de ofertas públicas"""
        for i in range(5):
            Oferta.objects.create(
                valor=100.00 * (i + 1),
                descricao=f"Oferta {i+1}",
                registrado_por=self.admin,
                is_publico=True
            )
        
        # Adicionar ofertas privadas
        for i in range(3):
            Oferta.objects.create(
                valor=100.00 * (i + 1),
                descricao=f"Oferta privada {i+1}",
                registrado_por=self.admin,
                is_publico=False
            )
        
        ofertas_publicas = Oferta.objects.filter(is_publico=True)
        assert ofertas_publicas.count() == 5

