# usuario/forms.py
from django import forms
from .models import Cargo, Patente, Funcao
from .models import UserProfile, Instituicao # Necessário para AdminUserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

class CargoForm(forms.ModelForm):
    """ Formulário para criar/editar um Cargo dentro de uma instituição. """
    class Meta:
        model = Cargo
        fields = ['nome']
        widgets = { 'nome': forms.TextInput(attrs={'class': 'form-control'}) }

class PatenteForm(forms.ModelForm):
    """ Formulário para criar/editar uma Patente dentro de uma instituição. """
    class Meta:
        model = Patente
        fields = ['nome', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'ordem': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class FuncaoForm(forms.ModelForm):
    """ Formulário para criar/editar uma Função dentro de uma instituição. """
    class Meta:
        model = Funcao
        fields = ['nome']
        widgets = { 'nome': forms.TextInput(attrs={'class': 'form-control'}) }

# --- Formulários de Gerenciamento de Usuários (para Admin SI) ---

class AdminUserCreationForm(forms.ModelForm):
    username = forms.CharField(label='Nome de Usuário', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = UserProfile
        fields = ['instituicao', 'cargo', 'patente', 'funcoes', 'cpf', 'celular', 'foto', 'is_admin_instituicao']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instituicao' in self.data:
            try:
                instituicao_id = int(self.data.get('instituicao'))
                self.fields['cargo'].queryset = Cargo.objects.filter(instituicao_id=instituicao_id).order_by('nome')
                self.fields['patente'].queryset = Patente.objects.filter(instituicao_id=instituicao_id).order_by('ordem')
                self.fields['funcoes'].queryset = Funcao.objects.filter(instituicao_id=instituicao_id).order_by('nome')
            except (ValueError, TypeError): pass
        elif self.instance.pk and self.instance.instituicao:
             self.fields['cargo'].queryset = self.instance.instituicao.cargos.order_by('nome')
             self.fields['patente'].queryset = self.instance.instituicao.patentes.order_by('ordem')
             self.fields['funcoes'].queryset = self.instance.instituicao.funcoes.order_by('nome')
        else:
             self.fields['cargo'].queryset = Cargo.objects.none()
             self.fields['patente'].queryset = Patente.objects.none()
             self.fields['funcoes'].queryset = Funcao.objects.none()

class UserProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(label='Nome', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Sobrenome', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    class Meta:
        model = UserProfile
        fields = ['instituicao', 'cargo', 'patente', 'funcoes', 'cpf', 'celular', 'foto', 'is_admin_instituicao']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
        if self.instance.pk and self.instance.instituicao:
             self.fields['cargo'].queryset = self.instance.instituicao.cargos.order_by('nome')
             self.fields['patente'].queryset = self.instance.instituicao.patentes.order_by('ordem')
             self.fields['funcoes'].queryset = self.instance.instituicao.funcoes.order_by('nome')