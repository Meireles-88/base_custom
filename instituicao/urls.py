from django.urls import path
from . import views

app_name = 'instituicao'

urlpatterns = [
    # A rota principal agora aponta para a nova ListView de Instituições
    path('', views.InstituicaoListView.as_view(), name='lista_instituicoes'),

    # URLs para o CRUD de Tipos de Instituição
    path('tipos/', views.TipoInstituicaoListView.as_view(), name='lista_tipos'),
    # A linha abaixo foi removida, pois a criação é feita na lista_tipos
    # path('tipos/novo/', views.TipoInstituicaoCreateView.as_view(), name='cria_tipo'),
    path('tipos/<int:pk>/editar/', views.TipoInstituicaoUpdateView.as_view(), name='edita_tipo'),
    path('tipos/<int:pk>/excluir/', views.TipoInstituicaoDeleteView.as_view(), name='exclui_tipo'),
]