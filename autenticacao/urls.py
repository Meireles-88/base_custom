# autenticacao/urls.py
from django.urls import path
from . import views

app_name = 'autenticacao'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
]