"""
Steps para publicação de fotos de eventos pelo Admin.
Testa se Admin consegue publicar artes e fotos de eventos/cultos/missas.
"""
from behave import given, when, then
from app_Alfa.models import Admin, Usuario, Evento, FotoEvento, Postagem, FotoPostagem
from django.utils import timezone

# Criar Admin como usuário do sistema
@given('que existe um Admin logado como usuário')
@given('existe um Admin logado como usuário')
def step_given_admin_as_usuario(context):
    # Cria Admin se não existir
    if not hasattr(context, 'admin'):
        context.admin = Admin.objects.create(
            nome="Admin Test",
            email="admin@test.com",
            senha="password123"
        )
    
    # Vincula Admin a um usuário do sistema
    context.usuario = Usuario.objects.create(
        username=f"admin_{context.admin.id}",
        email=context.admin.email,
        senha=context.admin.senha
    )

# Criar evento sem fotos
@given('existe um evento "{titulo}"')
def step_given_evento_exists(context, titulo):
    # Cria usuário organizador se necessário
    if not hasattr(context, 'usuario'):
        context.usuario = Usuario.objects.create(
            username="organizador",
            email="organizador@test.com",
            senha="password123"
        )
    
    # Cria evento (culto, missa, encontro)
    Evento.objects.create(
        titulo=titulo,
        descricao=f"Descrição do {titulo}",
        data=timezone.now(),
        local="Igreja Central",
        organizador=context.usuario
    )

# Admin publica múltiplas fotos de um evento
@when('o Admin publica {quantidade:d} fotos para o evento "{titulo}"')
def step_when_admin_publishes_photos(context, quantidade, titulo):
    # Busca evento
    evento = Evento.objects.get(titulo=titulo)
    
    # Cria múltiplas fotos para o evento
    for i in range(quantidade):
        FotoEvento.objects.create(
            evento=evento,
            imagem=f"eventos_fotos/foto_{i+1}.jpg",
            descricao=f"Foto {i+1} do evento {titulo}"
        )

# Admin cria postagem com fotos
@when('o Admin cria uma postagem "{titulo}" com {quantidade:d} fotos')
def step_when_admin_creates_post_with_photos(context, titulo, quantidade):
    # Cria postagem (anúncio, notícia, etc.)
    postagem = Postagem.objects.create(
        titulo=titulo,
        conteudo=f"Conteúdo da postagem {titulo}",
        autor=context.usuario
    )
    
    # Adiciona fotos à postagem
    for i in range(quantidade):
        FotoPostagem.objects.create(
            postagem=postagem,
            imagem=f"postagens_fotos/foto_{i+1}.jpg",
            descricao=f"Foto {i+1}"
        )
    
    context.postagem = postagem

# Verifica se evento tem fotos publicadas
@then('o evento deve ter {quantidade:d} fotos publicadas')
def step_then_event_has_photos(context, quantidade):
    # Busca último evento criado
    eventos = Evento.objects.all().order_by('-id')
    if eventos.exists():
        evento = eventos.first()
        count = evento.fotos.count()
        assert count == quantidade, f"Esperado {quantidade} fotos, encontrado {count}"

# Verifica se postagem foi publicada
@then('a postagem "{titulo}" deve estar publicada')
def step_then_post_published(context, titulo):
    # Busca postagem no banco
    postagem = Postagem.objects.filter(titulo=titulo).first()
    assert postagem is not None, f"Postagem '{titulo}' não foi encontrada"

# Verifica quantidade de fotos na postagem
@then('a postagem deve ter {quantidade:d} fotos anexadas')
def step_then_post_has_photos(context, quantidade):
    # Conta fotos vinculadas à postagem
    count = context.postagem.fotos.count()
    assert count == quantidade, f"Esperado {quantidade} fotos, encontrado {count}"
