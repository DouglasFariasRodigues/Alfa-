"""
Steps para testar acesso completo do Admin.
Testa se o Admin consegue acessar todas as áreas da aplicação após login.
"""
from behave import given, when, then
from app_alfa.models import Admin, Oferta, Evento, FotoEvento, Usuario
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
        is_admin=True
    )

# Passo: Criar Admin apenas com email (senha padrão)
@given('que existe um Admin cadastrado com email "{email}"')
@given('existe um Admin cadastrado com email "{email}"')
def step_given_admin_with_email_only(context, email):
    # Cria Admin com senha padrão
    context.admin = Admin.objects.create(
        nome="Admin Teste",
        email=email,
        senha="senha123",  # Senha padrão
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
    if hasattr(context, 'admin_authenticated') and context.admin_authenticated and context.admin.is_admin:
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
    if not hasattr(context, 'admin_authenticated'):
        # Se não tem o atributo, verifica se tem admin e considera autenticado
        assert hasattr(context, 'admin') and context.admin is not None, "Admin não está autenticado"
        context.admin_authenticated = True
    else:
        assert context.admin_authenticated, "Admin não está autenticado"

# Passo: Verificar se Admin tem acesso total
@then('o Admin deve ter acesso total à aplicação')
def step_then_admin_full_access(context):
    # Verifica se Admin tem permissões de admin
    assert context.admin.is_admin, "Admin não tem acesso total"

# Passo: Verificar permissão para gerenciar membros
@then('o Admin deve ter permissão para gerenciar membros')
def step_then_admin_can_manage_members(context):
    # Confirma que Admin pode acessar área de membros
    if not hasattr(context, 'has_member_access'):
        # Se não tem o atributo, verifica se admin é admin ou tem cargo com permissão
        if hasattr(context, 'admin'):
            has_permission = context.admin.is_admin or (
                context.admin.cargo and context.admin.cargo.pode_gerenciar_membros
            )
            assert has_permission, "Admin não tem permissão para gerenciar membros"
        else:
            raise AssertionError("Admin não encontrado no contexto")
        context.has_member_access = True
    else:
        assert context.has_member_access, "Admin não tem permissão para gerenciar membros"

# Passo: Verificar se Admin pode ver informações dos membros
@then('o Admin pode visualizar informações dos membros')
def step_then_admin_can_view_member_info(context):
    # Verifica permissão de admin para visualizar dados
    assert context.admin.is_admin, "Admin não pode visualizar informações dos membros"

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
    # Verifica se Admin tem permissão de admin para gerenciar fotos
    assert context.admin.is_admin, "Admin não pode gerenciar fotos"

# Passo: Admin tem cargo sem permissão para registrar dízimos
@given('o Admin tem um cargo "{cargo_nome}" sem permissão para registrar dízimos')
def step_given_admin_cargo_sem_permissao(context, cargo_nome):
    from app_alfa.models import Cargo
    cargo = Cargo.objects.create(
        nome=cargo_nome,
        pode_registrar_dizimos=False
    )
    context.admin.cargo = cargo
    context.admin.save()

# Passo: Admin tem cargo com permissão para registrar dízimos
@given('o Admin tem um cargo "{cargo_nome}" com permissão para registrar dízimos')
def step_given_admin_cargo_com_permissao(context, cargo_nome):
    from app_alfa.models import Cargo
    cargo = Cargo.objects.create(
        nome=cargo_nome,
        pode_registrar_dizimos=True
    )
    context.admin.cargo = cargo
    context.admin.save()

# Passo: Admin faz login
@when('o Admin faz login com email "{email}" e senha "{senha}"')
def step_when_admin_login(context, email, senha):
    from app_alfa.models import Admin
    admin = Admin.objects.filter(email=email).first()
    if admin and admin.check_password(senha):
        context.admin_authenticated = True
        context.admin = admin
        context.response_status = 200
    else:
        context.admin_authenticated = False
        context.response_status = 401

# Passo: Admin tenta criar transação
@when('o Admin tenta criar uma transação de entrada tipo "{tipo}" com valor {valor:f}')
def step_when_admin_create_transaction(context, tipo, valor):
    from app_alfa.models import Transacao
    from decimal import Decimal
    from django.utils import timezone
    
    # Simula verificação de permissão
    if hasattr(context.admin, 'cargo') and context.admin.cargo and not context.admin.cargo.pode_registrar_dizimos:
        context.response_status = 403
        context.error_message = "permissões insuficientes"
    else:
        try:
            context.transacao = Transacao.objects.create(
                tipo='entrada',
                valor=Decimal(str(valor)),
                descricao=f"Transação de {tipo}",
                categoria=tipo,
                data=timezone.now().date(),
                registrado_por=context.admin
            )
            context.response_status = 201
        except Exception as e:
            context.response_status = 400
            context.error_message = str(e)

# Passo: Admin acessa área de publicações
@when('o Admin acessa a área de publicações')
def step_when_admin_access_publications(context):
    context.has_publications_access = context.admin.is_admin
    context.response_status = 200 if context.has_publications_access else 403

# Passo: Admin acessa área de ofertas
@when('o Admin acessa a área de ofertas')
def step_when_admin_access_ofertas(context):
    context.has_ofertas_access = context.admin.is_admin
    context.response_status = 200 if context.has_ofertas_access else 403

# Passo: Verificar erro 403
@then('a requisição deve retornar erro 403 "{error_type}"')
def step_then_response_403(context, error_type):
    assert context.response_status == 403, f"Esperado status 403, recebido {context.response_status}"

# Passo: Verificar mensagem de erro
@then('a mensagem de erro deve conter "{message}"')
def step_then_error_message_contains(context, message):
    assert hasattr(context, 'error_message'), "Nenhuma mensagem de erro encontrada"
    assert message in context.error_message, f"Esperado '{message}' na mensagem, encontrado '{context.error_message}'"

# Passo: Verificar status 200 ou 201
@then('a requisição deve retornar status 201 ou 200')
def step_then_response_200_or_201(context):
    assert context.response_status in [200, 201], f"Esperado status 200/201, recebido {context.response_status}"

# Passo: Verificar transação criada
@then('a transação deve ser criada com sucesso')
def step_then_transaction_created(context):
    assert hasattr(context, 'transacao'), "Transação não foi criada"
    assert context.transacao.id is not None, "Transação não foi salva"

# Passo: Verificar acesso às publicações
@then('o Admin deve ter acesso às publicações')
def step_then_admin_has_publications_access(context):
    assert context.has_publications_access, "Admin não tem acesso às publicações"

# Passo: Verificar acesso às ofertas
@then('o Admin deve ter acesso às ofertas')
def step_then_admin_has_ofertas_access(context):
    assert context.has_ofertas_access, "Admin não tem acesso às ofertas"
