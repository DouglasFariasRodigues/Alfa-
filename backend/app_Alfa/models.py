from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
import re
from .validators import (
    validate_cpf, validate_phone, validate_email_domain, 
    validate_rg, validate_cep, validate_age
)

def validate_password_strength(value):
    """Validador de força de senha - VERSÃO RELAXADA"""
    # Apenas verificar tamanho mínimo
    if len(value) < 4:
        raise ValidationError('A senha deve ter pelo menos 4 caracteres.')
    
    # Verificar apenas senhas muito comuns e perigosas
    dangerous_passwords = ['123', 'abc', '1234', 'admin', 'root', 'password']
    if value.lower() in dangerous_passwords:
        raise ValidationError('Esta senha é muito comum. Escolha uma senha mais segura.')

class PasswordHashMixin:
    """Mixin para hash automático de senhas com integração Django Auth"""
    
    def set_password(self, raw_password):
        """Define uma senha com hash automático"""
        self.senha = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Verifica se a senha está correta"""
        return check_password(raw_password, self.senha)
    
    def save(self, *args, **kwargs):
        # Se a senha foi alterada e não está hasheada, fazer hash
        if hasattr(self, 'senha') and self.senha and not self.senha.startswith('pbkdf2_'):
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)
    
    def is_authenticated(self):
        """Verifica se o usuário está autenticado"""
        return True
    
    def is_anonymous(self):
        """Verifica se o usuário é anônimo"""
        return False
    
    def get_username(self):
        """Retorna o username para compatibilidade com Django Auth"""
        if hasattr(self, 'email'):
            return self.email
        elif hasattr(self, 'username'):
            return self.username
        return str(self.id)

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(editable=False, blank=True, null=True)
    is_active = models.BooleanField(editable=False, default=True)
    
    # Campos de auditoria - serão adicionados em migração futura
    # created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_created')
    # updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_updated')
    
    objects = SoftDeleteManager()
    
    class Meta:
        abstract = True
    
    def delete(self, **kwargs):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()
        
    def hard_delete(self, **kwargs):
        super(BaseModel, self).delete(**kwargs)

class UserBaseModel(BaseModel):
    """Modelo base para todos os usuários do sistema"""
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    senha = models.CharField(max_length=128, validators=[validate_password_strength], help_text="Senha deve ter pelo menos 6 caracteres, conter letras e números")
    last_login = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True
    
    def set_password(self, raw_password):
        """Define uma senha com hash automático"""
        from django.contrib.auth.hashers import make_password
        self.senha = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Verifica se a senha está correta"""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.senha)
    
    def save(self, *args, **kwargs):
        # Se a senha foi alterada e não está hasheada, fazer hash
        if hasattr(self, 'senha') and self.senha and not self.senha.startswith('pbkdf2_'):
            from django.contrib.auth.hashers import make_password
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)
    
    def is_authenticated(self):
        """Verifica se o usuário está autenticado"""
        return True
    
    def is_anonymous(self):
        """Verifica se o usuário é anônimo"""
        return False
    
    def get_username(self):
        """Retorna o username para compatibilidade com Django Auth"""
        return self.email
class Cargo(BaseModel):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)

    # Permissões
    pode_registrar_dizimos = models.BooleanField(default=False, help_text="Pode registrar dízimos")
    pode_registrar_ofertas = models.BooleanField(default=False, help_text="Pode registrar ofertas")
    pode_gerenciar_membros = models.BooleanField(default=False, help_text="Pode gerenciar membros")
    pode_gerenciar_eventos = models.BooleanField(default=False, help_text="Pode gerenciar eventos")
    pode_gerenciar_financas = models.BooleanField(default=False, help_text="Pode gerenciar finanças")
    pode_gerenciar_cargos = models.BooleanField(default=False, help_text="Pode gerenciar cargos")
    pode_gerenciar_documentos = models.BooleanField(default=False, help_text="Pode gerenciar documentos")
    pode_visualizar_relatorios = models.BooleanField(default=False, help_text="Pode visualizar relatórios")

