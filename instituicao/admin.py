# instituicao/admin.py

from django.contrib import admin
from .models import TipoInstituicao, Instituicao, Estado, Municipio

@admin.register(TipoInstituicao)
class TipoInstituicaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'uf')
    search_fields = ('nome', 'uf')

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'get_uf')
    search_fields = ('nome',)
    list_filter = ('estado',)
    autocomplete_fields = ('estado',)

    @admin.display(description='UF', ordering='estado__uf')
    def get_uf(self, obj):
        return obj.estado.uf

@admin.register(Instituicao)
class InstituicaoAdmin(admin.ModelAdmin):
    # Usamos um método customizado 'get_uf' para exibir a UF
    list_display = ('__str__', 'get_uf_from_municipio', 'cnpj')
    
    # Para buscar, usamos a sintaxe de relacionamento
    search_fields = ('municipio__nome', 'cnpj', 'tipo__nome')
    
    # Para filtrar, também usamos a sintaxe de relacionamento
    list_filter = ('municipio__estado', 'tipo')
    
    # autocomplete_fields melhora muito a usabilidade para selecionar ForeignKeys
    autocomplete_fields = ('tipo', 'municipio')

    @admin.display(description='UF', ordering='municipio__estado__uf')
    def get_uf_from_municipio(self, obj):
        """ Pega a UF a partir do município relacionado """
        if obj.municipio and obj.municipio.estado:
            return obj.municipio.estado.uf
        return "N/A"