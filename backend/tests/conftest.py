"""
Configuração global de fixtures para todos os testes.
Aqui são definidas as fixtures compartilhadas entre unit, integration e e2e.
"""
import os
import sys
import django
import pytest
from django.conf import settings

# Adicionar o caminho do backend ao Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfa_project.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from app_alfa.models import Admin, Membro, Usuario, Cargo, Grupo, ONG


@pytest.fixture
def admin_user(db):
    """Cria um Admin de teste."""
    return Admin.objects.create(
        nome="Admin Teste",
        email="admin@teste.com",
        senha=make_password("senha123"),
        is_admin=True
    )


@pytest.fixture
def member_user(db, admin_user):
    """Cria um Membro de teste."""
    return Membro.objects.create(
        nome="João Silva",
        cpf="123.456.789-00",
        email="joao@email.com",
        status=Membro.ATIVO,
        cadastrado_por=admin_user
    )


@pytest.fixture
def regular_user(db):
    """Cria um Usuario regular de teste."""
    return Usuario.objects.create(
        username="usuario_teste",
        email="usuario@teste.com",
        senha=make_password("senha123")
    )


@pytest.fixture
def cargo_pastor(db):
    """Cria um Cargo de Pastor com permissões."""
    return Cargo.objects.create(
        nome="Pastor",
        descricao="Líder espiritual da congregação",
        pode_gerenciar_membros=True,
        pode_gerenciar_financas=True,
        pode_registrar_dizimos=True,
        pode_registrar_ofertas=True,
        pode_gerenciar_eventos=True,
        pode_gerenciar_documentos=True,
        pode_visualizar_relatorios=True,
        pode_gerenciar_cargos=False
    )


@pytest.fixture
def cargo_tesoureiro(db):
    """Cria um Cargo de Tesoureiro com permissões financeiras."""
    return Cargo.objects.create(
        nome="Tesoureiro",
        descricao="Responsável pelas finanças da congregação",
        pode_gerenciar_membros=False,
        pode_gerenciar_financas=True,
        pode_registrar_dizimos=True,
        pode_registrar_ofertas=True,
        pode_gerenciar_eventos=False,
        pode_gerenciar_documentos=False,
        pode_visualizar_relatorios=True,
        pode_gerenciar_cargos=False
    )


@pytest.fixture
def cargo_secretario(db):
    """Cria um Cargo de Secretário com permissões administrativas."""
    return Cargo.objects.create(
        nome="Secretário",
        descricao="Responsável pelos registros e documentos",
        pode_gerenciar_membros=True,
        pode_gerenciar_financas=False,
        pode_registrar_dizimos=False,
        pode_registrar_ofertas=False,
        pode_gerenciar_eventos=False,
        pode_gerenciar_documentos=True,
        pode_visualizar_relatorios=False,
        pode_gerenciar_cargos=False
    )


@pytest.fixture
def grupo_missoes(db):
    """Cria um Grupo de Missões para testes."""
    return Grupo.objects.create(
        nome="Missões",
        descricao="Grupo de trabalho missionário"
    )


@pytest.fixture
def ong_test(db):
    """Cria uma ONG de teste para doações."""
    return ONG.objects.create(
        nome="ONG Teste",
        cnpj="12.345.678/0001-90"
    )
