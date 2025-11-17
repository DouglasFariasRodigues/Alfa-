"""
Steps para doações de usuários/membros.
Testa se membros conseguem fazer doações para grupos e ofertas da igreja.
"""
from behave import given, when, then
from app_alfa.models import Usuario, Membro, Grupo, Doacao, Admin, Oferta
from decimal import Decimal

# Criar grupo para receber doações (Missões, Construção, etc.)
@given('existe um grupo "{nome}" cadastrado')
def step_given_grupo_exists(context, nome):
    if not Grupo.objects.filter(nome=nome).exists():
        Grupo.objects.create(
            nome=nome,
            descricao=f"Descrição do grupo {nome}"
        )

@given('existe um membro vinculado ao usuário "{nome}"')
def step_given_member_linked_to_user(context, nome):
    usuario = Usuario.objects.get(username=nome.lower())
    
    # Criar membro vinculado
    context.membro = Membro.objects.create(
        nome=nome,
        email=usuario.email,
        status=Membro.ATIVO
    )

# Step já definido em manage_members_status_steps.py
# @given('que existe um membro ativo "{nome}"')
# @given('existe um membro ativo "{nome}"')

@given('o membro "{nome}" fez {quantidade:d} doações para o grupo "{grupo_nome}"')
def step_given_member_made_donations(context, nome, quantidade, grupo_nome):
    membro = Membro.objects.get(nome=nome)
    grupo = Grupo.objects.get(nome=grupo_nome)
    
    for i in range(quantidade):
        Doacao.objects.create(
            membro=membro,
            grupo=grupo,
            valor=Decimal('50.00'),
            tipo='oferta'
        )

@when('o usuário "{nome}" realiza uma doação de {valor:f} para o grupo "{grupo_nome}"')
def step_when_user_donates(context, nome, valor, grupo_nome):
    membro = Membro.objects.get(nome=nome)
    grupo = Grupo.objects.get(nome=grupo_nome)
    
    context.doacao = Doacao.objects.create(
        membro=membro,
        grupo=grupo,
        valor=Decimal(str(valor)),
        tipo='doacao'
    )

@when('o usuário "{nome}" realiza uma oferta de {valor:f}')
def step_when_user_makes_oferta(context, nome, valor):
    # Criar admin se não existir
    if not Admin.objects.exists():
        admin = Admin.objects.create(
            nome="Admin Sistema",
            email="admin@sistema.com",
            senha="password123"
        )
    else:
        admin = Admin.objects.first()
    
    context.oferta = Oferta.objects.create(
        valor=Decimal(str(valor)),
        descricao=f"Oferta de {nome}",
        registrado_por=admin,
        is_publico=True
    )

@when('o membro "{nome}" consulta seu histórico de doações')
def step_when_member_queries_donations(context, nome):
    membro = Membro.objects.get(nome=nome)
    context.doacoes = list(membro.doacoes.all())

@when('o membro "{nome}" doa {valor:f} para "{grupo_nome}"')
def step_when_member_donates(context, nome, valor, grupo_nome):
    membro = Membro.objects.get(nome=nome)
    grupo = Grupo.objects.get(nome=grupo_nome)
    
    Doacao.objects.create(
        membro=membro,
        grupo=grupo,
        valor=Decimal(str(valor)),
        tipo='doacao'
    )

@then('a doação deve ser registrada com sucesso')
def step_then_donation_registered(context):
    assert context.doacao is not None, "Doação não foi registrada"
    assert context.doacao.id is not None, "Doação não foi salva no banco"

@then('a doação deve estar vinculada ao membro de "{nome}"')
def step_then_donation_linked_to_member(context, nome):
    membro = Membro.objects.get(nome=nome)
    assert context.doacao.membro == membro, "Doação não está vinculada ao membro correto"

@then('o valor da doação deve ser {valor:f}')
def step_then_donation_value(context, valor):
    assert float(context.doacao.valor) == valor, \
        f"Valor esperado {valor}, encontrado {context.doacao.valor}"

