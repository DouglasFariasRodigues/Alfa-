from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count, Q
from django.forms import PasswordInput
from .models import (Admin, Usuario, Membro, Grupo, Doacao, Igreja, Evento, 
                     Postagem, FotoEvento, FotoPostagem, Cargo, ONG, Oferta, DistribuicaoOferta,
                     DocumentoMembro, Transacao)

# Registre seus modelos aqui.

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'get_cargo_nome', 'get_status_badge', 'get_telefone_formatado', 'is_active', 'created_at')
    search_fields = ('nome', 'email', 'telefone', 'cargo__nome')
    list_filter = ('is_active', 'is_admin', 'cargo', 'created_at')
    ordering = ('-created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'email', 'telefone')
        }),
        ('Permissões', {
            'fields': ('is_active', 'is_admin', 'cargo'),
            'classes': ('collapse',)
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_cargo_nome(self, obj):
        if obj.cargo:
            return format_html(
                '<span style="color: #007cba;">{}</span>',
                obj.cargo.nome
            )
        return format_html('<span style="color: #999;">Sem cargo</span>')
    get_cargo_nome.short_description = 'Cargo'
    get_cargo_nome.admin_order_field = 'cargo__nome'
    
    def get_status_badge(self, obj):
        if obj.is_active and obj.is_admin:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">ADMIN ATIVO</span>'
            )
        elif obj.is_active:
            return format_html(
                '<span style="background: #17a2b8; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">ATIVO</span>'
            )
        else:
            return format_html(
                '<span style="background: #dc3545; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">INATIVO</span>'
            )
    get_status_badge.short_description = 'Status'
    
    def get_telefone_formatado(self, obj):
        if obj.telefone:
            return format_html('<span style="font-family: monospace;">{}</span>', obj.telefone)
        return '-'
    get_telefone_formatado.short_description = 'Telefone'

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'get_cargo_nome', 'is_active', 'is_staff', 'created_at')
    search_fields = ('username', 'email', 'cargo__nome')
    list_filter = ('is_active', 'is_staff', 'cargo')

    def get_cargo_nome(self, obj):
        return obj.cargo.nome if obj.cargo else 'Sem cargo'
    get_cargo_nome.short_description = 'Cargo'
    get_cargo_nome.admin_order_field = 'cargo__nome'

