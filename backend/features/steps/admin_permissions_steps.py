"""
Steps de teste para permissões de Admin.
Testa se o Admin sem permissão é bloqueado ao tentar executar ações.
"""
from behave import given, when, then
from app_alfa.models import Admin, Cargo, Transacao
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal

# Passo: Admin tem um cargo com permissões específicas
@given('o Admin tem um cargo "{cargo_nome}" sem permissão para registrar dízimos')
def step_given_admin_cargo_no_dizimo(context, cargo_nome):
    # Criar cargo sem permissão
    cargo = Cargo.objects.create(
        nome=cargo_nome,
        descricao=f"Cargo {cargo_nome}",
        pode_registrar_dizimos=False,
        pode_registrar_ofertas=False,
        pode_gerenciar_membros=False,
        pode_gerenciar_eventos=False,
        pode_gerenciar_financas=False,
        pode_gerenciar_cargos=False,
        pode_gerenciar_documentos=False,
        pode_visualizar_relatorios=False
    )
    
    # Associar cargo ao admin
    context.admin.cargo = cargo
    context.admin.save()

# Passo: Admin tem um cargo com permissões específicas
@given('o Admin tem um cargo "{cargo_nome}" com permissão para registrar dízimos')
def step_given_admin_cargo_with_dizimo(context, cargo_nome):
    # Criar cargo com permissão
    cargo = Cargo.objects.create(
        nome=cargo_nome,
        descricao=f"Cargo {cargo_nome}",
        pode_registrar_dizimos=True,
        pode_registrar_ofertas=True,
        pode_gerenciar_membros=True,
        pode_gerenciar_eventos=True,
        pode_gerenciar_financas=True,
        pode_gerenciar_cargos=True,
        pode_gerenciar_documentos=True,
        pode_visualizar_relatorios=True
    )
    
    # Associar cargo ao admin
    context.admin.cargo = cargo
    context.admin.save()

# Passo: Admin tenta criar transação (teste de permissão)
@when('o Admin tenta criar uma transação de entrada tipo "{tipo}" com valor {valor:f}')
def step_when_admin_create_transacao(context, tipo, valor):
    if not hasattr(context, 'client'):
        context.client = APIClient()
    
    # Usar token do login anterior
    if hasattr(context, 'access_token') and context.access_token:
        context.client.credentials(HTTP_AUTHORIZATION=f'Bearer {context.access_token}')
    elif hasattr(context, 'login_response') and hasattr(context, 'login_status') and context.login_status == status.HTTP_200_OK:
        # Se não tem access_token direto, extrair do response
        data = context.login_response.json()
        token = data.get('access_token') or data.get('access')
        if token:
            context.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
            context.access_token = token
    
    # Fazer requisição POST para criar transação
    response = context.client.post('/api/transacoes/', {
        'tipo': 'entrada',
        'categoria': tipo,
        'valor': str(valor),
        'data': '2025-11-01',
        'descricao': f'Transação teste {tipo}'
    }, format='json')
    
    context.api_response = response
    context.api_status = response.status_code

# Passo: Requisição retorna 403 Forbidden
@then('a requisição deve retornar erro 403 "Forbidden"')
def step_then_forbidden_error(context):
    assert context.api_status == status.HTTP_403_FORBIDDEN, \
        f"Status esperado 403, recebido {context.api_status}"

# Passo: Mensagem de erro contém texto
@then('a mensagem de erro deve conter "{error_text}"')
def step_then_error_contains(context, error_text):
    response_data = context.api_response.json()
    
    # Procurar em vários locais possíveis da resposta
    error_msg = str(response_data.get('detail', '') or response_data.get('message', '') or response_data.get('error', ''))
    
    assert error_text.lower() in error_msg.lower(), \
        f"Erro '{error_text}' não encontrado em '{error_msg}'"

# Passo: Requisição retorna 201 ou 200
@then('a requisição deve retornar status 201 ou 200')
def step_then_success_status(context):
    assert context.api_status in (status.HTTP_201_CREATED, status.HTTP_200_OK), \
        f"Status esperado 201 ou 200, recebido {context.api_status}: {context.api_response.json()}"

# Passo: Transação criada com sucesso
@then('a transação deve ser criada com sucesso')
def step_then_transacao_created(context):
    response_data = context.api_response.json()
    
    assert 'id' in response_data or response_data.get('success', False), \
        f"Transação não foi criada: {response_data}"
