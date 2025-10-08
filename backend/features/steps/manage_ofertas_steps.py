"""
Steps para gerenciamento de ofertas e distribuição para ONGs.
Testa transparência no direcionamento de valores arrecadados para instituições.
"""
from behave import given, when, then
from app_alfa.models import Admin, ONG, Oferta, DistribuicaoOferta
from decimal import Decimal
import hashlib

# Passo: Cadastrar uma ONG para receber ofertas
@given('existe uma ONG "{nome}" cadastrada')
def step_given_ong_exists(context, nome):
    # Verifica se ONG já existe para evitar duplicatas
    if not ONG.objects.filter(nome=nome).exists():
        # Gera CNPJ único baseado no nome
        import hashlib
        nome_hash = hashlib.md5(nome.encode()).hexdigest()[:8]
        cnpj_unico = f"{nome_hash[:2]}.{nome_hash[2:5]}.{nome_hash[5:8]}/0001-90"
        
        # Cria ONG com dados básicos
        ONG.objects.create(
            nome=nome,
            descricao=f"Descrição da {nome}",
            cnpj=cnpj_unico,
            email=f"contato@{nome.lower().replace(' ', '')}.org"
        )

# Passo: Criar uma oferta com valor específico
@given('existe uma oferta de valor {valor:f}')
def step_given_oferta_exists(context, valor):
    # Cria Admin se necessário
    if not hasattr(context, 'admin'):
        context.admin = Admin.objects.create(
            nome="Admin Test",
            email="admin@test.com",
            senha="password123"
        )
    
    # Registra oferta arrecadada
    context.oferta = Oferta.objects.create(
        valor=Decimal(str(valor)),
        descricao="Oferta da semana",
        registrado_por=context.admin,
        is_publico=True
    )

# Passo: Criar oferta já com distribuição para ONG
@given('existe uma oferta de valor {valor:f} com distribuição para "{nome_ong}"')
def step_given_oferta_with_distribution(context, valor, nome_ong):
    # Cria Admin se necessário
    if not hasattr(context, 'admin'):
        context.admin = Admin.objects.create(
            nome="Admin Test",
            email="admin@test.com",
            senha="password123"
        )
    
    # Cria oferta
    oferta = Oferta.objects.create(
        valor=Decimal(str(valor)),
        descricao="Oferta da semana",
        registrado_por=context.admin,
        is_publico=True
    )
    
    # Adiciona distribuição para a ONG
    ong = ONG.objects.get(nome=nome_ong)
    DistribuicaoOferta.objects.create(
        oferta=oferta,
        ong=ong,
        valor=Decimal(str(valor / 2)),
        destino=nome_ong,
        meio_envio="PIX"
    )

# Passo: Admin direciona parte da oferta para ONG
@when('o Admin direciona {valor:f} da oferta para "{destino}" via "{meio}"')
def step_when_admin_directs_oferta(context, valor, destino, meio):
    # Busca ONG destino
    ong = ONG.objects.filter(nome=destino).first()
    
    # Registra distribuição com meio de envio (PIX, transferência, etc.)
    context.distribuicao = DistribuicaoOferta.objects.create(
        oferta=context.oferta,
        ong=ong,
        valor=Decimal(str(valor)),
        destino=destino,
        meio_envio=meio
    )

# Passo: Admin visualiza todas as distribuições
@when('o Admin solicita visualizar todas as distribuições')
def step_when_admin_views_distributions(context):
    # Lista todas as distribuições cadastradas
    context.distribuicoes = list(DistribuicaoOferta.objects.all())

# Passo: Verificar se distribuição foi registrada
@then('a distribuição deve ser registrada com sucesso')
def step_then_distribution_registered(context):
    # Confirma que distribuição existe e foi salva
    assert context.distribuicao is not None, "Distribuição não foi criada"
    assert context.distribuicao.id is not None, "Distribuição não foi salva no banco"

# Passo: Verificar distribuição específica
@then('a oferta deve ter uma distribuição de {valor:f} para "{destino}"')
def step_then_oferta_has_distribution(context, valor, destino):
    # Busca distribuição para destino específico
    distribuicao = context.oferta.distribuicoes.filter(destino=destino).first()
    assert distribuicao is not None, f"Distribuição para {destino} não encontrada"
    assert float(distribuicao.valor) == valor, f"Valor esperado {valor}, encontrado {distribuicao.valor}"

# Passo: Verificar quantidade de distribuições
@then('a oferta deve ter {quantidade:d} distribuições registradas')
def step_then_oferta_has_distributions(context, quantidade):
    # Conta distribuições da oferta
    count = context.oferta.distribuicoes.count()
    assert count == quantidade, f"Esperado {quantidade} distribuições, encontrado {count}"

# Passo: Verificar total distribuído
@then('o total distribuído deve ser {total:f}')
def step_then_total_distributed(context, total):
    # Soma todos os valores distribuídos
    total_calc = sum(float(d.valor) for d in context.oferta.distribuicoes.all())
    assert total_calc == total, f"Total esperado {total}, encontrado {total_calc}"

# Passo: Verificar visualização de distribuições
@then('o Admin deve ver pelo menos {quantidade:d} distribuição')
def step_then_admin_sees_distributions(context, quantidade):
    # Verifica quantidade mínima de distribuições listadas
    assert len(context.distribuicoes) >= quantidade, \
        f"Esperado pelo menos {quantidade} distribuição, encontrado {len(context.distribuicoes)}"
