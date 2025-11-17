"""
Steps para gerenciamento de status dos membros.
Testa gerenciamento de membros ativos, inativos, falecidos e que deixaram a fé.
"""
from behave import given, when, then
from app_alfa.models import Admin, Membro

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

# Steps para cadastro de membros
@given('existe um membro cadastrado "{nome}"')
def step_given_member_registered(context, nome):
    if not hasattr(context, 'admin'):
        context.admin = Admin.objects.create(
            nome="Admin Test",
            email="admin@test.com",
            senha="password123"
        )
    
    Membro.objects.create(
        nome=nome,
        status=Membro.ATIVO,
        cadastrado_por=context.admin
    )

@given('o membro "{nome}" tem {quantidade:d} documentos gerados')
def step_given_member_has_documents(context, nome, quantidade):
    from app_alfa.models import DocumentoMembro
    membro = Membro.objects.get(nome=nome)
    
    tipos = ['cartao_membro', 'transferencia', 'registro']
    for i in range(quantidade):
        DocumentoMembro.objects.create(
            membro=membro,
            tipo=tipos[i % len(tipos)],
            arquivo=f"documentos/doc_{i+1}.pdf",
            gerado_por=context.admin
        )

@when('o Admin cadastra um membro com os seguintes dados')
def step_when_admin_registers_member_with_data(context):
    # Pega dados da tabela no cenário (formato vertical: campo | valor)
    dados = {}
    
    # Behave trata a primeira linha como headings
    # Para tabela vertical sem headings explícitos, Behave usa a primeira linha
    # Então vamos adicionar os headings como dados
    if hasattr(context.table, 'headings') and len(context.table.headings) >= 2:
        # A primeira linha se tornou headings, então vamos adicionar manualmente
        dados[context.table.headings[0]] = context.table.headings[1]
    
    # Agora processar as outras linhas normalmente
    for row in context.table:
        if len(row.cells) >= 2:
            campo = row.cells[0].strip()
            valor = row.cells[1].strip()
            dados[campo] = valor
    
    context.novo_membro = Membro.objects.create(
        nome=dados.get('nome', 'Nome Padrão'),
        email=dados.get('email', 'teste@email.com'),
        telefone=dados.get('telefone', ''),
        endereco=dados.get('endereço', dados.get('endereco', '')),
        cpf=dados.get('cpf', ''),
        status=Membro.ATIVO,
        cadastrado_por=context.admin
    )

@when('o Admin gera um cartão de membro para "{nome}"')
def step_when_admin_generates_card(context, nome):
    from app_alfa.models import DocumentoMembro
    membro = Membro.objects.get(nome=nome)
    
    context.documento = DocumentoMembro.objects.create(
        membro=membro,
        tipo='cartao_membro',
        arquivo=f"documentos/cartao_{membro.id}.pdf",
        gerado_por=context.admin
    )

@when('o Admin gera transferência de igreja para "{nome}"')
def step_when_admin_generates_transfer(context, nome):
    from app_alfa.models import DocumentoMembro
    membro = Membro.objects.get(nome=nome)
    
    context.documento = DocumentoMembro.objects.create(
        membro=membro,
        tipo='transferencia',
        arquivo=f"documentos/transferencia_{membro.id}.pdf",
        gerado_por=context.admin
    )

@when('o Admin gera registro para "{nome}"')
def step_when_admin_generates_registro(context, nome):
    from app_alfa.models import DocumentoMembro
    membro = Membro.objects.get(nome=nome)
    
    context.documento = DocumentoMembro.objects.create(
        membro=membro,
        tipo='registro',
        arquivo=f"documentos/registro_{membro.id}.pdf",
        gerado_por=context.admin
    )

@when('o Admin consulta os documentos de "{nome}"')
def step_when_admin_queries_documents(context, nome):
    from app_alfa.models import DocumentoMembro
    membro = Membro.objects.get(nome=nome)
    context.documentos = list(membro.documentos.all())

@then('o membro "{nome}" deve estar cadastrado')
def step_then_member_registered(context, nome):
    # Primeiro verifica se foi salvo no contexto
    if hasattr(context, 'novo_membro'):
        assert context.novo_membro.nome == nome, f"Nome não corresponde: esperado '{nome}', encontrado '{context.novo_membro.nome}'"
        assert context.novo_membro.id is not None, "Membro não foi salvo no banco"
    
    # Depois busca no banco para confirmar
    membro = Membro.objects.filter(nome=nome).first()
    assert membro is not None, f"Membro '{nome}' não foi encontrado no banco"

@then('o membro deve ter sido cadastrado pelo Admin')
def step_then_member_registered_by_admin(context):
    assert context.novo_membro.cadastrado_por == context.admin, \
        "Membro não foi cadastrado pelo Admin"

@then('os dados devem estar armazenados de forma segura')
def step_then_data_stored_securely(context):
    # Verifica se membro foi salvo no banco
    membro = Membro.objects.get(id=context.novo_membro.id)
    assert membro is not None, "Dados não foram armazenados"

@then('o documento do tipo "{tipo}" deve ser gerado')
def step_then_document_type_generated(context, tipo):
    assert context.documento.tipo == tipo, \
        f"Esperado documento tipo '{tipo}', encontrado '{context.documento.tipo}'"

@then('o documento deve estar vinculado ao membro "{nome}"')
def step_then_document_linked_to_member(context, nome):
    membro = Membro.objects.get(nome=nome)
    assert context.documento.membro == membro, \
        "Documento não está vinculado ao membro correto"

@then('o documento deve ter sido gerado pelo Admin')
def step_then_document_generated_by_admin(context):
    assert context.documento.gerado_por == context.admin, \
        "Documento não foi gerado pelo Admin"

@then('o Admin deve ver {quantidade:d} documentos')
def step_then_admin_sees_documents(context, quantidade):
    assert len(context.documentos) == quantidade, \
        f"Esperado {quantidade} documentos, encontrado {len(context.documentos)}"