@then('a oferta deve ser registrada')
def step_then_oferta_registered(context):
    assert context.oferta is not None, "Oferta não foi registrada"

# Step já definido em admin_full_access_steps.py
# @then('a oferta deve ter valor {valor:f}')

@then('a oferta deve estar visível publicamente')
def step_then_oferta_public(context):
    assert context.oferta.is_publico, "Oferta não está pública"

@then('o membro deve ver {quantidade:d} doações registradas')
def step_then_member_sees_donations(context, quantidade):
    assert len(context.doacoes) == quantidade, \
        f"Esperado {quantidade} doações, encontrado {len(context.doacoes)}"

@then('o membro "{nome}" deve ter {quantidade:d} doações registradas')
def step_then_member_has_donations(context, nome, quantidade):
    membro = Membro.objects.get(nome=nome)
    count = membro.doacoes.count()
    assert count == quantidade, f"Esperado {quantidade} doações, encontrado {count}"

@then('o total doado deve ser {total:f}')
def step_then_total_donated(context, total):
    membro = Membro.objects.filter(doacoes__isnull=False).distinct().first()
    total_calc = sum(float(d.valor) for d in membro.doacoes.all())
    assert total_calc == total, f"Total esperado {total}, encontrado {total_calc}"

# Steps para gerenciamento de ofertas pelo Admin
@given('que existe um Admin logado')
def step_given_admin_logged(context):
    if not hasattr(context, 'admin'):
        context.admin = Admin.objects.create(
            nome="Admin Logado",
            email="admin@logado.com",
            senha="senha123",
            is_admin=True
        )
    context.admin_authenticated = True

@given('existe uma ONG "{nome}" cadastrada')
def step_given_ong_exists(context, nome):
    from app_alfa.models import ONG
    if not ONG.objects.filter(nome=nome).exists():
        ONG.objects.create(
            nome=nome,
            descricao=f"Descrição da {nome}",
            email=f"contato@{nome.lower().replace(' ', '')}.com"
        )

@given('existe uma oferta de valor {valor:f}')
def step_given_oferta_value(context, valor):
    if not hasattr(context, 'admin'):
        context.admin = Admin.objects.first() or Admin.objects.create(
            nome="Admin Sistema",
            email="admin@sistema.com",
            senha="senha123"
        )
    context.oferta = Oferta.objects.create(
        valor=Decimal(str(valor)),
        descricao="Oferta teste",
        registrado_por=context.admin,
        is_publico=True
    )

@given('existe uma oferta de valor {valor:f} com distribuição para "{ong_nome}"')
def step_given_oferta_with_distribution(context, valor, ong_nome):
    from app_alfa.models import ONG, DistribuicaoOferta
    if not hasattr(context, 'admin'):
        context.admin = Admin.objects.first() or Admin.objects.create(
            nome="Admin Sistema",
            email="admin@sistema.com",
            senha="senha123"
        )
    
    ong = ONG.objects.get(nome=ong_nome)
    context.oferta = Oferta.objects.create(
        valor=Decimal(str(valor)),
        descricao="Oferta com distribuição",
        registrado_por=context.admin,
        is_publico=True
    )
    
    DistribuicaoOferta.objects.create(
        oferta=context.oferta,
        ong=ong,
        valor=Decimal(str(valor)),
        destino=ong_nome,
        meio_envio="Transferência bancária"
    )

@when('o Admin registra uma oferta de {valor:f} com descrição "{descricao}"')
def step_when_admin_registers_oferta(context, valor, descricao):
    context.oferta = Oferta.objects.create(
        valor=Decimal(str(valor)),
        descricao=descricao,
        registrado_por=context.admin,
        is_publico=True
    )

@when('o Admin registra uma oferta de {valor:f}')
def step_when_admin_registers_oferta_simple(context, valor):
    context.oferta = Oferta.objects.create(
        valor=Decimal(str(valor)),
        descricao="Oferta registrada",
        registrado_por=context.admin,
        is_publico=True
    )

