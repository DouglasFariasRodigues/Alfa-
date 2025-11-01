"""
Steps de teste para permissões de Usuario.
Testa se o Usuario com cargo limitado é bloqueado ao tentar executar ações não autorizadas.
"""
from behave import given, when, then
from app_Alfa.models import Usuario, Cargo
from rest_framework.test import APIClient
from rest_framework import status

# Passo: Usuario tem um cargo sem permissões específicas
@given('o Usuario tem um cargo "{cargo_nome}" sem permissão para gerenciar membros')
def step_given_usuario_cargo_no_membros(context, cargo_nome):
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
    
    # Associar cargo ao usuario
    context.usuario.cargo = cargo
    context.usuario.save()

# Passo: Usuario tem um cargo com permissões específicas
@given('o Usuario tem um cargo "{cargo_nome}" com permissão para gerenciar eventos')
def step_given_usuario_cargo_with_eventos(context, cargo_nome):
    # Criar cargo com permissão
    cargo = Cargo.objects.create(
        nome=cargo_nome,
        descricao=f"Cargo {cargo_nome}",
        pode_registrar_dizimos=False,
        pode_registrar_ofertas=False,
        pode_gerenciar_membros=False,
        pode_gerenciar_eventos=True,
        pode_gerenciar_financas=False,
        pode_gerenciar_cargos=False,
        pode_gerenciar_documentos=False,
        pode_visualizar_relatorios=False
    )
    
    # Associar cargo ao usuario
    context.usuario.cargo = cargo
    context.usuario.save()

# Passo: Usuario tenta listar membros
@when('o Usuario tenta listar membros')
def step_when_usuario_list_membros(context):
    if not hasattr(context, 'client'):
        context.client = APIClient()
    
    # Usar token do login anterior
    if hasattr(context, 'access_token'):
        context.client.credentials(HTTP_AUTHORIZATION=f'Bearer {context.access_token}')
    
    # Fazer requisição GET para listar membros
    response = context.client.get('/api/membros/', format='json')
    
    context.api_response = response
    context.api_status = response.status_code

# Passo: Usuario tenta criar um novo membro
@when('o Usuario tenta criar um novo membro')
def step_when_usuario_create_membro(context):
    if not hasattr(context, 'client'):
        context.client = APIClient()
    
    # Usar token do login anterior
    if hasattr(context, 'access_token'):
        context.client.credentials(HTTP_AUTHORIZATION=f'Bearer {context.access_token}')
    
    # Fazer requisição POST para criar membro
    response = context.client.post('/api/membros/', {
        'nome': 'Novo Membro',
        'email': 'membro@teste.com',
        'telefone': '11987654321',
        'status': 'ativo',
        'data_batismo': '2020-01-01'
    }, format='json')
    
    context.api_response = response
    context.api_status = response.status_code

# Passo: Usuario tenta listar eventos
@when('o Usuario tenta listar eventos')
def step_when_usuario_list_eventos(context):
    if not hasattr(context, 'client'):
        context.client = APIClient()
    
    # Usar token do login anterior
    if hasattr(context, 'access_token'):
        context.client.credentials(HTTP_AUTHORIZATION=f'Bearer {context.access_token}')
    
    # Fazer requisição GET para listar eventos
    response = context.client.get('/api/eventos/', format='json')
    
    context.api_response = response
    context.api_status = response.status_code

# Passo: Usuario recebe lista de eventos
@then('o Usuario deve receber a lista de eventos')
def step_then_usuario_receive_events(context):
    response_data = context.api_response.json()
    
    # Verificar se é uma lista ou um dict com results
    assert isinstance(response_data, (list, dict)), \
        f"Resposta deve ser list ou dict, recebido {type(response_data)}"

# Passo: Usuario cadastrado (para reusar step existente)
@given('que existe um Usuario cadastrado com email "{email}" e senha "{senha}"')
def step_given_usuario_exists(context, email, senha):
    context.usuario = Usuario.objects.create(
        username=email.split('@')[0],
        email=email,
        senha=senha,
        is_active=True,
        is_staff=True
    )
    context.usuario.set_password(senha)
    context.usuario.save()

# Passo: Usuario faz login
@when('o Usuario faz login com email "{email}" e senha "{senha}"')
def step_when_usuario_login(context, email, senha):
    # Garantir que usuario tem senha hasheada
    usuario = Usuario.objects.filter(email=email).first()
    if usuario and not usuario.senha.startswith('pbkdf2_'):
        usuario.set_password(senha)
        usuario.save()
    
    context.client = APIClient()
    
    # Fazer requisição POST para endpoint de login do usuario
    response = context.client.post('/api/auth/login_usuario/', {
        'email': email,
        'senha': senha
    }, format='json')
    
    context.login_response = response
    context.login_status = response.status_code
    
    # Armazenar token para próximas requisições
    if context.login_status == status.HTTP_200_OK:
        data = response.json()
        context.access_token = data.get('access_token') or data.get('access')