class Admin(BaseModel):
    """Administrador/Pastor - Acesso completo ao sistema"""
    nome = models.CharField(max_length=100, help_text="Nome completo do administrador")
    email = models.EmailField(unique=True, validators=[EmailValidator(), validate_email_domain], help_text="Email válido")
    telefone = models.CharField(max_length=15, blank=True, null=True, validators=[validate_phone], help_text="Telefone com DDD (10 ou 11 dígitos)")
    senha = models.CharField(max_length=128, validators=[validate_password_strength], help_text="Senha deve ter pelo menos 6 caracteres, conter letras e números")
    last_login = models.DateTimeField(null=True, blank=True)
    cargo = models.ForeignKey('app_alfa.Cargo', on_delete=models.PROTECT, null=True, blank=True, related_name='admins')
    is_admin = models.BooleanField(default=True, help_text="Indica se é administrador do sistema")
    
    def set_password(self, raw_password):
        """Define uma senha com hash automático"""
        from django.contrib.auth.hashers import make_password
        self.senha = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Verifica se a senha está correta"""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.senha)
    
    def save(self, *args, **kwargs):
        # Se a senha foi alterada e não está hasheada, fazer hash
        if hasattr(self, 'senha') and self.senha and not self.senha.startswith('pbkdf2_'):
            from django.contrib.auth.hashers import make_password
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)

class Usuario(BaseModel):
    """Colaborador/Staff - Usuário com permissões específicas baseadas no cargo"""
    username = models.CharField(max_length=150, unique=True, help_text="Nome de usuário único")
    email = models.EmailField(unique=True, validators=[EmailValidator(), validate_email_domain], help_text="Email válido")
    telefone = models.CharField(max_length=15, blank=True, null=True, validators=[validate_phone], help_text="Telefone com DDD (10 ou 11 dígitos)")
    senha = models.CharField(max_length=128, validators=[validate_password_strength], help_text="Senha deve ter pelo menos 6 caracteres, conter letras e números")
    last_login = models.DateTimeField(null=True, blank=True)
    cargo = models.ForeignKey('app_alfa.Cargo', on_delete=models.PROTECT, null=True, blank=True, related_name='usuarios')
    is_staff = models.BooleanField(default=True, help_text="Indica se é staff/colaborador")
    
    def set_password(self, raw_password):
        """Define uma senha com hash automático"""
        from django.contrib.auth.hashers import make_password
        self.senha = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Verifica se a senha está correta"""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.senha)
    
    def save(self, *args, **kwargs):
        # Se a senha foi alterada e não está hasheada, fazer hash
        if hasattr(self, 'senha') and self.senha and not self.senha.startswith('pbkdf2_'):
            from django.contrib.auth.hashers import make_password
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)