@when('o Admin distribui {valor:f} para "{ong_nome}"')
def step_when_admin_distributes_to_ong(context, valor, ong_nome):
    from app_alfa.models import ONG, DistribuicaoOferta
    ong = ONG.objects.get(nome=ong_nome)
    
    if not hasattr(context, 'distribuicoes'):
        context.distribuicoes = []
    
    distribuicao = DistribuicaoOferta.objects.create(
        oferta=context.oferta,
        ong=ong,
        valor=Decimal(str(valor)),
        destino=ong_nome,
        meio_envio="Transferência bancária"
    )
    context.distribuicoes.append(distribuicao)

@when('o Admin direciona {valor:f} da oferta para "{ong_nome}" via "{forma_pagamento}"')
def step_when_admin_directs_to_ong(context, valor, ong_nome, forma_pagamento):
    from app_alfa.models import ONG, DistribuicaoOferta
    ong = ONG.objects.get(nome=ong_nome)
    
    if not hasattr(context, 'distribuicoes'):
        context.distribuicoes = []
    
    distribuicao = DistribuicaoOferta.objects.create(
        oferta=context.oferta,
        ong=ong,
        valor=Decimal(str(valor)),
        destino=ong_nome,
        meio_envio=forma_pagamento
    )
    context.distribuicoes.append(distribuicao)

@when('o Admin solicita visualizar todas as distribuições')
def step_when_admin_views_distributions(context):
    from app_alfa.models import DistribuicaoOferta
    context.all_distributions = list(DistribuicaoOferta.objects.all())

@then('a oferta deve ser registrada como pública')
def step_then_oferta_public_flag(context):
    assert context.oferta.is_publico, "Oferta não está marcada como pública"

@then('a oferta deve estar visível para os membros')
def step_then_oferta_visible_to_members(context):
    oferta = Oferta.objects.get(id=context.oferta.id)
    assert oferta.is_publico, "Oferta não está visível para membros"

@then('os membros podem visualizar a distribuição completa')
def step_then_members_can_view_distribution(context):
    # Verifica se oferta é pública
    assert context.oferta.is_publico, "Membros não podem visualizar distribuição"

@then('o total distribuído é {total:f}')
def step_then_total_distributed_is(context, total):
    from app_alfa.models import DistribuicaoOferta
    total_calc = sum(float(d.valor) for d in context.distribuicoes)
    assert total_calc == total, f"Total esperado {total}, encontrado {total_calc}"

@then('a distribuição deve ser registrada com sucesso')
def step_then_distribution_registered(context):
    assert len(context.distribuicoes) > 0, "Distribuição não foi registrada"
    assert context.distribuicoes[-1].id is not None, "Distribuição não foi salva"

@then('a oferta deve ter uma distribuição de {valor:f} para "{ong_nome}"')
def step_then_oferta_has_distribution(context, valor, ong_nome):
    from app_alfa.models import ONG, DistribuicaoOferta
    ong = ONG.objects.get(nome=ong_nome)
    distribuicao = DistribuicaoOferta.objects.filter(oferta=context.oferta, ong=ong, valor=Decimal(str(valor))).first()
    assert distribuicao is not None, f"Distribuição de {valor} para {ong_nome} não encontrada"

@then('a oferta deve ter {quantidade:d} distribuições registradas')
def step_then_oferta_has_distributions_count(context, quantidade):
    from app_alfa.models import DistribuicaoOferta
    count = DistribuicaoOferta.objects.filter(oferta=context.oferta).count()
    assert count == quantidade, f"Esperado {quantidade} distribuições, encontrado {count}"

@then('o total distribuído deve ser {total:f}')
def step_then_total_distributed(context, total):
    from app_alfa.models import DistribuicaoOferta
    total_calc = sum(float(d.valor) for d in DistribuicaoOferta.objects.filter(oferta=context.oferta))
    assert total_calc == total, f"Total esperado {total}, encontrado {total_calc}"

@then('o Admin deve ver pelo menos {quantidade:d} distribuição')
def step_then_admin_sees_distributions(context, quantidade):
    assert len(context.all_distributions) >= quantidade, f"Esperado pelo menos {quantidade} distribuições"
