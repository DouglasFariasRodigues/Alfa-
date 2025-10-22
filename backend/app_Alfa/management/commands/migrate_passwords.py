from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from app_alfa.models import Admin, Usuario, Membro

class Command(BaseCommand):
    help = 'Migra senhas existentes para hash seguro'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando migração de senhas...')
        
        # Migrar senhas de Admin
        admin_count = 0
        for admin in Admin.objects.all():
            if admin.senha and not admin.senha.startswith('$'):
                admin.senha = make_password(admin.senha)
                admin.save()
                admin_count += 1
                self.stdout.write(f'Admin {admin.nome} - senha migrada')
        
        # Migrar senhas de Usuario
        usuario_count = 0
        for usuario in Usuario.objects.all():
            if usuario.senha and not usuario.senha.startswith('$'):
                usuario.senha = make_password(usuario.senha)
                usuario.save()
                usuario_count += 1
                self.stdout.write(f'Usuario {usuario.username} - senha migrada')
        
        # Migrar senhas de Membro
        membro_count = 0
        for membro in Membro.objects.all():
            if membro.senha and not membro.senha.startswith('$'):
                membro.senha = make_password(membro.senha)
                membro.save()
                membro_count += 1
                self.stdout.write(f'Membro {membro.nome} - senha migrada')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Migração concluída! {admin_count} admins, {usuario_count} usuarios, {membro_count} membros migrados.'
            )
        )
