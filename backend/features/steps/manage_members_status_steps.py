"""
Steps para gerenciamento de status dos membros.
Testa gerenciamento de membros ativos, inativos, falecidos e que deixaram a fé.
"""
from behave import given, when, then
from app_Alfa.models import Admin, Membro

# Passo: Criar múltiplos membros ativos
@given('existem {quantidade:d} membros ativos cadastrados')
def step_given_active_members(context, quantidade):
    # Cria Admin se não existir
    if not hasattr(context, 'admin'):
        context.admin = Admin.objects.create(
            nome="Admin Test",
            email="admin@test.com",
            senha="password123"
        )
    
    # Cria vários membros com status ativo
    for i in range(quantidade):
        Membro.objects.create(
            nome=f"Membro Ativo {i+1}",
            status=Membro.ATIVO,
            cadastrado_por=context.admin
        )

# Passo: Criar múltiplos membros inativos
@given('existem {quantidade:d} membros inativos cadastrados')
def step_given_inactive_members(context, quantidade):
    # Cria Admin se não existir
    if not hasattr(context, 'admin'):
        context.admin = Admin.objects.create(
            nome="Admin Test",
            email="admin@test.com",
            senha="password123"
        )
    
    # Cria vários membros que não frequentam mais
    for i in range(quantidade):
        Membro.objects.create(
            nome=f"Membro Inativo {i+1}",
            status=Membro.INATIVO,
            cadastrado_por=context.admin
        )

# Passo: Criar múltiplos membros falecidos
@given('existem {quantidade:d} membros falecidos cadastrados')
def step_given_deceased_members(context, quantidade):
    # Cria Admin se não existir
    if not hasattr(context, 'admin'):
        context.admin = Admin.objects.create(
            nome="Admin Test",
            email="admin@test.com",
            senha="password123"
        )
    
    # Cria registros de membros que faleceram
    for i in range(quantidade):
        Membro.objects.create(
            nome=f"Membro Falecido {i+1}",
            status=Membro.FALECIDO,
            cadastrado_por=context.admin
        )

# Passo: Criar múltiplos membros que deixaram a fé
@given('existem {quantidade:d} membros afastados da fé cadastrados')
def step_given_away_members(context, quantidade):
    # Cria Admin se não existir
    if not hasattr(context, 'admin'):
        context.admin = Admin.objects.create(
            nome="Admin Test",
            email="admin@test.com",
            senha="password123"
        )
    
    # Cria registros de membros que se afastaram da igreja
    for i in range(quantidade):
        Membro.objects.create(
            nome=f"Membro Afastado {i+1}",
            status=Membro.AFASTADO,
            cadastrado_por=context.admin
        )

# Passo: Criar um membro ativo com nome específico
@given('que existe um membro ativo "{nome}"')
@given('existe um membro ativo "{nome}"')
def step_given_active_member_named(context, nome):
    # Cria Admin se não existir
    if not hasattr(context, 'admin'):
        context.admin = Admin.objects.create(
            nome="Admin Test",
            email="admin@test.com",
            senha="password123"
        )
    
    # Cria membro com nome específico
    Membro.objects.create(
        nome=nome,
        status=Membro.ATIVO,
        cadastrado_por=context.admin
    )

# Passo: Admin visualiza estatísticas de membros
@when('o Admin solicita visualizar estatísticas de membros')
def step_when_admin_views_statistics(context):
    # Conta membros por status
    context.stats = {
        'ativos': Membro.objects.filter(status=Membro.ATIVO).count(),
        'inativos': Membro.objects.filter(status=Membro.INATIVO).count(),
        'falecidos': Membro.objects.filter(status=Membro.FALECIDO).count(),
        'afastados': Membro.objects.filter(status=Membro.AFASTADO).count(),
    }

# Passo: Admin altera membro para inativo
@when('o Admin altera o status de "{nome}" para inativo')
def step_when_admin_changes_to_inactive(context, nome):
    # Busca membro e altera status
    membro = Membro.objects.get(nome=nome)
    membro.status = Membro.INATIVO
    membro.save()
    context.membro = membro

# Passo: Admin altera membro para afastado da fé
@when('o Admin altera o status de "{nome}" para afastado')
def step_when_admin_changes_to_away(context, nome):
    # Busca membro e marca como afastado da fé
    membro = Membro.objects.get(nome=nome)
    membro.status = Membro.AFASTADO
    membro.save()
    context.membro = membro

# Passo: Verificar quantidade de membros ativos
@then('o Admin deve ver {quantidade:d} membros ativos')
def step_then_see_active_members(context, quantidade):
    # Compara quantidade de membros ativos
    assert context.stats['ativos'] == quantidade, \
        f"Esperado {quantidade} membros ativos, encontrado {context.stats['ativos']}"

# Passo: Verificar quantidade de membros inativos
@then('o Admin deve ver {quantidade:d} membros inativos')
def step_then_see_inactive_members(context, quantidade):
    # Compara quantidade de membros inativos
    assert context.stats['inativos'] == quantidade, \
        f"Esperado {quantidade} membros inativos, encontrado {context.stats['inativos']}"

# Passo: Verificar quantidade de membros falecidos
@then('o Admin deve ver {quantidade:d} membros falecidos')
def step_then_see_deceased_members(context, quantidade):
    # Compara quantidade de membros falecidos
    assert context.stats['falecidos'] == quantidade, \
        f"Esperado {quantidade} membros falecidos, encontrado {context.stats['falecidos']}"

# Passo: Verificar quantidade de membros afastados
@then('o Admin deve ver {quantidade:d} membros afastados')
def step_then_see_away_members(context, quantidade):
    # Compara quantidade de membros que deixaram a fé
    assert context.stats['afastados'] == quantidade, \
        f"Esperado {quantidade} membros afastados, encontrado {context.stats['afastados']}"

# Passo: Verificar se membro está inativo
@then('o membro "{nome}" deve ter status inativo')
def step_then_member_is_inactive(context, nome):
    # Busca membro e verifica status
    membro = Membro.objects.get(nome=nome)
    assert membro.status == Membro.INATIVO, f"Membro {nome} não está inativo"

# Passo: Verificar se membro está afastado
@then('o membro "{nome}" deve ter status afastado')
def step_then_member_is_away(context, nome):
    # Busca membro e verifica se deixou a fé
    membro = Membro.objects.get(nome=nome)
    assert membro.status == Membro.AFASTADO, f"Membro {nome} não está afastado"

# Passo: Verificar se membro está na lista de afastados
@then('o membro deve estar na lista de pessoas que deixaram a fé')
def step_then_member_in_away_list(context):
    # Busca todos afastados e verifica se membro está incluído
    afastados = Membro.objects.filter(status=Membro.AFASTADO)
    assert context.membro in afastados, "Membro não está na lista de afastados"
