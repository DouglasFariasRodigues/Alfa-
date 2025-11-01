"""
Steps para cadastro de membros e geração de documentos.
Testa cadastro com dados pessoais e geração automática de cartão de membro, 
transferência de igreja e registro.
"""
from behave import given, when, then
from app_Alfa.models import Admin, Membro, DocumentoMembro
from datetime import datetime

# Admin cadastra novo membro com dados pessoais (tabela)
@when('o Admin cadastra um membro com os seguintes dados')
def step_when_admin_registers_member(context):
    # Cria Admin se não existir
    if not hasattr(context, 'admin'):
        context.admin = Admin.objects.create(
            nome="Admin Test",
            email="admin@test.com",
            senha="password123"
        )
    
    # Parsear dados da tabela Gherkin
    # Behave trata primeira linha como heading, então incluímos ela também
    dados = {}
    
    # Adicionar heading (primeira linha) como dados
    if hasattr(context.table, 'headings') and len(context.table.headings) >= 2:
        dados[context.table.headings[0]] = context.table.headings[1]
    
    # Adicionar demais linhas da tabela
    for row in context.table:
        cells = list(row.cells)
        if len(cells) >= 2:
            dados[cells[0]] = cells[1]
    
    # Parsear data de batismo se existir
    data_batismo = None
    if 'data_batismo' in dados:
        try:
            data_batismo = datetime.strptime(dados['data_batismo'], '%Y-%m-%d').date()
        except:
            data_batismo = None
    
    # Criar membro com dados pessoais seguros
    context.membro = Membro.objects.create(
        nome=dados.get('nome', 'Sem nome'),
        cpf=dados.get('cpf'),
        email=dados.get('email'),
        telefone=dados.get('telefone'),
        data_batismo=data_batismo,
        cadastrado_por=context.admin,
        status=Membro.ATIVO
    )

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
    membro = Membro.objects.get(nome=nome)
    
    tipos = [DocumentoMembro.CARTAO_MEMBRO, DocumentoMembro.TRANSFERENCIA, DocumentoMembro.REGISTRO]
    for i in range(quantidade):
        DocumentoMembro.objects.create(
            membro=membro,
            tipo=tipos[i % len(tipos)],
            gerado_por=context.admin
        )

@when('o Admin gera um cartão de membro para "{nome}"')
def step_when_admin_generates_card(context, nome):
    membro = Membro.objects.get(nome=nome)
    context.documento = DocumentoMembro.objects.create(
        membro=membro,
        tipo=DocumentoMembro.CARTAO_MEMBRO,
        gerado_por=context.admin
    )

@when('o Admin gera transferência de igreja para "{nome}"')
def step_when_admin_generates_transfer(context, nome):
    membro = Membro.objects.get(nome=nome)
    context.documento = DocumentoMembro.objects.create(
        membro=membro,
        tipo=DocumentoMembro.TRANSFERENCIA,
        gerado_por=context.admin
    )

@when('o Admin gera registro para "{nome}"')
def step_when_admin_generates_register(context, nome):
    membro = Membro.objects.get(nome=nome)
    context.documento = DocumentoMembro.objects.create(
        membro=membro,
        tipo=DocumentoMembro.REGISTRO,
        gerado_por=context.admin
    )

@when('o Admin consulta os documentos de "{nome}"')
def step_when_admin_queries_documents(context, nome):
    membro = Membro.objects.get(nome=nome)
    context.documentos = list(membro.documentos.all())

@then('o membro "{nome}" deve estar cadastrado')
def step_then_member_registered(context, nome):
    membro = Membro.objects.filter(nome=nome).first()
    assert membro is not None, f"Membro {nome} não foi encontrado"

@then('o membro deve ter sido cadastrado pelo Admin')
def step_then_member_registered_by_admin(context):
    assert context.membro.cadastrado_por == context.admin, \
        "Membro não foi cadastrado pelo Admin"

@then('os dados devem estar armazenados de forma segura')
def step_then_data_stored_securely(context):
    # Verificar que os dados estão no banco
    membro = Membro.objects.get(id=context.membro.id)
    assert membro.nome is not None, "Nome não foi armazenado"
    assert membro.cpf is not None, "CPF não foi armazenado"

@then('o documento do tipo "{tipo}" deve ser gerado')
def step_then_document_generated(context, tipo):
    assert context.documento is not None, "Documento não foi gerado"
    assert context.documento.tipo == tipo, f"Tipo de documento incorreto: {context.documento.tipo}"

@then('o documento deve estar vinculado ao membro "{nome}"')
def step_then_document_linked_to_member(context, nome):
    membro = Membro.objects.get(nome=nome)
    assert context.documento.membro == membro, "Documento não está vinculado ao membro correto"

@then('o documento deve ter sido gerado pelo Admin')
def step_then_document_generated_by_admin(context):
    assert context.documento.gerado_por == context.admin, \
        "Documento não foi gerado pelo Admin"

@then('o Admin deve ver {quantidade:d} documentos')
def step_then_admin_sees_documents(context, quantidade):
    assert len(context.documentos) == quantidade, \
        f"Esperado {quantidade} documentos, encontrado {len(context.documentos)}"
