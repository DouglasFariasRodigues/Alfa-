from django.db import models

# Modelo de exemplo para usar 'models' e remover o aviso de importação não utilizada
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


class Membro(models.Model):
    dados_completos = models.TextField()
    foto = models.ImageField(upload_to='membros_fotos/', blank=True, null=True)
    status = models.BooleanField(default=True)

class Doacao(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(auto_now_add=True)
    tipo = models.CharField(max_length=50)
    membro = models.ForeignKey(Membro, related_name='doacoes', on_delete=models.CASCADE)

class Igreja(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15, blank=True, null=True)

class deleted_at(models.Model):
    deleted_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
