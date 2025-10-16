"""
Steps de teste para login do Admin.
Testa se o Admin consegue fazer login com credenciais corretas ou incorretas.
"""
from behave import given, when, then
from app_Alfa.models import Admin

# Passo: Criar um Admin no banco de dados para testar
@given('que existe um Admin com email "{email}" e senha "{senha}"')
def step_given_admin_exists(context, email, senha):
    # Cria um novo Admin com os dados fornecidos
    Admin.objects.create(nome="Admin Test", email=email, senha=senha)

# Passo: Tentar fazer login com email e senha
@when('eu tento fazer login com email "{email}" e senha "{senha}"')
def step_when_attempt_login(context, email, senha):
    # Verifica se existe um Admin com essas credenciais no banco
    context.login_success = Admin.objects.filter(email=email, senha=senha).exists()

# Passo: Verificar se o login foi bem-sucedido
@then('eu devo estar logado com sucesso')
def step_then_logged_in(context):
    # Confirma que as credenciais estavam corretas
    assert context.login_success, "Login should be successful with valid credentials"

# Passo: Verificar se o login falhou
@then('eu devo ver uma mensagem de erro de login')
def step_then_error(context):
    # Confirma que as credenciais estavam incorretas
    assert not context.login_success, "Login should fail with invalid credentials"
