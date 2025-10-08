from django.db import models
from django.utils import timezone

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(editable=False, blank=True, null=True)
    is_active = models.BooleanField(editable=False, default=True)
    
    objects = SoftDeleteManager()
    
    class Meta:
        abstract = True
    
    def delete(self, **kwargs):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()
        
    def hard_delete(self, **kwargs):
        super(BaseModel, self).delete(**kwargs)
class Admin(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=15, blank=True, null=True)
    cargo = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    senha = models.CharField(max_length=128)

class Usuario(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    cargo = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    senha = models.CharField(max_length=128)


class Membro(BaseModel):
    ATIVO = 'ativo'
    INATIVO = 'inativo'
    FALECIDO = 'falecido'
    AFASTADO = 'afastado'  # Pessoas que deixaram a fé
    STATUS_CHOICES = [
        (ATIVO, 'Ativo'),
        (INATIVO, 'Inativo'),
        (FALECIDO, 'Falecido'),
        (AFASTADO, 'Afastado'),
    ]
    
    # Dados pessoais
    nome = models.CharField(max_length=200, blank=True, null=True)
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    
    dados_completos = models.TextField(blank=True, null=True)  # Campo legado
    foto = models.ImageField(upload_to='membros_fotos/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ATIVO)
    
    # Dados da igreja
    data_batismo = models.DateField(blank=True, null=True)
    igreja_origem = models.CharField(max_length=200, blank=True, null=True)
    cadastrado_por = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True, related_name='membros_cadastrados')

class DocumentoMembro(models.Model):
    CARTAO_MEMBRO = 'cartao_membro'
    TRANSFERENCIA = 'transferencia'
    REGISTRO = 'registro'
    TIPO_CHOICES = [
        (CARTAO_MEMBRO, 'Cartão de Membro'),
        (TRANSFERENCIA, 'Transferência de Igreja'),
        (REGISTRO, 'Registro de Membro'),
    ]
    
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE, related_name='documentos')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    arquivo = models.FileField(upload_to='documentos_membros/', blank=True, null=True)
    gerado_em = models.DateTimeField(auto_now_add=True)
    gerado_por = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, related_name='documentos_gerados')

class Grupo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

class Doacao(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(auto_now_add=True)
    tipo = models.CharField(max_length=50)
    membro = models.ForeignKey(Membro, related_name='doacoes', on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='doacoes')

class Igreja(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15, blank=True, null=True)

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data = models.DateTimeField()
    local = models.CharField(max_length=255, blank=True, null=True)
    organizador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='eventos')
    foto = models.ImageField(upload_to='eventos_fotos/', blank=True, null=True)

class FotoEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='fotos')
    imagem = models.ImageField(upload_to='eventos_fotos/')
    descricao = models.CharField(max_length=255, blank=True, null=True)
    data_upload = models.DateTimeField(auto_now_add=True)

class Postagem(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='postagens')
    data_publicacao = models.DateTimeField(auto_now_add=True)

class FotoPostagem(models.Model):
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE, related_name='fotos')
    imagem = models.ImageField(upload_to='postagens_fotos/')
    descricao = models.CharField(max_length=255, blank=True, null=True)
    data_upload = models.DateTimeField(auto_now_add=True)

class Cargo(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    criado_por = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, related_name='cargos_criados')
    data_criacao = models.DateTimeField(auto_now_add=True)

class ONG(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    cnpj = models.CharField(max_length=18, unique=True, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

class Oferta(BaseModel):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(auto_now_add=True)
    descricao = models.TextField(blank=True, null=True)
    registrado_por = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, related_name='ofertas_registradas')
    is_publico = models.BooleanField(default=True)

class DistribuicaoOferta(models.Model):
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, related_name='distribuicoes')
    ong = models.ForeignKey(ONG, on_delete=models.CASCADE, related_name='distribuicoes', blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    destino = models.CharField(max_length=200)
    meio_envio = models.CharField(max_length=100, blank=True, null=True)
    data_envio = models.DateField(blank=True, null=True)
    comprovante = models.FileField(upload_to='comprovantes_ofertas/', blank=True, null=True)
