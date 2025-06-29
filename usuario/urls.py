# usuario/urls.py
from django.urls import path
from . import views

app_name = 'usuario'

urlpatterns = [
    # URLs de Gerenciamento de Usuários
    path('', views.user_list, name='user_list'),
    path('criar/', views.user_create, name='user_create'),
    path('<int:pk>/', views.user_profile, name='user_profile'),
    path('<int:pk>/editar/', views.user_edit, name='user_edit'),
    path('<int:pk>/deletar/', views.user_delete, name='user_delete'),

    # Rota para o Painel de Administração SI
    path('admin-si/', views.AdministracaoSIView.as_view(), name='painel_admin_si'),
]