class Membro(BaseModel):
    """Membro comum da igreja - Acesso limitado baseado em permissões"""
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
    nome = models.CharField(max_length=200, help_text="Nome completo do membro")
    cpf = models.CharField(max_length=14, blank=True, null=True, help_text="CPF (opcional)")
    rg = models.CharField(max_length=20, blank=True, null=True, help_text="RG (opcional)")
    data_nascimento = models.DateField(blank=True, null=True, help_text="Data de nascimento (opcional)")
    telefone = models.CharField(max_length=15, blank=True, null=True, help_text="Telefone (opcional)")
    email = models.EmailField(validators=[EmailValidator()], help_text="Email válido")
    endereco = models.TextField(blank=True, null=True, help_text="Endereço completo")
    senha = models.CharField(max_length=128, blank=True, null=True, validators=[validate_password_strength], help_text="Senha para acesso ao sistema. Deve ter pelo menos 6 caracteres, conter letras e números")
    last_login = models.DateTimeField(null=True, blank=True)
    
    dados_completos = models.TextField(blank=True, null=True)  # Campo legado
    foto = models.ImageField(upload_to='membros_fotos/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ATIVO)
    
    def set_password(self, raw_password):
        """Define uma senha com hash automático"""
        from django.contrib.auth.hashers import make_password
        self.senha = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Verifica se a senha está correta"""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.senha)
    
    def save(self, *args, **kwargs):
        # Se a senha foi alterada e não está hasheada, fazer hash
        if hasattr(self, 'senha') and self.senha and not self.senha.startswith('pbkdf2_'):
            from django.contrib.auth.hashers import make_password
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)
    
    # Dados da igreja
    data_batismo = models.DateField(blank=True, null=True)
    igreja_origem = models.CharField(max_length=200, blank=True, null=True)
    cargo = models.ForeignKey('app_alfa.Cargo', on_delete=models.PROTECT, null=True, blank=True, related_name='membros', help_text="Cargo do membro na igreja")
    cadastrado_por = models.ForeignKey('app_alfa.Admin', on_delete=models.PROTECT, null=True, blank=True, related_name='membros_cadastrados')

class DocumentoMembro(models.Model):
    CARTAO_MEMBRO = 'cartao_membro'
    TRANSFERENCIA = 'transferencia'
    REGISTRO = 'registro'
    TIPO_CHOICES = [
        (CARTAO_MEMBRO, 'Cartão de Membro'),
        (TRANSFERENCIA, 'Transferência de Igreja'),
        (REGISTRO, 'Registro de Membro'),
    ]
    
    membro = models.ForeignKey('app_alfa.Membro', on_delete=models.CASCADE, related_name='documentos')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    arquivo = models.FileField(upload_to='documentos_membros/', blank=True, null=True)
    gerado_em = models.DateTimeField(auto_now_add=True)
    gerado_por = models.ForeignKey('app_alfa.Admin', on_delete=models.SET_NULL, null=True, related_name='documentos_gerados')

class Grupo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

class Doacao(BaseModel):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(auto_now_add=True)
    tipo = models.CharField(max_length=50)
    membro = models.ForeignKey('app_alfa.Membro', related_name='doacoes', on_delete=models.CASCADE)
    grupo = models.ForeignKey('app_alfa.Grupo', on_delete=models.CASCADE, related_name='doacoes')

class Igreja(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15, blank=True, null=True)

class Evento(BaseModel):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data = models.DateTimeField()
    local = models.CharField(max_length=255, blank=True, null=True)
    organizador = models.ForeignKey('app_alfa.Usuario', on_delete=models.CASCADE, related_name='eventos')
    foto = models.ImageField(upload_to='eventos_fotos/', blank=True, null=True)

class FotoEvento(models.Model):
    evento = models.ForeignKey('app_alfa.Evento', on_delete=models.CASCADE, related_name='fotos')
    imagem = models.ImageField(upload_to='eventos_fotos/')
    descricao = models.CharField(max_length=255, blank=True, null=True)
    data_upload = models.DateTimeField(auto_now_add=True)

class Postagem(BaseModel):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    autor = models.ForeignKey('app_alfa.Usuario', on_delete=models.CASCADE, related_name='postagens')
    data_publicacao = models.DateTimeField(auto_now_add=True)

class FotoPostagem(models.Model):
    postagem = models.ForeignKey('app_alfa.Postagem', on_delete=models.CASCADE, related_name='fotos')
    imagem = models.ImageField(upload_to='postagens_fotos/')
    descricao = models.CharField(max_length=255, blank=True, null=True)
    data_upload = models.DateTimeField(auto_now_add=True)



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
    registrado_por = models.ForeignKey('app_alfa.Admin', on_delete=models.SET_NULL, null=True, related_name='ofertas_registradas')
    is_publico = models.BooleanField(default=True)

class DistribuicaoOferta(models.Model):
    oferta = models.ForeignKey('app_alfa.Oferta', on_delete=models.CASCADE, related_name='distribuicoes')
    ong = models.ForeignKey('app_alfa.ONG', on_delete=models.CASCADE, related_name='distribuicoes', blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    destino = models.CharField(max_length=200)
    meio_envio = models.CharField(max_length=100, blank=True, null=True)
    data_envio = models.DateField(blank=True, null=True)
    comprovante = models.FileField(upload_to='comprovantes_ofertas/', blank=True, null=True)

class Transferencia(BaseModel):
    membro = models.ForeignKey('app_alfa.Membro', on_delete=models.CASCADE)
    igreja_origem = models.ForeignKey('app_alfa.Igreja', on_delete=models.CASCADE, related_name='transferencias_origem')
    igreja_destino = models.ForeignKey('app_alfa.Igreja', on_delete=models.CASCADE, related_name='transferencias_destino')
    data_transferencia = models.DateField()
    motivo = models.TextField(blank=True)
    gerado_por = models.ForeignKey('app_alfa.Admin', on_delete=models.SET_NULL, null=True, related_name='transferencias_geradas')

class Transacao(BaseModel):
    ENTRADA = 'entrada'
    SAIDA = 'saida'
    TIPO_CHOICES = [
        (ENTRADA, 'Entrada'),
        (SAIDA, 'Saída'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    descricao = models.TextField(blank=True, null=True)
    metodo_pagamento = models.CharField(max_length=50, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    registrado_por = models.ForeignKey('app_alfa.Admin', on_delete=models.SET_NULL, null=True, related_name='transacoes_registradas')

class EventoPresenca(BaseModel):
    """Modelo para confirmação de presença em eventos"""
    evento = models.ForeignKey('app_alfa.Evento', on_delete=models.CASCADE, related_name='presencas')
    membro = models.ForeignKey('app_alfa.Membro', on_delete=models.CASCADE, related_name='presencas_eventos')
    confirmado = models.BooleanField(default=False)
    data_confirmacao = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['evento', 'membro']  # Um membro só pode confirmar presença uma vez por evento

class EventoComentario(BaseModel):
    """Modelo para comentários em eventos"""
    evento = models.ForeignKey('app_alfa.Evento', on_delete=models.CASCADE, related_name='comentarios')
    membro = models.ForeignKey('app_alfa.Membro', on_delete=models.CASCADE, related_name='comentarios_eventos')
    comentario = models.TextField()
    data_comentario = models.DateTimeField(auto_now_add=True)
    aprovado = models.BooleanField(default=True)  # Comentários são aprovados por padrão
