"""
Steps de teste para JWT - Token Expiration e Refresh
Testa se o token expira, refresh funciona e validações de JWT
"""
from behave import when, then
from rest_framework.test import APIClient
from rest_framework import status
from datetime import timedelta, datetime
from django.utils import timezone
import jwt
from django.conf import settings

# =============== JWT TOKEN EXPIRATION ===============

# Passo: Admin recebe um access_token válido
@when('o Admin recebe um access_token válido')
def step_when_admin_receives_token(context):
    # Verificar se o login foi bem-sucedido - pode estar em login_response ou login_status
    login_response = getattr(context, 'login_response', None)
    login_status = getattr(context, 'login_status', None)
    
    if login_response:
        # Rota com APIClient
        if login_status == status.HTTP_200_OK:
            data = login_response.json()
            context.access_token = data.get('access_token') or data.get('access')
            assert context.access_token, "Access token não foi fornecido na resposta de login"
        else:
            raise Exception(f"Login falhou com status {login_status}")
    else:
        # Se veio de outro step que não fez a chamada HTTP
        # Tentar fazer o login direto aqui
        email = getattr(context, 'admin_email', context.admin.email if hasattr(context, 'admin') else None)
        senha = getattr(context, 'admin_senha', 'senha123')
        
        assert email, "Email do admin não encontrado no contexto"
        
        client = APIClient()
        response = client.post('/api/auth/login/', {
            'email': email,
            'senha': senha
        }, format='json')
        
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            context.access_token = data.get('access_token') or data.get('access')
            context.client = client
            assert context.access_token, "Access token não foi fornecido"
        else:
            raise Exception(f"Login falhou com status {response.status_code}: {response.json()}")

# Passo: Simular expiração do token
@when('o token expira (simula passagem de tempo)')
def step_when_token_expires(context):
    # Decodificar o token
    try:
        decoded = jwt.decode(context.access_token, settings.SECRET_KEY, algorithms=['HS256'])
        
        # Criar um token com data de expiração no passado
        payload = decoded.copy()
        payload['exp'] = int((timezone.now() - timedelta(minutes=1)).timestamp())
        
        # Recodificar o token com expiração no passado
        context.expired_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    except Exception as e:
        # Se não conseguir manipular o JWT, criar um token expirado genérico
        context.expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MDAwMDAwMDB9.invalid"

# Passo: Admin tenta acessar API com token expirado
@when('o Admin tenta acessar a API com o token expirado')
def step_when_access_with_expired_token(context):
    if not hasattr(context, 'client'):
        context.client = APIClient()
    
    context.client.credentials(HTTP_AUTHORIZATION=f'Bearer {context.expired_token}')
    
    # Tentar acessar um endpoint protegido
    response = context.client.get('/api/membros/', format='json')
    
    context.api_response = response
    context.api_status = response.status_code

# Passo: Requisição retorna erro 401
@then('a requisição deve retornar erro 401 "Unauthorized"')
def step_then_unauthorized_error(context):
    assert context.api_status == status.HTTP_401_UNAUTHORIZED, \
        f"Status esperado 401, recebido {context.api_status}"

# Passo: Mensagem de erro correta
@then('a mensagem de erro deve ser "{erro_msg}"')
def step_then_error_message(context, erro_msg):
    response_data = context.api_response.json()
    
    # Verificar se a mensagem de erro contém o texto esperado
    error_detail = str(response_data.get('detail', ''))
    assert erro_msg.lower() in error_detail.lower(), \
        f"Mensagem de erro esperada '{erro_msg}' não encontrada em '{error_detail}'"

# Passo: Requisição com token válido
@when('o Admin tenta acessar a API com o token válido')
def step_when_access_with_valid_token(context):
    if not hasattr(context, 'client'):
        context.client = APIClient()
    
    context.client.credentials(HTTP_AUTHORIZATION=f'Bearer {context.access_token}')
    
    # Tentar acessar um endpoint protegido
    response = context.client.get('/api/membros/', format='json')
    
    context.api_response = response
    context.api_status = response.status_code

# Passo: Requisição retorna 200
@then('a requisição deve retornar status 200')
def step_then_success_status(context):
    assert context.api_status == status.HTTP_200_OK, \
        f"Status esperado 200, recebido {context.api_status}"

# Passo: Admin recebe dados de resposta
@then('o Admin deve receber os dados de resposta')
def step_then_receive_data(context):
    response_data = context.api_response.json()
    
    # Verificar se há dados na resposta
    assert response_data is not None, "Resposta não contém dados"
    assert isinstance(response_data, (dict, list)), "Resposta deve ser dict ou list"

# =============== JWT REFRESH TOKEN ===============

# Passo: Admin recebe access_token e refresh_token válidos
@when('o Admin recebe um access_token e refresh_token válidos')
def step_when_admin_receives_tokens(context):
    # Verificar se o login foi bem-sucedido - pode estar em login_response ou login_status
    login_response = getattr(context, 'login_response', None)
    login_status = getattr(context, 'login_status', None)
    
    if login_response:
        # Rota com APIClient
        if login_status == status.HTTP_200_OK:
            data = login_response.json()
            context.access_token = data.get('access_token') or data.get('access')
            context.refresh_token = data.get('refresh_token') or data.get('refresh')
            
            assert context.access_token, "Access token não foi fornecido"
            assert context.refresh_token, "Refresh token não foi fornecido"
        else:
            raise Exception(f"Login falhou com status {login_status}")
    else:
        # Se veio de outro step que não fez a chamada HTTP
        # Tentar fazer o login direto aqui
        email = getattr(context, 'admin_email', context.admin.email if hasattr(context, 'admin') else None)
        senha = getattr(context, 'admin_senha', 'senha123')
        
        assert email, "Email do admin não encontrado"
        
        client = APIClient()
        response = client.post('/api/auth/login/', {
            'email': email,
            'senha': senha
        }, format='json')
        
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            context.access_token = data.get('access_token') or data.get('access')
            context.refresh_token = data.get('refresh_token') or data.get('refresh')
            context.client = client
            assert context.access_token, "Access token não foi fornecido"
            assert context.refresh_token, "Refresh token não foi fornecido"
        else:
            raise Exception(f"Login falhou com status {response.status_code}")

