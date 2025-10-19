from rest_framework import serializers
from .models import (
    Membro, Admin, Usuario, Cargo, Evento, Postagem, 
    Transacao, Oferta, ONG, Grupo, Doacao, Igreja,
    FotoEvento, FotoPostagem, DocumentoMembro, Transferencia
)

class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    cargo_nome = serializers.CharField(source='cargo.nome', read_only=True)
    
    class Meta:
        model = Admin
        fields = ['id', 'nome', 'email', 'telefone', 'cargo', 'cargo_nome', 'is_active', 'is_staff', 'date_joined', 'last_login']
        extra_kwargs = {'senha': {'write_only': True}}

class UsuarioSerializer(serializers.ModelSerializer):
    cargo_nome = serializers.CharField(source='cargo.nome', read_only=True)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'telefone', 'cargo', 'cargo_nome', 'is_active', 'is_staff', 'date_joined', 'last_login']
        extra_kwargs = {'senha': {'write_only': True}}

class MembroSerializer(serializers.ModelSerializer):
    cadastrado_por_nome = serializers.CharField(source='cadastrado_por.nome', read_only=True)
    
    class Meta:
        model = Membro
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'deleted_at', 'is_active']

class MembroCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membro
        exclude = ['created_at', 'updated_at', 'deleted_at', 'is_active', 'cadastrado_por']

class IgrejaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Igreja
        fields = '__all__'

class EventoSerializer(serializers.ModelSerializer):
    organizador_nome = serializers.CharField(source='organizador.username', read_only=True)
    
    class Meta:
        model = Evento
        fields = '__all__'

class EventoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        exclude = ['organizador']

class FotoEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoEvento
        fields = '__all__'

class PostagemSerializer(serializers.ModelSerializer):
    autor_nome = serializers.CharField(source='autor.username', read_only=True)
    
    class Meta:
        model = Postagem
        fields = '__all__'

class PostagemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postagem
        exclude = ['autor']

class FotoPostagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoPostagem
        fields = '__all__'

class TransacaoSerializer(serializers.ModelSerializer):
    registrado_por_nome = serializers.CharField(source='registrado_por.nome', read_only=True)
    
    class Meta:
        model = Transacao
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'deleted_at', 'is_active']

class TransacaoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacao
        exclude = ['created_at', 'updated_at', 'deleted_at', 'is_active', 'registrado_por']

class ONGSerializer(serializers.ModelSerializer):
    class Meta:
        model = ONG
        fields = '__all__'

class OfertaSerializer(serializers.ModelSerializer):
    registrado_por_nome = serializers.CharField(source='registrado_por.nome', read_only=True)
    
    class Meta:
        model = Oferta
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'deleted_at', 'is_active']

class OfertaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oferta
        exclude = ['created_at', 'updated_at', 'deleted_at', 'is_active', 'registrado_por']

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = '__all__'

class DoacaoSerializer(serializers.ModelSerializer):
    membro_nome = serializers.CharField(source='membro.nome', read_only=True)
    grupo_nome = serializers.CharField(source='grupo.nome', read_only=True)
    
    class Meta:
        model = Doacao
        fields = '__all__'

class DocumentoMembroSerializer(serializers.ModelSerializer):
    membro_nome = serializers.CharField(source='membro.nome', read_only=True)
    gerado_por_nome = serializers.CharField(source='gerado_por.nome', read_only=True)
    
    class Meta:
        model = DocumentoMembro
        fields = '__all__'

class TransferenciaSerializer(serializers.ModelSerializer):
    membro_nome = serializers.CharField(source='membro.nome', read_only=True)
    igreja_origem_nome = serializers.CharField(source='igreja_origem.nome', read_only=True)
    igreja_destino_nome = serializers.CharField(source='igreja_destino.nome', read_only=True)
    gerado_por_nome = serializers.CharField(source='gerado_por.nome', read_only=True)
    
    class Meta:
        model = Transferencia
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'deleted_at', 'is_active']

class TransferenciaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transferencia
        exclude = ['created_at', 'updated_at', 'deleted_at', 'is_active', 'gerado_por']
