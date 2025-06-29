from django.urls import path
from . import views

app_name = 'instituicao'

urlpatterns = [
    # URLs para Instituições
    path('', views.InstituicaoListView.as_view(), name='lista_instituicoes'),
    path('nova/', views.InstituicaoCreateView.as_view(), name='cria_instituicao'),
    path('<int:pk>/detalhe/', views.InstituicaoDetailView.as_view(), name='detalhe_instituicao'),
    path('<int:pk>/editar/', views.InstituicaoUpdateView.as_view(), name='edita_instituicao'),
    path('<int:pk>/excluir/', views.InstituicaoDeleteView.as_view(), name='exclui_instituicao'),

    # --- ROTAS DE MUDANÇA DE CONTEXTO ADICIONADAS ---
    path('<int:pk>/entrar-contexto/', views.entrar_contexto_institucional, name='entrar_contexto'),
    path('sair-contexto/', views.sair_contexto_institucional, name='sair_contexto'),

    # URL para a chamada dinâmica (AJAX)
    path('ajax/carregar-municipios/', views.carregar_municipios, name='ajax_carregar_municipios'),
    
    # URLs para Tipos de Instituição (Globais)
    path('tipos/', views.TipoInstituicaoView.as_view(), name='lista_tipos'),
    path('tipos/<int:pk>/editar/', views.TipoInstituicaoUpdateView.as_view(), name='edita_tipo'),
    path('tipos/<int:pk>/excluir/', views.TipoInstituicaoDeleteView.as_view(), name='exclui_tipo'),
    
    # --- ROTAS DE GERENCIAMENTO INSTITUCIONAL ---
    path('<int:pk>/gerenciar/', views.GerenciarInstituicaoView.as_view(), name='gerenciar_instituicao'),
    path('<int:instituicao_pk>/gerenciar/hierarquia/', views.GerenciarHierarquiaView.as_view(), name='gerenciar_hierarquia'),
    
    # (As outras rotas para o CRUD de Cargo, Patente e Função permanecem aqui)
]