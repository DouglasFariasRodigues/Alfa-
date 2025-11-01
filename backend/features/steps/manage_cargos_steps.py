"""
Steps para gerenciamento de cargos da igreja.
Testa criação e visualização de cargos como Pastor, Diácono, Líder de Louvor, etc.
"""
from behave import given, when, then
from app_alfa.models import Admin, Cargo

# Passo: Admin cria um novo cargo
@when('o Admin cria o cargo "{nome}" com descrição "{descricao}"')
def step_when_admin_creates_cargo(context, nome, descricao):
    # Cria Admin se não existir
    if not hasattr(context, 'admin'):
        context.admin = Admin.objects.create(
            nome="Admin Test",
            email="admin@test.com",
            senha="password123"
        )
    
    # Cria cargo com nome e descrição
    context.cargo = Cargo.objects.create(
        nome=nome,
        descricao=descricao,
        criado_por=context.admin
    )

# Passo: Admin solicita ver todos os cargos
@when('o Admin solicita visualizar todos os cargos')
def step_when_admin_views_cargos(context):
    # Lista todos os cargos cadastrados
    context.cargos = list(Cargo.objects.all())

# Passo: Criar cargo já cadastrado (para testes)
@given('existe o cargo "{nome}" cadastrado')
def step_given_cargo_exists(context, nome):
    # Cria Admin se não existir
    if not hasattr(context, 'admin'):
        context.admin = Admin.objects.create(
            nome="Admin Test",
            email="admin@test.com",
            senha="password123"
        )
    
    # Cria cargo pré-existente
    Cargo.objects.create(
        nome=nome,
        descricao=f"Descrição do cargo {nome}",
        criado_por=context.admin
    )

# Passo: Verificar se cargo foi cadastrado
@then('o cargo "{nome}" deve estar cadastrado')
def step_then_cargo_registered(context, nome):
    # Busca cargo no banco
    cargo = Cargo.objects.filter(nome=nome).first()
    assert cargo is not None, f"Cargo '{nome}' não foi encontrado"

# Passo: Verificar se cargo foi criado pelo Admin
@then('o cargo deve ter sido criado pelo Admin')
def step_then_cargo_created_by_admin(context):
    # Verifica que o criador do cargo é o Admin logado
    assert context.cargo.criado_por == context.admin, \
        "Cargo não foi criado pelo Admin esperado"

# Passo: Verificar quantidade total de cargos
@then('devem existir {quantidade:d} cargos cadastrados')
def step_then_cargos_count(context, quantidade):
    # Conta cargos no banco
    count = Cargo.objects.count()
    assert count == quantidade, f"Esperado {quantidade} cargos, encontrado {count}"

# Passo: Verificar quantidade de cargos visualizados
@then('o Admin deve ver {quantidade:d} cargos listados')
def step_then_admin_sees_cargos(context, quantidade):
    # Compara quantidade na lista
    assert len(context.cargos) == quantidade, \
        f"Esperado {quantidade} cargos, encontrado {len(context.cargos)}"
