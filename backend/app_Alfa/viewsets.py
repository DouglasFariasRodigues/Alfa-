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
    FotoEvento, FotoPostagem, DocumentoMembro, Transferencia
)
from .serializers import (
    MembroSerializer, MembroCreateSerializer, AdminSerializer, UsuarioSerializer,
    CargoSerializer, EventoSerializer, EventoCreateSerializer, PostagemSerializer,
    PostagemCreateSerializer, TransacaoSerializer, TransacaoCreateSerializer,
    OfertaSerializer, OfertaCreateSerializer, ONGSerializer, GrupoSerializer,
    DoacaoSerializer, IgrejaSerializer, DocumentoMembroSerializer,
    TransferenciaSerializer, TransferenciaCreateSerializer, FotoEventoSerializer,
    FotoPostagemSerializer
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
