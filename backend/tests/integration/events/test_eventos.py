"""
Testes de integração para eventos, fotos e presenças.
Valida fluxos completos de criação e gerenciamento de eventos.
"""
import pytest
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from app_alfa.models import (
    Admin, Usuario, Evento, FotoEvento, Membro, EventoPresenca
)


@pytest.mark.integration
@pytest.mark.events
class TestEventoIntegration(TestCase):
    """Testes de integração para fluxo de eventos"""
    
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
    
    def test_evento_creation_flow(self):
        """Testa fluxo completo de criação de evento"""
        data_evento = timezone.now() + timedelta(days=7)
        
        evento = Evento.objects.create(
            titulo="Culto Especial",
            descricao="Evento de louvor",
            data=data_evento,
            local="Igreja Central",
            organizador=self.usuario
        )
        
        assert evento.titulo == "Culto Especial"
        assert evento.organizador == self.usuario
        assert evento.local == "Igreja Central"
    
    def test_evento_count_by_user(self):
        """Testa contagem de eventos por organizador"""
        for i in range(3):
            Evento.objects.create(
                titulo=f"Evento {i}",
                descricao=f"Descrição {i}",
                data=timezone.now() + timedelta(days=i),
                local="Igreja",
                organizador=self.usuario
            )
        
        eventos_usuario = Evento.objects.filter(organizador=self.usuario).count()
        assert eventos_usuario == 3


@pytest.mark.integration
@pytest.mark.events
class TestFotoEventoIntegration(TestCase):
    """Testes de integração para fotos de eventos"""
    
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
        self.evento = Evento.objects.create(
            titulo="Evento com Fotos",
            descricao="Para test fotos",
            data=timezone.now() - timedelta(days=1),
            local="Igreja",
            organizador=self.usuario
        )
    
    def test_add_foto_to_evento(self):
        """Testa adição de foto a um evento"""
        foto = FotoEvento.objects.create(
            evento=self.evento,
            descricao="Foto 1 do evento"
        )
        
        assert foto.evento == self.evento
        assert foto.descricao == "Foto 1 do evento"
    
    def test_multiple_fotos_single_evento(self):
        """Testa múltiplas fotos em um único evento"""
        fotos = []
        for i in range(5):
            foto = FotoEvento.objects.create(
                evento=self.evento,
                descricao=f"Foto {i+1}"
            )
            fotos.append(foto)
        
        fotos_do_evento = FotoEvento.objects.filter(evento=self.evento)
        assert fotos_do_evento.count() == 5


@pytest.mark.integration
@pytest.mark.events
class TestPresencaIntegration(TestCase):
    """Testes de integração para presenças em eventos"""
    
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
        self.evento = Evento.objects.create(
            titulo="Culto Domingo",
            descricao="Culto dominical",
            data=timezone.now() - timedelta(days=1),
            local="Igreja",
            organizador=self.usuario
        )
        self.membro1 = Membro.objects.create(
            nome="João",
            email="joao@test.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
        self.membro2 = Membro.objects.create(
            nome="Maria",
            email="maria@test.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
    
    def test_register_presenca(self):
        """Testa registro de presença em evento"""
        presenca = EventoPresenca.objects.create(
            evento=self.evento,
            membro=self.membro1
        )
        
        assert presenca.evento == self.evento
        assert presenca.membro == self.membro1
    
    def test_multiple_presencas_same_evento(self):
        """Testa múltiplas presenças no mesmo evento"""
        presenca1 = EventoPresenca.objects.create(
            evento=self.evento,
            membro=self.membro1
        )
        
        presenca2 = EventoPresenca.objects.create(
            evento=self.evento,
            membro=self.membro2
        )
        
        presencas = EventoPresenca.objects.filter(evento=self.evento)
        assert presencas.count() == 2
    
    def test_presenca_count_for_evento(self):
        """Testa contagem de presenças por evento"""
        # Adicionar 10 presenças
        for i in range(10):
            membro = Membro.objects.create(
                nome=f"Membro {i}",
                email=f"membro_presenca{i}@test.com",
                status=Membro.ATIVO,
                cadastrado_por=self.admin
            )
            EventoPresenca.objects.create(
                evento=self.evento,
                membro=membro
            )
        
        total_presencas = EventoPresenca.objects.filter(
            evento=self.evento
        ).count()
        
        assert total_presencas == 10