# Passo: Receber refresh_token válido
@when('o Admin recebe um refresh_token válido')
def step_when_admin_receives_refresh_token(context):
    login_response = getattr(context, 'login_response', None)
    login_status = getattr(context, 'login_status', None)
    
    if login_response:
        if login_status == status.HTTP_200_OK:
            data = login_response.json()
            context.refresh_token = data.get('refresh_token') or data.get('refresh')
            
            assert context.refresh_token, "Refresh token não foi fornecido"
        else:
            raise Exception(f"Login falhou com status {login_status}")
    else:
        # Fazer login direto
        email = getattr(context, 'admin_email', context.admin.email if hasattr(context, 'admin') else None)
        senha = getattr(context, 'admin_senha', 'senha123')
        
        assert email, "Email do admin não encontrado"
        
        client = APIClient()
        response = client.post('/api/auth/login/', {
            'email': email,
            'senha': senha
        }, format='json')
        
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            context.refresh_token = data.get('refresh_token') or data.get('refresh')
            context.client = client
            assert context.refresh_token, "Refresh token não foi fornecido"
        else:
            raise Exception(f"Login falhou com status {response.status_code}")

# Passo: Admin usa refresh_token para renovar access_token
@when('o Admin usa o refresh_token para renovar o access_token')
def step_when_refresh_token_used(context):
    if not hasattr(context, 'client'):
        context.client = APIClient()
    
    # Garantir que refresh_token existe
    refresh_token = getattr(context, 'refresh_token', None)
    assert refresh_token, "Refresh token não encontrado no contexto"
    
    # Fazer requisição POST para endpoint de refresh
    response = context.client.post('/api/token/refresh/', {
        'refresh': refresh_token
    }, format='json')
    
    context.refresh_response = response
    context.refresh_status = response.status_code

# Passo: Admin recebe novo access_token válido
@then('o Admin deve receber um novo access_token válido')
def step_then_new_token_received(context):
    assert context.refresh_status == status.HTTP_200_OK, \
        f"Status esperado 200, recebido {context.refresh_status}. Resposta: {context.refresh_response.json()}"
    
    data = context.refresh_response.json()
    new_token = data.get('access_token') or data.get('access')
    
    assert new_token, "Novo access token não foi fornecido"
    
    # Armazenar o novo token
    context.new_access_token = new_token

# Passo: Novo token permite requisições à API
@then('o novo access_token deve permitir requisições à API')
def step_then_new_token_works(context):
    if not hasattr(context, 'client'):
        context.client = APIClient()
    
    context.client.credentials(HTTP_AUTHORIZATION=f'Bearer {context.new_access_token}')
    
    # Tentar acessar um endpoint protegido
    response = context.client.get('/api/membros/', format='json')
    
    # Deve retornar 200 ou 403 (por permissões), mas não 401 (unauthorized)
    assert response.status_code != status.HTTP_401_UNAUTHORIZED, \
        f"Token inválido. Status: {response.status_code}"

# Passo: Tenta usar refresh_token inválido
@when('o Admin tenta usar um refresh_token inválido')
def step_when_invalid_refresh_token(context):
    if not hasattr(context, 'client'):
        context.client = APIClient()
    
    # Usar um refresh token claramente inválido
    context.invalid_refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.invalid"
    
    response = context.client.post('/api/token/refresh/', {
        'refresh': context.invalid_refresh_token
    }, format='json')
    
    context.api_response = response
    context.api_status = response.status_code



# Passo: Novo token tem expiração correta
@then('o novo access_token deve ter uma data de expiração 60 minutos no futuro')
def step_then_token_expiration_correct(context):
    # Obter o novo token - pode estar em new_access_token ou no response
    new_token = getattr(context, 'new_access_token', None)
    
    if not new_token:
        # Tentar extrair do response
        if hasattr(context, 'refresh_response'):
            data = context.refresh_response.json()
            new_token = data.get('access_token') or data.get('access')
    
    assert new_token, "Novo access token não encontrado"
    
    # Decodificar o novo token
    try:
        decoded = jwt.decode(new_token, settings.SECRET_KEY, algorithms=['HS256'])
        exp_timestamp = decoded.get('exp')
        
        assert exp_timestamp, "Token não contém data de expiração"
        
        # Calcular quanto tempo até expiração
        now = timezone.now()
        # Usar timezone-aware datetime
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.get_current_timezone())
        time_until_exp = (exp_datetime - now).total_seconds() / 60  # em minutos
        
        # Verificar se está entre 59 e 61 minutos (margem de 1 minuto)
        assert 59 <= time_until_exp <= 61, \
            f"Token deve expirar em 60 minutos, mas expira em {time_until_exp:.1f} minutos"
    except jwt.InvalidTokenError as e:
        raise AssertionError(f"Erro ao decodificar token: {e}")
