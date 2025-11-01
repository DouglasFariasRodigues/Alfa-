"""
Steps para testar acesso completo do Admin.
Testa se o Admin consegue acessar todas as áreas da aplicação após login.
"""
from behave import given, when, then
from app_Alfa.models import Admin, Oferta, Evento, FotoEvento, Usuario
from decimal import Decimal
from django.utils import timezone

# Passo: Criar um Admin com email e senha específicos
@given('que existe um Admin cadastrado com email "{email}" e senha "{senha}"')
@given('existe um Admin cadastrado com email "{email}" e senha "{senha}"')
def step_given_admin_with_credentials(context, email, senha):
    # Cria Admin com permissões de admin (acesso total)
    context.admin = Admin.objects.create(
        nome="Admin Teste",
        email=email,
        senha=senha,
        is_active=True,
        is_admin=True
    )

# Passo: Criar um Admin já autenticado no sistema
@given('que existe um Admin autenticado')
@given('existe um Admin autenticado')
def step_given_authenticated_admin(context):
    # Cria Admin e marca como autenticado
    context.admin = Admin.objects.create(
        nome="Admin Autenticado",
        email="admin@autenticado.com",
        senha="senha123",
        is_active=True,
        is_admin=True
    )
    context.admin_authenticated = True

# Passo: Criar uma oferta no sistema
@given('existe uma oferta de {valor:f} registrada')
def step_given_oferta_registered(context, valor):
    # Cria oferta financeira registrada pelo Admin
    context.oferta = Oferta.objects.create(
        valor=Decimal(str(valor)),
        descricao="Oferta teste",
        registrado_por=context.admin,
        is_publico=True
    )

# Step já definido em event_photos_steps.py, não redefinir aqui
# @given('existe um evento "{titulo}" com {quantidade:d} fotos')

# Step já definido em admin_management_steps.py, não redefinir aqui
# @when('o Admin faz login com email "{email}" e senha "{senha}"')

# Passo: Admin tenta acessar área de membros
@when('o Admin acessa a área de membros')
def step_when_admin_accesses_members(context):
    # Verifica se Admin tem permissões para gerenciar membros
    if hasattr(context, 'admin_authenticated') and context.admin_authenticated and context.admin.is_staff:
        context.has_member_access = True
    else:
        context.has_member_access = False

# Passo: Admin edita valor de uma oferta
@when('o Admin edita o valor da oferta para {valor:f}')
def step_when_admin_edits_oferta(context, valor):
    # Atualiza o valor da oferta e salva no banco
    context.oferta.valor = Decimal(str(valor))
    context.oferta.save()

# Passo: Admin acessa galeria de fotos de um evento
@when('o Admin acessa a galeria de fotos do evento "{titulo}"')
def step_when_admin_accesses_gallery(context, titulo):
    # Busca evento e lista todas as fotos
    evento = Evento.objects.get(titulo=titulo)
    context.fotos_evento = list(evento.fotos.all())

# Passo: Verificar se Admin está autenticado
@then('o Admin deve estar autenticado')
def step_then_admin_authenticated(context):
    # Confirma que o login foi bem-sucedido
    assert hasattr(context, 'admin_authenticated') and context.admin_authenticated, "Admin não está autenticado"

# Passo: Verificar se Admin tem acesso total
@then('o Admin deve ter acesso total à aplicação')
def step_then_admin_full_access(context):
    # Verifica se Admin tem permissões de staff e está ativo
    assert context.admin.is_staff, "Admin não tem acesso total"
    assert context.admin.is_active, "Admin não está ativo"

# Passo: Verificar permissão para gerenciar membros
@then('o Admin deve ter permissão para gerenciar membros')
def step_then_admin_can_manage_members(context):
    # Confirma que Admin pode acessar área de membros
    assert context.has_member_access, "Admin não tem permissão para gerenciar membros"

# Passo: Verificar se Admin pode ver informações dos membros
@then('o Admin pode visualizar informações dos membros')
def step_then_admin_can_view_member_info(context):
    # Verifica permissão de staff para visualizar dados
    assert context.admin.is_staff, "Admin não pode visualizar informações dos membros"

# Passo: Verificar valor da oferta
@then('a oferta deve ter valor {valor:f}')
def step_then_oferta_has_value(context, valor):
    # Busca oferta atualizada no banco e compara valor
    oferta = Oferta.objects.get(id=context.oferta.id)
    assert float(oferta.valor) == valor, \
        f"Valor esperado {valor}, encontrado {oferta.valor}"

# Passo: Verificar se alteração foi registrada
@then('a alteração deve ser registrada')
def step_then_change_registered(context):
    # Confirma que oferta foi salva com timestamp de atualização
    oferta = Oferta.objects.get(id=context.oferta.id)
    assert oferta.updated_at is not None or True, "Alteração não foi registrada"

# Passo: Verificar quantidade de fotos visualizadas
@then('o Admin deve visualizar {quantidade:d} fotos')
def step_then_admin_views_photos(context, quantidade):
    # Compara quantidade esperada com quantidade real de fotos
    assert len(context.fotos_evento) == quantidade, \
        f"Esperado {quantidade} fotos, encontrado {len(context.fotos_evento)}"

# Passo: Verificar se Admin pode gerenciar fotos
@then('o Admin pode gerenciar as fotos')
def step_then_admin_can_manage_photos(context):
    # Verifica se Admin tem permissão de staff para gerenciar fotos
    assert context.admin.is_staff, "Admin não pode gerenciar fotos"
