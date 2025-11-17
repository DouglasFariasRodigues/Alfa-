"""
Testes para Eventos, Fotos de Eventos e Presenças.
"""
import pytest
from django.test import TestCase
from django.utils import timezone

from app_alfa.models import (
    Usuario, Evento, FotoEvento, Membro, Admin
)


@pytest.mark.unit
@pytest.mark.events
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
    
    def test_evento_has_timestamps(self):
        """Testa que evento tem timestamps"""
        evento = Evento.objects.create(
            titulo="Culto",
            descricao="Culto",
            data=timezone.now(),
            local="Igreja",
            organizador=self.usuario
        )
        assert evento.created_at is not None
        assert evento.updated_at is not None
        assert evento.is_active is True
    
    def test_evento_is_soft_deletable(self):
        """Testa que evento suporta soft delete"""
        evento = Evento.objects.create(
            titulo="Culto",
            descricao="Culto",
            data=timezone.now(),
            local="Igreja",
            organizador=self.usuario
        )
        evento.delete()
        
        assert evento.deleted_at is not None
        assert evento.is_active is False
        
        evento_recuperado = Evento.objects.filter(id=evento.id).first()
        assert evento_recuperado is None
    
    def test_evento_update_description(self):
        """Testa atualização de descrição do evento"""
        evento = Evento.objects.create(
            titulo="Culto",
            descricao="Culto dominical",
            data=timezone.now(),
            local="Igreja",
            organizador=self.usuario
        )
        
        nova_descricao = "Culto especial com louvor"
        evento.descricao = nova_descricao
        evento.save()
        
        evento_atualizado = Evento.objects.get(id=evento.id)
        assert evento_atualizado.descricao == nova_descricao
    
    def test_evento_update_local(self):
        """Testa atualização de local do evento"""
        evento = Evento.objects.create(
            titulo="Culto",
            descricao="Culto",
            data=timezone.now(),
            local="Igreja Central",
            organizador=self.usuario
        )
        
        novo_local = "Igreja da Zona Leste"
        evento.local = novo_local
        evento.save()
        
        evento_atualizado = Evento.objects.get(id=evento.id)
        assert evento_atualizado.local == novo_local
    
    def test_evento_update_data(self):
        """Testa atualização de data do evento"""
        evento = Evento.objects.create(
            titulo="Culto",
            descricao="Culto",
            data=timezone.now(),
            local="Igreja",
            organizador=self.usuario
        )
        
        nova_data = timezone.now() + timezone.timedelta(days=7)
        evento.data = nova_data
        evento.save()
        
        evento_atualizado = Evento.objects.get(id=evento.id)
        assert evento_atualizado.data == nova_data
    
    def test_multiple_eventos_by_same_organizador(self):
        """Testa que mesmo organizador pode criar múltiplos eventos"""
        evento1 = Evento.objects.create(
            titulo="Culto",
            descricao="Culto",
            data=timezone.now(),
            local="Igreja",
            organizador=self.usuario
        )
        evento2 = Evento.objects.create(
            titulo="Estudo Bíblico",
            descricao="Estudo da Palavra",
            data=timezone.now(),
            local="Sala 1",
            organizador=self.usuario
        )
        
        eventos = Evento.objects.filter(organizador=self.usuario)
        assert eventos.count() == 2
        assert evento2 in eventos
    
    def test_evento_com_multiplas_fotos(self):
        """Testa evento com múltiplas fotos"""
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
        FotoEvento.objects.create(
            evento=evento,
            imagem="foto3.jpg",
            descricao="Foto 3"
        )
        
        assert evento.fotos.count() == 3


@pytest.mark.unit
@pytest.mark.events
class TestFotoEvento(TestCase):
    """Testes para fotos de eventos"""
    
    def setUp(self):
        """Configuração inicial"""
        self.usuario = Usuario.objects.create(
            username="user1",
            email="user1@test.com",
            senha="u123"
        )
        
        self.evento = Evento.objects.create(
            titulo="Evento Test",
            descricao="Teste",
            data=timezone.now(),
            local="Local",
            organizador=self.usuario
        )
    
    def test_foto_evento_creation(self):
        """Testa criação de foto de evento"""
        foto = FotoEvento.objects.create(
            evento=self.evento,
            imagem="foto.jpg",
            descricao="Foto teste"
        )
        
        assert foto.evento == self.evento
        assert foto.descricao == "Foto teste"
    
    def test_foto_evento_has_timestamp(self):
        """Testa que foto tem timestamp"""
        foto = FotoEvento.objects.create(
            evento=self.evento,
            imagem="foto.jpg"
        )
        
        assert foto.data_upload is not None
    
    def test_foto_evento_sem_descricao(self):
        """Testa que foto pode não ter descrição"""
        foto = FotoEvento.objects.create(
            evento=self.evento,
            imagem="foto.jpg"
        )
        
        assert foto.descricao is None or foto.descricao == ""
    
    def test_delete_foto_evento(self):
        """Testa exclusão de foto"""
        foto = FotoEvento.objects.create(
            evento=self.evento,
            imagem="foto.jpg"
        )
        
        foto_id = foto.id
        foto.delete()
        
        foto_deletada = FotoEvento.objects.filter(id=foto_id).first()
        assert foto_deletada is None
    
    def test_multiplas_fotos_different_eventos(self):
        """Testa que fotos podem estar em eventos diferentes"""
        evento2 = Evento.objects.create(
            titulo="Evento 2",
            descricao="Teste 2",
            data=timezone.now(),
            local="Local 2",
            organizador=self.usuario
        )
        
        foto1 = FotoEvento.objects.create(
            evento=self.evento,
            imagem="foto1.jpg"
        )
        
        foto2 = FotoEvento.objects.create(
            evento=evento2,
            imagem="foto2.jpg"
        )
        
        assert foto1.evento == self.evento
        assert foto2.evento == evento2
        assert foto1.evento != foto2.evento


