from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db.models import Q
from .models import (
    Membro, Admin, Usuario, Cargo, Evento, Postagem, 
    Transacao, Oferta, ONG, Grupo, Doacao, Igreja,
    FotoEvento, FotoPostagem, DocumentoMembro, Transferencia,
    EventoPresenca, EventoComentario
)
from .serializers import (
    MembroSerializer, MembroCreateSerializer, AdminSerializer, UsuarioSerializer,
    CargoSerializer, EventoSerializer, EventoCreateSerializer, PostagemSerializer,
    PostagemCreateSerializer, TransacaoSerializer, TransacaoCreateSerializer,
    OfertaSerializer, OfertaCreateSerializer, ONGSerializer, GrupoSerializer,
    DoacaoSerializer, IgrejaSerializer, DocumentoMembroSerializer,
    TransferenciaSerializer, TransferenciaCreateSerializer, FotoEventoSerializer,
    FotoPostagemSerializer, EventoPresencaSerializer, EventoPresencaCreateSerializer,
    EventoComentarioSerializer, EventoComentarioCreateSerializer
)

class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], permission_classes=[])
    def login(self, request):
        """Login de usuário admin"""
        email = request.data.get('email')
        senha = request.data.get('senha')
        
        if not email or not senha:
            return Response({
                'success': False,
                'message': 'Email e senha são obrigatórios'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            admin = Admin.objects.get(email=email)
            if admin.senha == senha:  # Em produção, usar hash de senha
                # Criar token JWT
                user, created = User.objects.get_or_create(
                    username=admin.email,
                    defaults={'email': admin.email, 'is_staff': True}
                )
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'success': True,
                    'message': 'Login realizado com sucesso',
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user': AdminSerializer(admin).data
                })
            else:
                return Response({
                    'success': False,
                    'message': 'Credenciais inválidas'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Admin.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Usuário não encontrado'
            }, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Obter dados do usuário atual"""
        try:
            # Tentar encontrar como admin primeiro
            admin = Admin.objects.get(email=request.user.username)
            return Response({
                'id': admin.id,
                'nome': admin.nome,
                'email': admin.email,
                'telefone': admin.telefone,
                'cargo': AdminSerializer(admin).data.get('cargo'),
                'is_admin': True,
                'user_type': 'admin',
                'date_joined': admin.date_joined,
                'last_login': admin.last_login
            })
        except Admin.DoesNotExist:
            try:
                # Se não for admin, tentar como membro
                membro = Membro.objects.get(email=request.user.username)
                return Response({
                    'id': membro.id,
                    'nome': membro.nome,
                    'email': membro.email,
                    'telefone': membro.telefone,
                    'cargo': MembroSerializer(membro).data.get('cargo'),
                    'is_admin': False,
                    'user_type': 'membro',
                    'status': membro.status,
                    'created_at': membro.created_at,
                    'updated_at': membro.updated_at
                })
            except Membro.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Usuário não encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], permission_classes=[])
    def login_membro(self, request):
        """Login de membro"""
        email = request.data.get('email')
        senha = request.data.get('senha')
        
        if not email or not senha:
            return Response({
                'success': False,
                'message': 'Email e senha são obrigatórios'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            membro = Membro.objects.get(email=email)
            if membro.senha == senha:  # Em produção, usar hash de senha
                # Criar token JWT
                user, created = User.objects.get_or_create(
                    username=membro.email,
                    defaults={'email': membro.email, 'is_staff': False}
                )
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'success': True,
                    'message': 'Login realizado com sucesso',
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user': MembroSerializer(membro).data,
                    'user_type': 'membro'
                })
            else:
                return Response({
                    'success': False,
                    'message': 'Credenciais inválidas'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Membro.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Membro não encontrado'
            }, status=status.HTTP_404_NOT_FOUND)

class MembroViewSet(viewsets.ModelViewSet):
    queryset = Membro.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MembroCreateSerializer
        return MembroSerializer
    
    def get_queryset(self):
        queryset = Membro.objects.all()
        status_filter = self.request.query_params.get('status')
        search = self.request.query_params.get('search')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) |
                Q(email__icontains=search) |
                Q(telefone__icontains=search)
            )
        
        return queryset
    
    def perform_create(self, serializer):
        # Assumir que o usuário autenticado é um Admin
        try:
            admin = Admin.objects.get(email=self.request.user.username)
            serializer.save(cadastrado_por=admin)
        except Admin.DoesNotExist:
            serializer.save()

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EventoCreateSerializer
        return EventoSerializer
    
    def get_queryset(self):
        queryset = Evento.objects.all()
        search = self.request.query_params.get('search')
        
        if search:
            queryset = queryset.filter(
                Q(titulo__icontains=search) |
                Q(descricao__icontains=search) |
                Q(local__icontains=search)
            )
        
        return queryset.order_by('-data')
    
    def perform_create(self, serializer):
        # Usar o usuário autenticado como organizador
        try:
            # Tentar encontrar o usuário correspondente ao admin autenticado
            admin = Admin.objects.get(email=self.request.user.username)
            organizador, created = Usuario.objects.get_or_create(
                username=admin.email,
                defaults={
                    'email': admin.email,
                    'is_active': True,
                    'is_staff': True
                }
            )
        except Admin.DoesNotExist:
            # Usuário padrão se não encontrar admin
            organizador, created = Usuario.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@igreja.com',
                    'is_active': True,
                    'is_staff': True
                }
            )
        serializer.save(organizador=organizador)

class PostagemViewSet(viewsets.ModelViewSet):
    queryset = Postagem.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostagemCreateSerializer
        return PostagemSerializer
    
    def get_queryset(self):
        return Postagem.objects.all().order_by('-data_publicacao')
    
    def perform_create(self, serializer):
        # Assumir que o usuário autenticado é um Admin
        try:
            admin = Admin.objects.get(email=self.request.user.username)
            # Criar usuário correspondente
            autor, created = Usuario.objects.get_or_create(
                username=admin.email,
                defaults={
                    'email': admin.email,
                    'is_active': True,
                    'is_staff': True
                }
            )
            serializer.save(autor=autor)
        except Admin.DoesNotExist:
            # Usuário padrão
            autor, created = Usuario.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@igreja.com',
                    'is_active': True,
                    'is_staff': True
                }
            )
            serializer.save(autor=autor)

class TransacaoViewSet(viewsets.ModelViewSet):
    queryset = Transacao.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TransacaoCreateSerializer
        return TransacaoSerializer
    
    def get_queryset(self):
        queryset = Transacao.objects.all()
        tipo = self.request.query_params.get('tipo')
        categoria = self.request.query_params.get('categoria')
        
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        
        if categoria:
            queryset = queryset.filter(categoria__icontains=categoria)
        
        return queryset.order_by('-data')
    
    def perform_create(self, serializer):
        # Assumir que o usuário autenticado é um Admin
        try:
            admin = Admin.objects.get(email=self.request.user.username)
            serializer.save(registrado_por=admin)
        except Admin.DoesNotExist:
            serializer.save()

class OfertaViewSet(viewsets.ModelViewSet):
    queryset = Oferta.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OfertaCreateSerializer
        return OfertaSerializer
    
    def get_queryset(self):
        return Oferta.objects.all().order_by('-data')
    
    def perform_create(self, serializer):
        # Assumir que o usuário autenticado é um Admin
        try:
            admin = Admin.objects.get(email=self.request.user.username)
            serializer.save(registrado_por=admin)
        except Admin.DoesNotExist:
            serializer.save()

class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    permission_classes = [IsAuthenticated]

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated]

class ONGViewSet(viewsets.ModelViewSet):
    queryset = ONG.objects.all()
    serializer_class = ONGSerializer
    permission_classes = [IsAuthenticated]

class IgrejaViewSet(viewsets.ModelViewSet):
    queryset = Igreja.objects.all()
    serializer_class = IgrejaSerializer
    permission_classes = [IsAuthenticated]

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
    permission_classes = [IsAuthenticated]

class DoacaoViewSet(viewsets.ModelViewSet):
    queryset = Doacao.objects.all()
    serializer_class = DoacaoSerializer
    permission_classes = [IsAuthenticated]

class TransferenciaViewSet(viewsets.ModelViewSet):
    queryset = Transferencia.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TransferenciaCreateSerializer
        return TransferenciaSerializer
    
    def perform_create(self, serializer):
        # Assumir que o usuário autenticado é um Admin
        try:
            admin = Admin.objects.get(email=self.request.user.username)
            serializer.save(gerado_por=admin)
        except Admin.DoesNotExist:
            serializer.save()

class FotoEventoViewSet(viewsets.ModelViewSet):
    queryset = FotoEvento.objects.all()
    serializer_class = FotoEventoSerializer
    permission_classes = [IsAuthenticated]

class FotoPostagemViewSet(viewsets.ModelViewSet):
    queryset = FotoPostagem.objects.all()
    serializer_class = FotoPostagemSerializer
    permission_classes = [IsAuthenticated]

class DocumentoMembroViewSet(viewsets.ModelViewSet):
    queryset = DocumentoMembro.objects.all()
    serializer_class = DocumentoMembroSerializer
    permission_classes = [IsAuthenticated]

class EventoPresencaViewSet(viewsets.ModelViewSet):
    queryset = EventoPresenca.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EventoPresencaCreateSerializer
        return EventoPresencaSerializer
    
    def get_queryset(self):
        queryset = EventoPresenca.objects.all()
        evento_id = self.request.query_params.get('evento')
        membro_id = self.request.query_params.get('membro')
        
        if evento_id:
            queryset = queryset.filter(evento_id=evento_id)
        if membro_id:
            queryset = queryset.filter(membro_id=membro_id)
            
        return queryset.order_by('-data_confirmacao')

class EventoComentarioViewSet(viewsets.ModelViewSet):
    queryset = EventoComentario.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EventoComentarioCreateSerializer
        return EventoComentarioSerializer
    
    def get_queryset(self):
        queryset = EventoComentario.objects.filter(aprovado=True)  # Só comentários aprovados
        evento_id = self.request.query_params.get('evento')
        membro_id = self.request.query_params.get('membro')
        
        if evento_id:
            queryset = queryset.filter(evento_id=evento_id)
        if membro_id:
            queryset = queryset.filter(membro_id=membro_id)
            
        return queryset.order_by('-data_comentario')
