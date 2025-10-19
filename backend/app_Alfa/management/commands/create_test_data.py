from django.core.management.base import BaseCommand
from app_alfa.models import Admin, Cargo, Membro, Evento, Usuario, Transacao, Postagem

class Command(BaseCommand):
    help = 'Cria dados de teste para o sistema'

    def handle(self, *args, **options):
        self.stdout.write('Criando dados de teste...')

        # Criar cargo
        cargo, created = Cargo.objects.get_or_create(
            nome='Pastor',
            defaults={
                'descricao': 'Pastor da igreja',
                'pode_fazer_postagens': True,
                'pode_registrar_dizimos': True,
                'pode_registrar_ofertas': True,
            }
        )

        # Criar admin
        admin, created = Admin.objects.get_or_create(
            email='admin@igreja.com',
            defaults={
                'nome': 'Pastor João Silva',
                'telefone': '(11) 99999-9999',
                'cargo': cargo,
                'is_active': True,
                'is_staff': True,
                'senha': 'admin123',  # Em produção, usar hash
            }
        )

        # Criar usuário correspondente
        usuario, created = Usuario.objects.get_or_create(
            username='admin@igreja.com',
            defaults={
                'email': 'admin@igreja.com',
                'telefone': '(11) 99999-9999',
                'cargo': cargo,
                'is_active': True,
                'is_staff': True,
                'senha': 'admin123',  # Em produção, usar hash
            }
        )

        # Criar alguns membros de teste
        membros_data = [
            {
                'nome': 'Maria Santos',
                'cpf': '123.456.789-00',
                'telefone': '(11) 88888-8888',
                'email': 'maria@email.com',
                'status': 'ativo',
            },
            {
                'nome': 'João Oliveira',
                'cpf': '987.654.321-00',
                'telefone': '(11) 77777-7777',
                'email': 'joao@email.com',
                'status': 'ativo',
            },
            {
                'nome': 'Ana Costa',
                'cpf': '456.789.123-00',
                'telefone': '(11) 66666-6666',
                'email': 'ana@email.com',
                'status': 'inativo',
            },
        ]

        for membro_data in membros_data:
            Membro.objects.get_or_create(
                cpf=membro_data['cpf'],
                defaults={
                    **membro_data,
                    'cadastrado_por': admin,
                }
            )

        # Criar alguns eventos de teste
        eventos_data = [
            {
                'titulo': 'Culto de Domingo',
                'descricao': 'Culto matutino de domingo',
                'data': '2024-01-15 09:00:00',
                'local': 'Igreja Central',
            },
            {
                'titulo': 'Reunião de Jovens',
                'descricao': 'Reunião semanal dos jovens',
                'data': '2024-01-20 19:00:00',
                'local': 'Salão de Jovens',
            },
        ]

        for evento_data in eventos_data:
            Evento.objects.get_or_create(
                titulo=evento_data['titulo'],
                data=evento_data['data'],
                defaults={
                    **evento_data,
                    'organizador': usuario,
                }
            )

        # Criar algumas transações de teste
        transacoes_data = [
            {
                'tipo': 'entrada',
                'categoria': 'Dízimo',
                'valor': 500.00,
                'data': '2024-01-10',
                'descricao': 'Dízimo do mês de janeiro',
            },
            {
                'tipo': 'entrada',
                'categoria': 'Oferta',
                'valor': 200.00,
                'data': '2024-01-12',
                'descricao': 'Oferta especial',
            },
            {
                'tipo': 'saida',
                'categoria': 'Manutenção',
                'valor': 300.00,
                'data': '2024-01-14',
                'descricao': 'Reparo no sistema de som',
            },
        ]

        for transacao_data in transacoes_data:
            Transacao.objects.get_or_create(
                categoria=transacao_data['categoria'],
                data=transacao_data['data'],
                defaults={
                    **transacao_data,
                    'registrado_por': admin,
                }
            )

        # Criar algumas postagens de teste
        postagens_data = [
            {
                'titulo': 'Bem-vindos ao novo sistema!',
                'conteudo': 'Estamos felizes em apresentar o novo sistema de gestão da nossa igreja.',
            },
            {
                'titulo': 'Próximo evento: Conferência de Jovens',
                'conteudo': 'Não percam a conferência de jovens que acontecerá no próximo mês.',
            },
        ]

        for postagem_data in postagens_data:
            Postagem.objects.get_or_create(
                titulo=postagem_data['titulo'],
                defaults={
                    **postagem_data,
                    'autor': usuario,
                }
            )

        self.stdout.write(
            self.style.SUCCESS('Dados de teste criados com sucesso!')
        )
        self.stdout.write('Credenciais de login:')
        self.stdout.write('Email: admin@igreja.com')
        self.stdout.write('Senha: admin123')
