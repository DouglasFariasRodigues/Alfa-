from django.contrib import admin
from .models import (Admin, Usuario, Membro, Grupo, Doacao, Igreja, Evento, 
                     Postagem, FotoEvento, FotoPostagem, Cargo, ONG, Oferta, DistribuicaoOferta,
                     DocumentoMembro)

# Registre seus modelos aqui.

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'get_cargo_nome', 'is_active', 'is_admin', 'created_at')
    search_fields = ('nome', 'email', 'cargo__nome')
    list_filter = ('is_active', 'is_admin', 'cargo')

    def get_cargo_nome(self, obj):
        return obj.cargo.nome if obj.cargo else 'Sem cargo'
    get_cargo_nome.short_description = 'Cargo'
    get_cargo_nome.admin_order_field = 'cargo__nome'

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
    list_display = ('id', 'nome', 'cpf', 'get_cargo_nome', 'status', 'cadastrado_por')
    search_fields = ('nome', 'cpf', 'email', 'dados_completos', 'cargo__nome')
    list_filter = ('status', 'data_batismo', 'cargo')
    
    def get_cargo_nome(self, obj):
        return obj.cargo.nome if obj.cargo else 'Sem cargo'
    get_cargo_nome.short_description = 'Cargo'
    get_cargo_nome.admin_order_field = 'cargo__nome'

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
    list_display = ('titulo', 'data', 'local', 'organizador')
    search_fields = ('titulo', 'descricao', 'local', 'organizador__username')
    list_filter = ('data', 'organizador')

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
    list_display = ('nome', 'created_at', 'pode_registrar_dizimos', 'pode_registrar_ofertas', 'pode_gerenciar_membros', 'pode_gerenciar_eventos')
    search_fields = ('nome', 'descricao')
    list_filter = ('created_at', 'pode_registrar_dizimos', 'pode_registrar_ofertas', 'pode_gerenciar_membros', 'pode_gerenciar_eventos')
    list_editable = ('pode_registrar_dizimos', 'pode_registrar_ofertas', 'pode_gerenciar_membros', 'pode_gerenciar_eventos')

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
