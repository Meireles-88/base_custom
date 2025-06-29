from django.urls import path
from . import views

app_name = 'instituicao'

urlpatterns = [
    # URLs para Gerenciamento Geral de Instituições (Nível SI)
    path('', views.InstituicaoListView.as_view(), name='lista_instituicoes'),
    path('nova/', views.InstituicaoCreateView.as_view(), name='cria_instituicao'),
    path('<int:pk>/editar/', views.InstituicaoUpdateView.as_view(), name='edita_instituicao'),
    path('<int:pk>/excluir/', views.InstituicaoDeleteView.as_view(), name='exclui_instituicao'),

    # URL para a chamada dinâmica (AJAX)
    path('ajax/carregar-municipios/', views.carregar_municipios, name='ajax_carregar_municipios'),
    
    # URLs para Tipos de Instituição (Globais, para Admin SI)
    path('tipos/', views.TipoInstituicaoView.as_view(), name='lista_tipos'),
    path('tipos/<int:pk>/editar/', views.TipoInstituicaoUpdateView.as_view(), name='edita_tipo'),
    path('tipos/<int:pk>/excluir/', views.TipoInstituicaoDeleteView.as_view(), name='exclui_tipo'),

    # --- ROTAS DE NAVEGAÇÃO E CONTEXTO INSTITUCIONAL ---
    path('<int:pk>/detalhe/', views.InstituicaoDetailView.as_view(), name='detalhe_instituicao'),
    path('<int:pk>/entrar-contexto/', views.entrar_contexto_institucional, name='entrar_contexto'),
    path('sair-contexto/', views.sair_contexto_institucional, name='sair_contexto'),
    path('<int:pk>/gerenciar/', views.GerenciarInstituicaoView.as_view(), name='gerenciar_instituicao'),
    path('<int:instituicao_pk>/membros/', views.InstituicaoMembrosListView.as_view(), name='lista_membros'),
    
    # --- ROTAS DE GERENCIAMENTO DE HIERARQUIA LOCAL ---
    
    # Rota Unificada para listar e criar Cargos, Patentes e Funções
    path('<int:instituicao_pk>/gerenciar/hierarquia/', views.GerenciarHierarquiaView.as_view(), name='gerenciar_hierarquia'),
    
    # Rotas para Editar e Excluir Cargos
    path('<int:instituicao_pk>/cargos/<int:pk>/editar/', views.CargoUpdateView.as_view(), name='edita_cargo'),
    path('<int:instituicao_pk>/cargos/<int:pk>/excluir/', views.CargoDeleteView.as_view(), name='exclui_cargo'),

    # Rotas para Editar e Excluir Patentes
    path('<int:instituicao_pk>/patentes/<int:pk>/editar/', views.PatenteUpdateView.as_view(), name='edita_patente'),
    path('<int:instituicao_pk>/patentes/<int:pk>/excluir/', views.PatenteDeleteView.as_view(), name='exclui_patente'),

    # Rotas para Editar e Excluir Funções
    path('<int:instituicao_pk>/funcoes/<int:pk>/editar/', views.FuncaoUpdateView.as_view(), name='edita_funcao'),
    path('<int:instituicao_pk>/funcoes/<int:pk>/excluir/', views.FuncaoDeleteView.as_view(), name='exclui_funcao'),
]