from django.core.management.base import BaseCommand
from app_Alfa.models import Membro, Cargo, Admin

class Command(BaseCommand):
    help = 'Cria um membro com senha para teste'

    def handle(self, *args, **options):
        # Criar um cargo de teste se não existir
        cargo, created = Cargo.objects.get_or_create(
            nome='Membro Teste',
            defaults={
                'descricao': 'Cargo para membros de teste',
                'pode_registrar_dizimos': False,
                'pode_registrar_ofertas': False,
                'pode_gerenciar_membros': False,
                'pode_gerenciar_eventos': True,  # Pode gerenciar eventos
                'pode_gerenciar_financas': False,
                'pode_gerenciar_cargos': False,
                'pode_gerenciar_documentos': False,
                'pode_visualizar_relatorios': True,  # Pode visualizar relatórios
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Cargo "{cargo.nome}" criado com sucesso!')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Cargo "{cargo.nome}" já existe.')
            )

        # Buscar um admin para ser o criador
        admin = Admin.objects.first()
        if not admin:
            self.stdout.write(
                self.style.ERROR('Nenhum admin encontrado. Crie um admin primeiro.')
            )
            return

        # Criar membro com senha
        membro, created = Membro.objects.get_or_create(
            email='membro.teste@igreja.com',
            defaults={
                'nome': 'João Silva',
                'cpf': '111.222.333-55',
                'telefone': '(11) 99999-9999',
                'endereco': 'Rua das Flores, 123',
                'data_nascimento': '1990-01-01',
                'status': 'ativo',
                'senha': '123456',  # Senha simples para teste
                'cargo': cargo,  # Atribuir cargo ao membro
                'cadastrado_por': admin,
                'dados_completos': 'Membro criado para teste do sistema de login'
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Membro "{membro.nome}" criado com sucesso!')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Email: {membro.email}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Senha: {membro.senha}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Cargo: {cargo.nome}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Membro com email "{membro.email}" já existe.')
            )
