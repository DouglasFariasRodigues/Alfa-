"""
Steps para visualização de conteúdo por usuários/membros.
Testa se membros conseguem ver fotos de eventos e transparência das ofertas.
"""
from behave import given, when, then
from app_alfa.models import Usuario, Evento, FotoEvento, Postagem, FotoPostagem, Admin, Oferta, ONG, DistribuicaoOferta, Membro
from django.utils import timezone
from decimal import Decimal

# Criar usuário comum (não Admin)
@given('que existe um usuário "{nome}" cadastrado')
@given('existe um usuário "{nome}" cadastrado')
@given('existe um usuário "{nome}" cadastrado')
def step_given_usuario_exists(context, nome):
    context.usuario = Usuario.objects.create(
        username=nome.lower(),
        email=f"{nome.lower()}@test.com",
        senha="password123"
    )

@given('existe um evento "{titulo}" com {quantidade:d} fotos públicas')
def step_given_event_with_public_photos(context, titulo, quantidade):
    if not hasattr(context, 'usuario'):
        organizador = Usuario.objects.create(
            username="organizador",
            email="organizador@test.com",
            senha="password123"
        )
    else:
        organizador = context.usuario
    
    evento = Evento.objects.create(
        titulo=titulo,
        descricao=f"Descrição do {titulo}",
        data=timezone.now(),
        local="Igreja Central",
        organizador=organizador
    )
    
    for i in range(quantidade):
        FotoEvento.objects.create(
            evento=evento,
            imagem=f"eventos_fotos/foto_{i+1}.jpg",
            descricao=f"Foto {i+1}"
        )

@given('existe uma postagem "{titulo}" com {quantidade:d} fotos')
def step_given_post_with_photos(context, titulo, quantidade):
    if not hasattr(context, 'usuario'):
        autor = Usuario.objects.create(
            username="autor",
            email="autor@test.com",
            senha="password123"
        )
    else:
        autor = context.usuario
    
    postagem = Postagem.objects.create(
        titulo=titulo,
        conteudo=f"Conteúdo sobre {titulo}",
        autor=autor
    )
    
    for i in range(quantidade):
        FotoPostagem.objects.create(
            postagem=postagem,
            imagem=f"postagens_fotos/foto_{i+1}.jpg",
            descricao=f"Foto {i+1}"
        )
    
    context.postagem = postagem

@given('existe uma oferta pública de {valor:f} distribuída para ONGs')
def step_given_public_oferta_distributed(context, valor):
    admin = Admin.objects.create(
        nome="Admin Test",
        email="admin@test.com",
        senha="password123"
    )
    
    ong = ONG.objects.create(
        nome="ONG Beneficente",
        cnpj="12.345.678/0001-90"
    )
    
    oferta = Oferta.objects.create(
        valor=Decimal(str(valor)),
        descricao="Oferta semanal",
        registrado_por=admin,
        is_publico=True
    )
    
    DistribuicaoOferta.objects.create(
        oferta=oferta,
        ong=ong,
        valor=Decimal(str(valor)),
        destino=ong.nome,
        meio_envio="PIX"
    )
    
    context.oferta = oferta

@given('que existe um membro ativo na igreja')
@given('existe um membro ativo na igreja')
def step_given_active_member(context):
    context.membro = Membro.objects.create(
        dados_completos="João Silva, 30 anos, Rua A",
        status=Membro.ATIVO
    )

@given('existe uma oferta de {valor:f} com {quantidade:d} distribuições para diferentes ONGs')
def step_given_oferta_with_distributions(context, valor, quantidade):
    admin = Admin.objects.create(
        nome="Admin Test",
        email="admin@test.com",
        senha="password123"
    )
    
    oferta = Oferta.objects.create(
        valor=Decimal(str(valor)),
        descricao="Oferta mensal",
        registrado_por=admin,
        is_publico=True
    )
    
    valor_por_ong = valor / quantidade
    for i in range(quantidade):
        ong = ONG.objects.create(
            nome=f"ONG {i+1}",
            cnpj=f"12.345.678/000{i+1}-90"
        )
        
        DistribuicaoOferta.objects.create(
            oferta=oferta,
            ong=ong,
            valor=Decimal(str(valor_por_ong)),
            destino=ong.nome,
            meio_envio="Transferência"
        )
    
    context.oferta = oferta

@when('o usuário "{nome}" solicita visualizar as fotos do evento "{titulo}"')
def step_when_user_views_event_photos(context, nome, titulo):
    evento = Evento.objects.get(titulo=titulo)
    context.fotos_visualizadas = list(evento.fotos.all())

@when('o usuário "{nome}" solicita visualizar a postagem "{titulo}"')
def step_when_user_views_post(context, nome, titulo):
    context.postagem_visualizada = Postagem.objects.get(titulo=titulo)

@when('o usuário "{nome}" solicita visualizar as ofertas públicas')
def step_when_user_views_public_ofertas(context, nome):
    context.ofertas_publicas = list(Oferta.objects.filter(is_publico=True))

@when('o membro solicita visualizar a transparência das ofertas')
def step_when_member_views_transparency(context):
    context.ofertas_visiveis = list(Oferta.objects.filter(is_publico=True))

@then('o usuário deve ver {quantidade:d} fotos')
def step_then_user_sees_photos(context, quantidade):
    assert len(context.fotos_visualizadas) == quantidade, \
        f"Esperado {quantidade} fotos, encontrado {len(context.fotos_visualizadas)}"

@then('o usuário deve ver a postagem com {quantidade:d} fotos')
def step_then_user_sees_post_with_photos(context, quantidade):
    count = context.postagem_visualizada.fotos.count()
    assert count == quantidade, f"Esperado {quantidade} fotos, encontrado {count}"

@then('o usuário deve ver pelo menos {quantidade:d} oferta')
def step_then_user_sees_ofertas(context, quantidade):
    assert len(context.ofertas_publicas) >= quantidade, \
        f"Esperado pelo menos {quantidade} oferta, encontrado {len(context.ofertas_publicas)}"

@then('o usuário deve ver as distribuições da oferta')
def step_then_user_sees_distributions(context):
    distribuicoes = context.oferta.distribuicoes.all()
    assert distribuicoes.exists(), "Nenhuma distribuição encontrada"

@then('o membro deve ver a oferta com valor {valor:f}')
def step_then_member_sees_oferta_value(context, valor):
    oferta = context.ofertas_visiveis[0]
    assert float(oferta.valor) == valor, f"Esperado valor {valor}, encontrado {oferta.valor}"

@then('o membro deve ver {quantidade:d} destinos da oferta')
def step_then_member_sees_destinations(context, quantidade):
    oferta = context.ofertas_visiveis[0]
    count = oferta.distribuicoes.count()
    assert count == quantidade, f"Esperado {quantidade} destinos, encontrado {count}"
