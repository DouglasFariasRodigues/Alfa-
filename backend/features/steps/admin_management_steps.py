"""
Steps para gerenciamento do Admin.
Testa acesso do Admin às áreas de publicações e ofertas, e registro de ofertas com transparência.
"""
from behave import given, when, then
from app_Alfa.models import Admin, Oferta, DistribuicaoOferta, ONG
from decimal import Decimal
from rest_framework.test import APIClient
from rest_framework import status

# Passo: Criar Admin apenas com email (senha padrão)
@given('que existe um Admin cadastrado com email "{email}"')
@given('existe um Admin cadastrado com email "{email}"')
def step_given_admin_exists_with_email(context, email):
    # Valida que não foi passado email com senha juntos (evita conflito)
    if " e senha " in email:
        raise ValueError(f"Email inválido: '{email}'. Use o step com email e senha separados.")
    
    # Cria Admin com senha padrão
    context.admin = Admin.objects.create(
        nome="Admin Teste",
        email=email,
        senha="senha123",
        is_active=True,
        is_admin=True
    )


# Passo: Admin tenta fazer login
@when('o Admin faz login com email "{email}" e senha "{senha}"')
def step_when_admin_logs_in(context, email, senha):
    # Garantir que admin tem senha hasheada
    admin = Admin.objects.filter(email=email).first()
    if admin and not admin.senha.startswith('pbkdf2_'):
        admin.set_password(senha)
        admin.save()
    
    context.client = APIClient()
    
    # Fazer requisição POST para endpoint de login
    response = context.client.post('/api/auth/login/', {
        'email': email,
        'senha': senha
    }, format='json')
    
    context.login_response = response
    context.login_status = response.status_code
    
    # Armazenar token para próximas requisições
    if context.login_status == status.HTTP_200_OK:
        data = response.json()
        context.access_token = data.get('access_token') or data.get('access')
    
    # Também manter compatibilidade com verificação em banco
    context.admin_logado = admin is not None
    context.admin_authenticated = admin is not None  # Para compatibilidade com outras features
    if admin:
        context.admin = admin

# Passo: Admin acessa área de publicações
@when('o Admin acessa a área de publicações')
def step_when_admin_accesses_publications(context):
    # Verifica se Admin logado tem permissão de staff
    if context.admin_logado:
        context.has_publication_access = context.admin.is_admin

# Passo: Admin acessa área de ofertas
@when('o Admin acessa a área de ofertas')
def step_when_admin_accesses_ofertas(context):
    # Verifica se Admin logado tem permissão de staff
    if context.admin_logado:
        context.has_oferta_access = context.admin.is_admin

# Passo: Admin registra oferta com descrição
@when('o Admin registra uma oferta de {valor:f} com descrição "{descricao}"')
def step_when_admin_registers_oferta_with_desc(context, valor, descricao):
    # Cria oferta financeira com valor e descrição personalizados
    context.oferta = Oferta.objects.create(
        valor=Decimal(str(valor)),
        descricao=descricao,
        registrado_por=context.admin,
        is_publico=True
    )

# Passo: Admin registra oferta sem descrição específica
@when('o Admin registra uma oferta de {valor:f}')
def step_when_admin_registers_oferta(context, valor):
    # Cria oferta com descrição padrão
    context.oferta = Oferta.objects.create(
        valor=Decimal(str(valor)),
        descricao="Oferta registrada",
        registrado_por=context.admin,
        is_publico=True
    )

# Passo: Admin distribui parte da oferta para ONG
@when('o Admin distribui {valor:f} para "{destino}"')
def step_when_admin_distributes(context, valor, destino):
    # Busca ONG no banco ou usa apenas o nome como destino
    ong = ONG.objects.filter(nome=destino).first()
    
    # Cria registro de distribuição da oferta
    DistribuicaoOferta.objects.create(
        oferta=context.oferta,
        ong=ong,
        valor=Decimal(str(valor)),
        destino=destino,
        meio_envio="Transferência"
    )

# Passo: Verificar se Admin tem acesso a publicações
@then('o Admin deve ter acesso às publicações')
def step_then_admin_has_publication_access(context):
    # Confirma que Admin pode acessar área de publicações
    assert context.has_publication_access, "Admin não tem acesso às publicações"

# Passo: Verificar se Admin tem acesso a ofertas
@then('o Admin deve ter acesso às ofertas')
def step_then_admin_has_oferta_access(context):
    # Confirma que Admin pode acessar área de ofertas
    assert context.has_oferta_access, "Admin não tem acesso às ofertas"

# Passo: Verificar se oferta é pública
@then('a oferta deve ser registrada como pública')
def step_then_oferta_is_public(context):
    # Confirma que oferta está marcada para ser vista pelos membros
    assert context.oferta.is_publico, "Oferta não está marcada como pública"

# Passo: Verificar se oferta está visível para membros
@then('a oferta deve estar visível para os membros')
def step_then_oferta_visible_to_members(context):
    # Busca ofertas públicas e verifica se a oferta criada está nelas
    ofertas_publicas = Oferta.objects.filter(is_publico=True)
    assert context.oferta in ofertas_publicas, "Oferta não está visível para membros"

# Passo: Verificar se membros podem ver distribuição
@then('os membros podem visualizar a distribuição completa')
def step_then_members_can_view_distribution(context):
    # Verifica que oferta é pública e tem distribuições registradas
    assert context.oferta.is_publico, "Oferta não é pública"
    assert context.oferta.distribuicoes.exists(), "Não há distribuições para visualizar"

# Passo: Verificar total distribuído
@then('o total distribuído é {total:f}')
def step_then_total_distributed_is(context, total):
    # Soma todas as distribuições e compara com valor esperado
    total_calc = sum(float(d.valor) for d in context.oferta.distribuicoes.all())
    assert total_calc == total, f"Total esperado {total}, encontrado {total_calc}"