@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'get_cpf_formatado', 'get_cargo_nome', 'get_status_badge', 'get_telefone_formatado', 'status', 'cadastrado_por')
    search_fields = ('nome', 'cpf', 'email', 'telefone', 'dados_completos', 'cargo__nome', 'cadastrado_por__nome')
    list_filter = ('status', 'data_batismo', 'cargo', 'cadastrado_por', 'created_at')
    list_editable = ('status',)
    ordering = ('-created_at',)
    list_per_page = 30
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'cpf', 'email', 'telefone', 'endereco', 'data_nascimento')
        }),
        ('Acesso e Segurança', {
            'fields': ('senha', 'last_login')
        }),
        ('Status e Cargo', {
            'fields': ('status', 'cargo', 'data_batismo')
        }),
        ('Dados Adicionais', {
            'fields': ('dados_completos', 'cadastrado_por'),
            'classes': ('collapse',)
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')
    actions = ['ativar_membros', 'desativar_membros', 'exportar_dados']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'senha' in form.base_fields:
            form.base_fields['senha'].widget = PasswordInput(attrs={'placeholder': 'Digite a senha'})
        return form
    
    def get_cpf_formatado(self, obj):
        if obj.cpf:
            cpf = obj.cpf.replace('.', '').replace('-', '')
            return format_html(
                '<span style="font-family: monospace;">{}.{}.{}-{}</span>',
                cpf[:3], cpf[3:6], cpf[6:9], cpf[9:]
            )
        return '-'
    get_cpf_formatado.short_description = 'CPF'
    
    def get_cargo_nome(self, obj):
        if obj.cargo:
            return format_html(
                '<span style="color: #007cba;">{}</span>',
                obj.cargo.nome
            )
        return format_html('<span style="color: #999;">Sem cargo</span>')
    get_cargo_nome.short_description = 'Cargo'
    get_cargo_nome.admin_order_field = 'cargo__nome'
    
    def get_status_badge(self, obj):
        status_colors = {
            'ativo': '#28a745',
            'inativo': '#dc3545',
            'pendente': '#ffc107',
            'suspenso': '#6c757d'
        }
        color = status_colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.status.upper()
        )
    get_status_badge.short_description = 'Status'
    
    def get_telefone_formatado(self, obj):
        if obj.telefone:
            return format_html('<span style="font-family: monospace;">{}</span>', obj.telefone)
        return '-'
    get_telefone_formatado.short_description = 'Telefone'
    
    def ativar_membros(self, request, queryset):
        updated = queryset.update(status='ativo')
        self.message_user(request, f'{updated} membros foram ativados.')
    ativar_membros.short_description = 'Ativar membros selecionados'
    
    def desativar_membros(self, request, queryset):
        updated = queryset.update(status='inativo')
        self.message_user(request, f'{updated} membros foram desativados.')
    desativar_membros.short_description = 'Desativar membros selecionados'
    
    def exportar_dados(self, request, queryset):
        # Implementar exportação de dados
        self.message_user(request, f'Exportação de {queryset.count()} membros iniciada.')
    exportar_dados.short_description = 'Exportar dados dos membros selecionados'

@admin.register(DocumentoMembro)
class DocumentoMembroAdmin(admin.ModelAdmin):
    list_display = ('membro', 'tipo', 'gerado_em', 'gerado_por')
    search_fields = ('membro__nome', 'tipo')
    list_filter = ('tipo', 'gerado_em')

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome', 'descricao')

@admin.register(Doacao)
class DoacaoAdmin(admin.ModelAdmin):
    list_display = ('membro', 'valor', 'tipo', 'data', 'grupo')
    search_fields = ('membro__dados_completos', 'tipo', 'grupo__nome')
    list_filter = ('tipo', 'data', 'grupo')

@admin.register(Igreja)
class IgrejaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco', 'telefone')
    search_fields = ('nome', 'endereco')

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'get_data_formatada', 'local', 'organizador', 'get_participantes_count')
    search_fields = ('titulo', 'descricao', 'local', 'organizador__username')
    list_filter = ('data', 'organizador', 'created_at')
    list_editable = ('local',)
    ordering = ('-data',)
    list_per_page = 25
    
    fieldsets = (
        ('Informações do Evento', {
            'fields': ('titulo', 'descricao', 'data', 'local')
        }),
        ('Organização', {
            'fields': ('organizador',),
            'classes': ('collapse',)
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')
    actions = ['duplicar_eventos', 'exportar_eventos']
    
    def get_data_formatada(self, obj):
        return obj.data.strftime('%d/%m/%Y %H:%M')
    get_data_formatada.short_description = 'Data'
    get_data_formatada.admin_order_field = 'data'
    
    def get_participantes_count(self, obj):
        count = obj.presencas.count()
        if count > 0:
            return format_html(
                '<span style="background: #007cba; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{} participantes</span>',
                count
            )
        return format_html('<span style="color: #999;">0 participantes</span>')
    get_participantes_count.short_description = 'Participantes'
    
    def duplicar_eventos(self, request, queryset):
        count = 0
        for evento in queryset:
            # Criar cópia do evento
            novo_evento = Evento.objects.create(
                titulo=f"{evento.titulo} (Cópia)",
                descricao=evento.descricao,
                data=evento.data,
                local=evento.local,
                organizador=evento.organizador
            )
            count += 1
        self.message_user(request, f'{count} eventos duplicados com sucesso.')
    duplicar_eventos.short_description = 'Duplicar eventos selecionados'
    
    def exportar_eventos(self, request, queryset):
        self.message_user(request, f'Exportação de {queryset.count()} eventos iniciada.')
    exportar_eventos.short_description = 'Exportar eventos selecionados'

@admin.register(FotoEvento)
class FotoEventoAdmin(admin.ModelAdmin):
    list_display = ('evento', 'descricao', 'data_upload')
    search_fields = ('evento__titulo', 'descricao')
    list_filter = ('data_upload', 'evento')

@admin.register(Postagem)
class PostagemAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data_publicacao')
    search_fields = ('titulo', 'conteudo', 'autor__username')
    list_filter = ('data_publicacao', 'autor')

@admin.register(FotoPostagem)
class FotoPostagemAdmin(admin.ModelAdmin):
    list_display = ('postagem', 'descricao', 'data_upload')
    search_fields = ('postagem__titulo', 'descricao')
    list_filter = ('data_upload',)

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'get_permissoes_badges', 'get_membros_count', 'pode_registrar_dizimos', 'pode_registrar_ofertas', 'pode_gerenciar_membros', 'pode_gerenciar_eventos', 'created_at')
    search_fields = ('nome', 'descricao')
    list_filter = ('created_at', 'pode_registrar_dizimos', 'pode_registrar_ofertas', 'pode_gerenciar_membros', 'pode_gerenciar_eventos', 'pode_gerenciar_financas', 'pode_gerenciar_cargos')
    list_editable = ('pode_registrar_dizimos', 'pode_registrar_ofertas', 'pode_gerenciar_membros', 'pode_gerenciar_eventos')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao')
        }),
        ('Permissões Financeiras', {
            'fields': ('pode_registrar_dizimos', 'pode_registrar_ofertas', 'pode_gerenciar_financas'),
            'classes': ('collapse',)
        }),
        ('Permissões de Gestão', {
            'fields': ('pode_gerenciar_membros', 'pode_gerenciar_eventos', 'pode_gerenciar_cargos', 'pode_gerenciar_documentos'),
            'classes': ('collapse',)
        }),
        ('Permissões de Visualização', {
            'fields': ('pode_visualizar_relatorios',),
            'classes': ('collapse',)
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_permissoes_badges(self, obj):
        permissoes = []
        if obj.pode_registrar_dizimos:
            permissoes.append('<span style="background: #28a745; color: white; padding: 1px 4px; border-radius: 2px; font-size: 10px;">DÍZIMOS</span>')
        if obj.pode_registrar_ofertas:
            permissoes.append('<span style="background: #17a2b8; color: white; padding: 1px 4px; border-radius: 2px; font-size: 10px;">OFERTAS</span>')
        if obj.pode_gerenciar_membros:
            permissoes.append('<span style="background: #007cba; color: white; padding: 1px 4px; border-radius: 2px; font-size: 10px;">MEMBROS</span>')
        if obj.pode_gerenciar_eventos:
            permissoes.append('<span style="background: #6f42c1; color: white; padding: 1px 4px; border-radius: 2px; font-size: 10px;">EVENTOS</span>')
        if obj.pode_gerenciar_financas:
            permissoes.append('<span style="background: #fd7e14; color: white; padding: 1px 4px; border-radius: 2px; font-size: 10px;">FINANÇAS</span>')
        if obj.pode_gerenciar_cargos:
            permissoes.append('<span style="background: #dc3545; color: white; padding: 1px 4px; border-radius: 2px; font-size: 10px;">CARGOS</span>')
        
        if permissoes:
            return format_html(' '.join(permissoes))
        return format_html('<span style="color: #999;">Nenhuma permissão</span>')
    get_permissoes_badges.short_description = 'Permissões'
    
    def get_membros_count(self, obj):
        count = obj.membro_set.count()
        if count > 0:
            return format_html(
                '<span style="background: #007cba; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{} membros</span>',
                count
            )
        return format_html('<span style="color: #999;">0 membros</span>')
    get_membros_count.short_description = 'Membros'
    get_membros_count.admin_order_field = 'membro__count'

@admin.register(ONG)
class ONGAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'email', 'telefone', 'is_active')
    search_fields = ('nome', 'cnpj', 'email')
    list_filter = ('is_active',)

@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ('valor', 'data', 'registrado_por', 'is_publico')
    search_fields = ('descricao', 'registrado_por__nome')
    list_filter = ('data', 'is_publico')

@admin.register(DistribuicaoOferta)
class DistribuicaoOfertaAdmin(admin.ModelAdmin):
    list_display = ('oferta', 'ong', 'destino', 'valor', 'meio_envio', 'data_envio')
    search_fields = ('destino', 'ong__nome', 'oferta__descricao')
    list_filter = ('data_envio', 'ong')

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('get_tipo_badge', 'categoria', 'get_valor_formatado', 'data', 'registrado_por', 'get_descricao_resumida')
    search_fields = ('descricao', 'categoria', 'registrado_por__nome')
    list_filter = ('tipo', 'categoria', 'data', 'registrado_por', 'created_at')
    list_editable = ('categoria',)
    ordering = ('-data', '-created_at')
    list_per_page = 50
    
    fieldsets = (
        ('Informações da Transação', {
            'fields': ('tipo', 'categoria', 'valor', 'descricao', 'data')
        }),
        ('Registro', {
            'fields': ('registrado_por',),
            'classes': ('collapse',)
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')
    actions = ['exportar_transacoes', 'marcar_como_confirmadas']
    
    def get_tipo_badge(self, obj):
        if obj.tipo == 'entrada':
            return format_html(
                '<span style="background: #28a745; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">ENTRADA</span>'
            )
        else:
            return format_html(
                '<span style="background: #dc3545; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">SAÍDA</span>'
            )
    get_tipo_badge.short_description = 'Tipo'
    
    def get_valor_formatado(self, obj):
        valor_formatado = f"{float(obj.valor):.2f}"
        if obj.tipo == 'entrada':
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">+ R$ {}</span>',
                valor_formatado
            )
        else:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">- R$ {}</span>',
                valor_formatado
            )
    get_valor_formatado.short_description = 'Valor'
    get_valor_formatado.admin_order_field = 'valor'
    
    def get_descricao_resumida(self, obj):
        if len(obj.descricao) > 30:
            return obj.descricao[:30] + '...'
        return obj.descricao
    get_descricao_resumida.short_description = 'Descrição'
    
    def exportar_transacoes(self, request, queryset):
        self.message_user(request, f'Exportação de {queryset.count()} transações iniciada.')
    exportar_transacoes.short_description = 'Exportar transações selecionadas'
    
    def marcar_como_confirmadas(self, request, queryset):
        # Implementar lógica de confirmação
        self.message_user(request, f'{queryset.count()} transações marcadas como confirmadas.')
    marcar_como_confirmadas.short_description = 'Marcar como confirmadas'
