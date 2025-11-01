"""
Configuração de URL para o projeto alfa_project.

A lista `urlpatterns` roteia URLs para views. Para mais informações, veja:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Exemplos:
Views de função
    1. Adicione uma importação:  from my_app import views
    2. Adicione uma URL a urlpatterns:  path('', views.home, name='home')
Views baseadas em classe
    1. Adicione uma importação:  from other_app.views import Home
    2. Adicione uma URL a urlpatterns:  path('', Home.as_view(), name='home')
Incluindo outra URLconf
    1. Importe a função include(): from django.urls import include, path
    2. Adicione uma URL a urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from app_Alfa import views
from app_Alfa.viewsets import (
    AuthViewSet, MembroViewSet, EventoViewSet, PostagemViewSet,
    TransacaoViewSet, OfertaViewSet, CargoViewSet, AdminViewSet,
    ONGViewSet, IgrejaViewSet, GrupoViewSet, DoacaoViewSet,
    TransferenciaViewSet, FotoEventoViewSet, FotoPostagemViewSet,
    DocumentoMembroViewSet, EventoPresencaViewSet, EventoComentarioViewSet
)
from app_Alfa.relatorio_views import (
    RelatorioMembrosView, RelatorioFinanceiroView, RelatorioEventosView,
    DashboardView, EstatisticasMembrosView, EstatisticasFinanceirasView,
    EstatisticasEventosView, ExportarMembrosView, ExportarTransacoesView
)

# Configurar router para viewsets
router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'membros', MembroViewSet)
router.register(r'eventos', EventoViewSet)
router.register(r'postagens', PostagemViewSet)
router.register(r'transacoes', TransacaoViewSet)
router.register(r'ofertas', OfertaViewSet)
router.register(r'cargos', CargoViewSet)
router.register(r'admins', AdminViewSet)
router.register(r'ongs', ONGViewSet)
router.register(r'igrejas', IgrejaViewSet)
router.register(r'grupos', GrupoViewSet)
router.register(r'doacoes', DoacaoViewSet)
router.register(r'transferencias', TransferenciaViewSet)
router.register(r'fotos-eventos', FotoEventoViewSet)
router.register(r'fotos-postagens', FotoPostagemViewSet)
router.register(r'documentos-membros', DocumentoMembroViewSet)
router.register(r'eventos-presencas', EventoPresencaViewSet)
router.register(r'eventos-comentarios', EventoComentarioViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API Routes
    path('api/', include(router.urls)),
    
    # Legacy endpoints (manter para compatibilidade)
    path('api/gerar-pdf-transferencia/<int:transferencia_id>/', views.gerar_pdf_transferencia, name='gerar_pdf_transferencia'),
    path('api/gerar-cartao-membro/<int:membro_id>/', views.gerar_cartao_membro, name='gerar_cartao_membro'),
    
    # Relatórios e Analytics
    path('api/relatorios/membros/pdf/', RelatorioMembrosView.as_view(), name='relatorio_membros_pdf'),
    path('api/relatorios/financeiro/pdf/', RelatorioFinanceiroView.as_view(), name='relatorio_financeiro_pdf'),
    path('api/relatorios/eventos/pdf/', RelatorioEventosView.as_view(), name='relatorio_eventos_pdf'),
    path('api/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('api/estatisticas/membros/', EstatisticasMembrosView.as_view(), name='estatisticas_membros'),
    path('api/estatisticas/financeiro/', EstatisticasFinanceirasView.as_view(), name='estatisticas_financeiro'),
    path('api/estatisticas/eventos/', EstatisticasEventosView.as_view(), name='estatisticas_eventos'),
    path('api/exportar/membros/csv/', ExportarMembrosView.as_view(), name='exportar_membros_csv'),
    path('api/exportar/transacoes/csv/', ExportarTransacoesView.as_view(), name='exportar_transacoes_csv'),
]
