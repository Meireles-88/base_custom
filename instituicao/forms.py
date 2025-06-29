from django import forms
from .models import TipoInstituicao, Instituicao, Municipio

class TipoInstituicaoForm(forms.ModelForm):
    """
    Formulário para criar/editar os Tipos de Instituição globais,
    gerenciado pelo Admin Nível SI.
    """
    class Meta:
        model = TipoInstituicao
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Guarda Civil Municipal'})
        }
        labels = {
            'nome': 'Nome do Tipo de Instituição'
        }

class InstituicaoForm(forms.ModelForm):
    """
    Formulário para o Admin SI criar ou editar uma Instituição específica.
    """
    # O queryset de municípios começará vazio e será preenchido dinamicamente via JavaScript.
    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.none(),
        label="Município",
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Selecione um estado primeiro para carregar a lista de municípios."
    )
    
    class Meta:
        model = Instituicao
        # Lista de todos os campos que aparecerão no formulário.
        # 'nome_gerado' não está aqui, pois é gerado automaticamente pelo modelo.
        fields = [
            'tipo', 'municipio', 'cnpj', 'contato', 'email_institucional', 
            'plano_contratado', 'logradouro', 'numero', 'bairro', 'cep',
            'brasao_instituicao', 'brasao_municipio'
        ]
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'contato': forms.TextInput(attrs={'class': 'form-control'}),
            'email_institucional': forms.EmailInput(attrs={'class': 'form-control'}),
            'plano_contratado': forms.TextInput(attrs={'class': 'form-control'}),
            'logradouro': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'brasao_instituicao': forms.FileInput(attrs={'class': 'form-control'}),
            'brasao_municipio': forms.FileInput(attrs={'class': 'form-control'}),
        }