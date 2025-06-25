from django.contrib import admin
from django.urls import path, include

# --- INÍCIO DAS MODIFICAÇÕES ---

# 1. Importe as bibliotecas necessárias
from django.conf import settings
from django.conf.urls.static import static

# --- FIM DAS MODIFICAÇÕES ---

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('painel.urls')),
    path('autenticacao/', include('autenticacao.urls')),
    path('usuario/', include('usuario.urls')),
    path('instituicoes/', include('instituicao.urls')),
]

# --- INÍCIO DAS MODIFICAÇÕES ---

# 2. Adicione esta linha no final do arquivo
# Esta linha diz ao Django para servir os arquivos de mídia (da pasta MEDIA_ROOT)
# apenas quando estivermos em modo de desenvolvimento (DEBUG=True).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# --- FIM DAS MODIFICAÇÕES ---