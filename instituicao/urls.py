# instituicao/urls.py
from django.urls import path
from . import views

app_name = 'instituicao'

urlpatterns = [
    # URLs para Instituições
    path('', views.InstituicaoListView.as_view(), name='lista_instituicoes'),
    path('nova/', views.InstituicaoCreateView.as_view(), name='cria_instituicao'),
    path('<int:pk>/editar/', views.InstituicaoUpdateView.as_view(), name='edita_instituicao'),
    path('<int:pk>/excluir/', views.InstituicaoDeleteView.as_view(), name='exclui_instituicao'),
    path('<int:pk>/detalhe/', views.InstituicaoDetailView.as_view(), name='detalhe_instituicao'),
    path('<int:pk>/gerenciar/', views.GerenciarInstituicaoView.as_view(), name='gerenciar_instituicao'),
    
    # URL para a chamada dinâmica (AJAX)
    path('ajax/carregar-municipios/', views.carregar_municipios, name='ajax_carregar_municipios'),

    # URLs para Tipos de Instituição
    path('tipos/', views.TipoInstituicaoListView.as_view(), name='lista_tipos'),
    path('tipos/<int:pk>/editar/', views.TipoInstituicaoUpdateView.as_view(), name='edita_tipo'),
    path('tipos/<int:pk>/excluir/', views.TipoInstituicaoDeleteView.as_view(), name='exclui_tipo'),

    # URLs para Gerenciamento de Hierarquia Local
    path('<int:instituicao_pk>/gerenciar/cargos/', views.CargoListView.as_view(), name='gerenciar_cargos'),
    path('<int:instituicao_pk>/gerenciar/cargos/novo/', views.CargoCreateView.as_view(), name='cria_cargo'),
    path('<int:instituicao_pk>/gerenciar/cargos/<int:pk>/editar/', views.CargoUpdateView.as_view(), name='edita_cargo'),
    path('<int:instituicao_pk>/gerenciar/cargos/<int:pk>/excluir/', views.CargoDeleteView.as_view(), name='exclui_cargo'),

    path('<int:instituicao_pk>/gerenciar/patentes/', views.PatenteListView.as_view(), name='gerenciar_patentes'),
    path('<int:instituicao_pk>/gerenciar/patentes/novo/', views.PatenteCreateView.as_view(), name='cria_patente'),
    path('<int:instituicao_pk>/gerenciar/patentes/<int:pk>/editar/', views.PatenteUpdateView.as_view(), name='edita_patente'),
    path('<int:instituicao_pk>/gerenciar/patentes/<int:pk>/excluir/', views.PatenteDeleteView.as_view(), name='exclui_patente'),

    path('<int:instituicao_pk>/gerenciar/funcoes/', views.FuncaoListView.as_view(), name='gerenciar_funcoes'),
    path('<int:instituicao_pk>/gerenciar/funcoes/novo/', views.FuncaoCreateView.as_view(), name='cria_funcao'),
    path('<int:instituicao_pk>/gerenciar/funcoes/<int:pk>/editar/', views.FuncaoUpdateView.as_view(), name='edita_funcao'),
    path('<int:instituicao_pk>/gerenciar/funcoes/<int:pk>/excluir/', views.FuncaoDeleteView.as_view(), name='exclui_funcao'),
]