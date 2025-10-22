from django.core.management.base import BaseCommand
from app_alfa.models import Admin, Cargo, Membro, Evento, Transacao, Usuario
from datetime import date, datetime, timedelta

class Command(BaseCommand):
    help = 'Cria dados de teste para o sistema'

    def handle(self, *args, **options):
        # Buscar admin
        admin = Admin.objects.get(email='admin@igreja.com')
        cargo_admin = admin.cargo

        # Criar usuário para eventos
        usuario_admin, created = Usuario.objects.get_or_create(
            email='admin@igreja.com',
            defaults={
                'username': 'admin',
                'senha': 'admin123',
                'cargo': cargo_admin,
                'is_staff': True,
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Usuário admin criado!')
            )

        # Criar cargos de teste
        cargos_data = [
            {
                'nome': 'Secretário',
                'descricao': 'Responsável pela secretaria da igreja',
                'pode_registrar_dizimos': True,
                'pode_registrar_ofertas': True,
                'pode_gerenciar_membros': True,
                'pode_gerenciar_eventos': False,
                'pode_gerenciar_financas': False,
                'pode_gerenciar_cargos': False,
                'pode_gerenciar_documentos': True,
                'pode_visualizar_relatorios': True,
            },
            {
                'nome': 'Tesoureiro',
                'descricao': 'Responsável pelas finanças da igreja',
                'pode_registrar_dizimos': True,
                'pode_registrar_ofertas': True,
                'pode_gerenciar_membros': False,
                'pode_gerenciar_eventos': False,
                'pode_gerenciar_financas': True,
                'pode_gerenciar_cargos': False,
                'pode_gerenciar_documentos': False,
                'pode_visualizar_relatorios': True,
            },
            {
                'nome': 'Líder de Eventos',
                'descricao': 'Responsável pela organização de eventos',
                'pode_registrar_dizimos': False,
                'pode_registrar_ofertas': False,
                'pode_gerenciar_membros': False,
                'pode_gerenciar_eventos': True,
                'pode_gerenciar_financas': False,
                'pode_gerenciar_cargos': False,
                'pode_gerenciar_documentos': False,
                'pode_visualizar_relatorios': False,
            },
            {
                'nome': 'Membro',
                'descricao': 'Membro comum da igreja',
                'pode_registrar_dizimos': False,
                'pode_registrar_ofertas': False,
                'pode_gerenciar_membros': False,
                'pode_gerenciar_eventos': False,
                'pode_gerenciar_financas': False,
                'pode_gerenciar_cargos': False,
                'pode_gerenciar_documentos': False,
                'pode_visualizar_relatorios': False,
            }
        ]

        cargos = {}
        for cargo_data in cargos_data:
            cargo, created = Cargo.objects.get_or_create(
                nome=cargo_data['nome'],
                defaults=cargo_data
            )
            cargos[cargo_data['nome']] = cargo
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Cargo "{cargo.nome}" criado!')
                )

        # Criar membros de teste
        membros_data = [
            {
                'nome': 'Maria Silva',
                'email': 'maria@igreja.com',
                'cpf': '111.111.111-11',
                'telefone': '(11) 11111-1111',
                'senha': '123456',
            },
            {
                'nome': 'João Santos',
                'email': 'joao@igreja.com',
                'cpf': '222.222.222-22',
                'telefone': '(11) 22222-2222',
                'senha': '123456',
            },
            {
                'nome': 'Ana Costa',
                'email': 'ana@igreja.com',
                'cpf': '333.333.333-33',
                'telefone': '(11) 33333-3333',
                'senha': '123456',
            },
            {
                'nome': 'Pedro Oliveira',
                'email': 'pedro@igreja.com',
                'cpf': '444.444.444-44',
                'telefone': '(11) 44444-4444',
                'senha': '123456',
            }
        ]

        for i, membro_data in enumerate(membros_data):
            # Atribuir cargos diferentes para cada membro
            cargo_nomes = ['Membro', 'Líder de Eventos', 'Membro', 'Membro']
            cargo = cargos.get(cargo_nomes[i], cargos['Membro'])
            
            membro, created = Membro.objects.get_or_create(
                email=membro_data['email'],
                defaults={
                    **membro_data,
                    'status': 'ativo',
                    'cargo': cargo,  # Atribuir cargo ao membro
                    'cadastrado_por': admin,
                    'endereco': 'Endereço de teste',
                    'data_nascimento': '1990-01-01',
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Membro "{membro.nome}" criado!')
                )

        # Criar eventos de teste
        eventos_data = [
            {
                'titulo': 'Culto Dominical',
                'descricao': 'Culto de domingo pela manhã',
                'data': datetime.now() + timedelta(days=1),
                'local': 'Igreja Central',
                'organizador': usuario_admin,
            },
            {
                'titulo': 'Reunião de Jovens',
                'descricao': 'Encontro semanal dos jovens',
                'data': datetime.now() + timedelta(days=3),
                'local': 'Salão de Jovens',
                'organizador': usuario_admin,
            },
            {
                'titulo': 'Conferência de Mulheres',
                'descricao': 'Conferência anual das mulheres',
                'data': datetime.now() + timedelta(days=7),
                'local': 'Auditório Principal',
                'organizador': usuario_admin,
            }
        ]

        for evento_data in eventos_data:
            evento, created = Evento.objects.get_or_create(
                titulo=evento_data['titulo'],
                defaults=evento_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Evento "{evento.titulo}" criado!')
                )

        # Criar transações de teste
        transacoes_data = [
            {
                'tipo': 'entrada',
                'categoria': 'dizimo',
                'valor': 1000.00,
                'descricao': 'Dízimos do mês',
                'data': date.today(),
                'registrado_por': admin,
            },
            {
                'tipo': 'entrada',
                'categoria': 'oferta',
                'valor': 500.00,
                'descricao': 'Ofertas especiais',
                'data': date.today(),
                'registrado_por': admin,
            },
            {
                'tipo': 'saida',
                'categoria': 'manutencao',
                'valor': 200.00,
                'descricao': 'Manutenção do ar condicionado',
                'data': date.today(),
                'registrado_por': admin,
            }
        ]

        for transacao_data in transacoes_data:
            transacao, created = Transacao.objects.get_or_create(
                descricao=transacao_data['descricao'],
                data=transacao_data['data'],
                defaults=transacao_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Transação "{transacao.descricao}" criada!')
                )

        self.stdout.write(
            self.style.SUCCESS('\nDados de teste criados com sucesso!')
        )
        self.stdout.write(
            self.style.SUCCESS('\nResumo dos dados criados:')
        )
        self.stdout.write(f'Administrador: admin@igreja.com / admin123')
        self.stdout.write(f'Membros: maria@igreja.com, joao@igreja.com, ana@igreja.com, pedro@igreja.com (senha: 123456)')
        self.stdout.write(f'Cargos: Administrador, Secretário, Tesoureiro, Líder de Eventos, Membro')
        self.stdout.write(f'Eventos: Culto Dominical, Reunião de Jovens, Conferência de Mulheres')
        self.stdout.write(f'Transações: Dízimos, Ofertas, Manutenção')