# instituicao/urls.py
from django.urls import path
from . import views

app_name = 'instituicao'

urlpatterns = [
    path('', views.lista_instituicoes, name='lista_instituicoes'),
    # Futuramente, adicionaremos as rotas para criar, editar, etc.
]