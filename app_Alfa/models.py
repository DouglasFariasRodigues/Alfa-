from django.db import models

# Example model to use 'models' and remove the unused import warning
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
    complete_data = models.TextField()
    photo = models.ImageField(upload_to='membros_photos/', blank=True, null=True)
    status = models.BooleanField(default=True)

class Doacao(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=50)
    member = models.ForeignKey(Membro, related_name='doacoes', on_delete=models.CASCADE)

class Igreja(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=True, null=True)

class deleted_at(models.Model):
    deleted_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)