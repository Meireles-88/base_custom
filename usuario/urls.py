# usuario/urls.py
from django.urls import path
from . import views

app_name = 'usuario'

urlpatterns = [
    path('', views.user_list, name='user_list'),  # Lista todos os perfis de usuários
    path('<int:pk>/', views.user_profile, name='user_profile'),  # Visualiza um perfil específico
]