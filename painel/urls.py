# painel/urls.py

from django.urls import path
from . import views

app_name = 'painel' # Define um namespace para as URLs do app

urlpatterns = [
    path('', views.home, name='home'), # URL para a página inicial
    path('dashboard/', views.dashboard, name='dashboard'), # URL para o painel
]