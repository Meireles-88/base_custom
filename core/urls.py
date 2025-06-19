# core/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

# Adicione este import temporário para usar o reverse_lazy
from django.urls import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('painel.urls')),

    # URLs de Autenticação do Django
    # TESTE: Adicionando um redirect_authenticated_user para depuração
    path('login/', auth_views.LoginView.as_view(
        template_name='public/login.html',
        redirect_authenticated_user=True, # Garante que redirecione se já logado
        # NOVO: Altere temporariamente o target de redirecionamento para um lugar único
        # Se você estiver logado e tentar ir para /login/, deveria ir para cá.
        # Se você não estiver logado, deveria ver o formulário de login.
        next_page=reverse_lazy('painel:dashboard') # Pode ser redundante com LOGIN_REDIRECT_URL, mas força
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)