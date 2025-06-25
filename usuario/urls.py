from django.urls import path
from . import views

app_name = 'usuario'

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('criar/', views.user_create, name='user_create'),
    path('<int:pk>/', views.user_profile, name='user_profile'),
    path('<int:pk>/editar/', views.user_edit, name='user_edit'),
    path('<int:pk>/deletar/', views.user_delete, name='user_delete'),

    # Rota para o Painel de Administração SI
    path('admin-si/', views.AdministracaoListView.as_view(), name='painel_admin_si'),

    # Rotas para Cargos
    path('cargos/', views.CargoListView.as_view(), name='lista_cargos'),
    path('cargos/novo/', views.CargoCreateView.as_view(), name='cria_cargo'),
    path('cargos/<int:pk>/editar/', views.CargoUpdateView.as_view(), name='edita_cargo'),
    path('cargos/<int:pk>/excluir/', views.CargoDeleteView.as_view(), name='exclui_cargo'),

    # Rotas para Patentes
    path('patentes/', views.PatenteListView.as_view(), name='lista_patentes'),
    path('patentes/novo/', views.PatenteCreateView.as_view(), name='cria_patente'),
    path('patentes/<int:pk>/editar/', views.PatenteUpdateView.as_view(), name='edita_patente'),
    path('patentes/<int:pk>/excluir/', views.PatenteDeleteView.as_view(), name='exclui_patente'),

    # Rotas para Funções
    path('funcoes/', views.FuncaoListView.as_view(), name='lista_funcoes'),
    path('funcoes/novo/', views.FuncaoCreateView.as_view(), name='cria_funcao'),
    path('funcoes/<int:pk>/editar/', views.FuncaoUpdateView.as_view(), name='edita_funcao'),
    path('funcoes/<int:pk>/excluir/', views.FuncaoDeleteView.as_view(), name='exclui_funcao'),
]