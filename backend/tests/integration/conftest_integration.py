"""
Configuração para testes de integração BDD.
"""
import pytest
from django.test import Client


@pytest.fixture
def api_client():
    """Cliente HTTP para fazer requisições à API."""
    return Client()


@pytest.fixture
def authenticated_admin(db, admin_user):
    """Admin já autenticado para testes."""
    return admin_user


@pytest.fixture
def authenticated_member(db, member_user):
    """Membro já autenticado para testes."""
    return member_user
