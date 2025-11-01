from django.core.management.base import BaseCommand
from app_Alfa.models import Admin, Cargo

class Command(BaseCommand):
    help = 'Cria um administrador padrão'

    def handle(self, *args, **options):
        # Criar cargo de administrador
        cargo_admin, created = Cargo.objects.get_or_create(
            nome='Administrador',
            defaults={
                'descricao': 'Administrador do sistema com acesso total',
                'pode_registrar_dizimos': True,
                'pode_registrar_ofertas': True,
                'pode_gerenciar_membros': True,
                'pode_gerenciar_eventos': True,
                'pode_gerenciar_financas': True,
                'pode_gerenciar_cargos': True,
                'pode_gerenciar_documentos': True,
                'pode_visualizar_relatorios': True,
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Cargo "{cargo_admin.nome}" criado com sucesso!')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Cargo "{cargo_admin.nome}" já existe.')
            )

        # Criar administrador
        admin, created = Admin.objects.get_or_create(
            email='admin@igreja.com',
            defaults={
                'nome': 'Administrador',
                'senha': 'admin123',
                'telefone': '(11) 99999-9999',
                'cargo': cargo_admin,
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Administrador "{admin.nome}" criado com sucesso!')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Email: {admin.email}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Senha: {admin.senha}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Administrador com email "{admin.email}" já existe.')
            )
