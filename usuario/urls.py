# usuario/urls.py
from django.urls import path
from . import views

app_name = 'usuario'

urlpatterns = [
    path('', views.user_list, name='user_list'),  # Lista todos os perfis de usuários
    path('<int:pk>/', views.user_profile, name='user_profile'),  # Visualiza um perfil específico
    path('<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('create/', views.user_create, name='user_create'),
    path('<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('update-status/<int:pk>/', views.update_status, name='update_status'),
]