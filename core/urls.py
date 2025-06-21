# core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('painel.urls')),
    path('autenticacao/', include('autenticacao.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)