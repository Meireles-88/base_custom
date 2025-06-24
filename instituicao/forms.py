from django import forms
from .models import TipoInstituicao, Instituicao

class TipoInstituicaoForm(forms.ModelForm):
    """
    Formulário para criar e editar o modelo TipoInstituicao.
    """
    class Meta:
        model = TipoInstituicao
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: Guarda Civil Municipal'
                }
            ),
        }
        labels = {
            'nome': 'Nome do Tipo de Instituição',
        }

class InstituicaoForm(forms.ModelForm):
    """
    Formulário para criar e editar o modelo Instituicao.
    """
    class Meta:
        model = Instituicao
        # Lista de todos os campos que aparecerão no formulário
        fields = [
            'tipo', 'municipio', 'cnpj', 
            'contato', 'email_institucional', 'plano_contratado', 
            'brasao_instituicao', 'brasao_municipio'
        ]
        widgets = {
            # Adicionando classes do Bootstrap para um visual consistente
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'municipio': forms.Select(attrs={'class': 'form-select'}), # Usando Select para o futuro
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'contato': forms.TextInput(attrs={'class': 'form-control'}),
            'email_institucional': forms.EmailInput(attrs={'class': 'form-control'}),
            'plano_contratado': forms.TextInput(attrs={'class': 'form-control'}),
            'brasao_instituicao': forms.FileInput(attrs={'class': 'form-control'}),
            'brasao_municipio': forms.FileInput(attrs={'class': 'form-control'}),
        }