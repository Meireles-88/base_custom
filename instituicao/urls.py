from django.urls import path
from . import views

app_name = 'instituicao'

urlpatterns = [
    path('', views.InstituicaoListView.as_view(), name='lista_instituicoes'),
    path('nova/', views.InstituicaoCreateView.as_view(), name='cria_instituicao'),
    path('<int:pk>/editar/', views.InstituicaoUpdateView.as_view(), name='edita_instituicao'),
    path('<int:pk>/excluir/', views.InstituicaoDeleteView.as_view(), name='exclui_instituicao'),
    path('<int:pk>/detalhe/', views.InstituicaoDetailView.as_view(), name='detalhe_instituicao'),
    path('<int:pk>/membros/', views.InstituicaoMembrosListView.as_view(), name='lista_membros'),
    path('ajax/carregar-municipios/', views.carregar_municipios, name='ajax_carregar_municipios'),
    path('tipos/', views.TipoInstituicaoListView.as_view(), name='lista_tipos'),
    path('tipos/<int:pk>/editar/', views.TipoInstituicaoUpdateView.as_view(), name='edita_tipo'),
    path('tipos/<int:pk>/excluir/', views.TipoInstituicaoDeleteView.as_view(), name='exclui_tipo'),
]