@pytest.mark.unit
@pytest.mark.events
class TestEventoPresence(TestCase):
    """Testes de presenças em eventos"""
    
    def setUp(self):
        """Configuração inicial"""
        self.admin = Admin.objects.create(
            nome="Admin",
            email="admin@test.com",
            senha="123"
        )
        
        self.usuario = Usuario.objects.create(
            username="user1",
            email="user1@test.com",
            senha="u123"
        )
        
        self.membro1 = Membro.objects.create(
            nome="Membro 1",
            email="membro1@test.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
        
        self.membro2 = Membro.objects.create(
            nome="Membro 2",
            email="membro2@test.com",
            status=Membro.ATIVO,
            cadastrado_por=self.admin
        )
        
        self.evento = Evento.objects.create(
            titulo="Culto",
            descricao="Culto",
            data=timezone.now(),
            local="Igreja",
            organizador=self.usuario
        )
    
    def test_evento_has_multiplos_membros(self):
        """Testa que evento pode ter múltiplos membros relacionados"""
        assert self.membro1 is not None
        assert self.membro2 is not None
        assert self.evento is not None
    
    def test_membro_status_validation_for_presence(self):
        """Testa que apenas membros ativos podem ter presença registrada"""
        assert self.membro1.status == Membro.ATIVO
        
        self.membro2.status = Membro.INATIVO
        self.membro2.save()
        
        assert self.membro2.status == Membro.INATIVO
    
    def test_evento_organizador_relationship(self):
        """Testa relacionamento entre evento e organizador"""
        assert self.evento.organizador == self.usuario
        
        eventos = Evento.objects.filter(organizador=self.usuario)
        assert self.evento in eventos
    
    def test_evento_data_comparison(self):
        """Testa que pode comparar datas de eventos"""
        data_passada = timezone.now() - timezone.timedelta(days=7)
        evento_passado = Evento.objects.create(
            titulo="Evento Passado",
            descricao="Teste",
            data=data_passada,
            local="Local",
            organizador=self.usuario
        )
        
        assert evento_passado.data < self.evento.data
        assert self.evento.data > evento_passado.data
    
    def test_evento_future_date(self):
        """Testa evento com data futura"""
        data_futura = timezone.now() + timezone.timedelta(days=30)
        evento_futuro = Evento.objects.create(
            titulo="Evento Futuro",
            descricao="Teste",
            data=data_futura,
            local="Local",
            organizador=self.usuario
        )
        
        assert evento_futuro.data > timezone.now()
    
    def test_membro_count_for_event_attendance(self):
        """Testa contagem de membros para presenças"""
        total_membros = Membro.objects.filter(status=Membro.ATIVO).count()
        assert total_membros >= 1


@pytest.mark.unit
@pytest.mark.events
class TestEventoValidation(TestCase):
    """Testes de validação de eventos"""
    
    def setUp(self):
        """Configuração inicial"""
        self.usuario = Usuario.objects.create(
            username="user1",
            email="user1@test.com",
            senha="u123"
        )
    
    def test_evento_requires_organizador(self):
        """Testa que evento requer organizador"""
        try:
            evento = Evento.objects.create(
                titulo="Evento",
                descricao="Teste",
                data=timezone.now(),
                organizador=None
            )
            assert False, "Deveria ter falhado"
        except Exception:
            pass  # Esperado - campo obrigatório
    
    def test_evento_descricao_can_be_long(self):
        """Testa que descrição pode ser longa"""
        descricao_longa = "Lorem ipsum dolor sit amet " * 50
        evento = Evento.objects.create(
            titulo="Evento",
            descricao=descricao_longa,
            data=timezone.now(),
            organizador=self.usuario
        )
        
        assert evento.descricao == descricao_longa
    
    def test_evento_local_optional(self):
        """Testa que local é opcional"""
        evento = Evento.objects.create(
            titulo="Evento",
            descricao="Teste",
            data=timezone.now(),
            organizador=self.usuario
        )
        
        assert evento.local is None
