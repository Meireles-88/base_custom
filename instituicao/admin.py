# instituicao/admin.py

from django.contrib import admin
from .models import TipoInstituicao, Instituicao

@admin.register(TipoInstituicao)
class TipoInstituicaoAdmin(admin.ModelAdmin):
    """
    Define a interface de administração para o modelo TipoInstituicao.
    """
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Instituicao)
class InstituicaoAdmin(admin.ModelAdmin):
    """
    Define a interface de administração para o modelo Instituicao.
    """
    list_display = ('__str__', 'municipio', 'uf', 'cnpj')
    search_fields = ('municipio', 'cnpj', 'tipo__nome')
    list_filter = ('uf', 'tipo')
    # autocomplete_fields melhora a seleção do 'tipo' quando há muitos registros.
    autocomplete_fields = ('tipo',)