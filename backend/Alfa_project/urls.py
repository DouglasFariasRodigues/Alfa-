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

from django.urls import path, include
from app_Alfa import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/gerar-pdf-transferencia/<int:transferencia_id>/', views.gerar_pdf_transferencia, name='gerar_pdf_transferencia'),
    path('api/gerar-cartao-membro/<int:membro_id>/', views.gerar_cartao_membro, name='gerar_cartao_membro'),
    path('api/transacoes/', views.transacao_create, name='transacao_create'),
    path('api/eventos/', views.evento_create, name='evento_create'),
    path('api/posts/', views.postagem_create, name='postagem_create'),
    path('api/comentarios/', views.comentario_create, name='comentario_create'),
    # Swagger/OpenAPI documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
