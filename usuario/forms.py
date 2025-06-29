# usuario/forms.py
from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from .models import UserProfile, Cargo, Patente, Funcao, Instituicao

# --- Formulários de Gerenciamento de Hierarquia (para o Painel Institucional) ---

class CargoForm(forms.ModelForm):
    """ Formulário para criar/editar um Cargo dentro de uma instituição. """
    class Meta:
        model = Cargo
        fields = ['nome']
        widgets = { 'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Guarda Civil'}) }

class PatenteForm(forms.ModelForm):
    """ Formulário para criar/editar uma Patente dentro de uma instituição. """
    class Meta:
        model = Patente
        fields = ['nome', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Inspetor Chefe'}),
            'ordem': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class FuncaoForm(forms.ModelForm):
    """ Formulário para criar/editar uma Função dentro de uma instituição. """
    class Meta:
        model = Funcao
        fields = ['nome']
        widgets = { 'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Chefe de Turno'}) }


# --- Formulários de Gerenciamento de Usuários (para Admin SI) ---

class AdminUserCreationForm(forms.ModelForm):
    """ Formulário para um Admin SI criar um novo usuário e seu perfil completo. """
    username = forms.CharField(label='Nome de Usuário', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = UserProfile
        fields = ['instituicao', 'cargo', 'patente', 'funcoes', 'cpf', 'celular', 'foto', 'is_admin_instituicao']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limita as opções de cargo, patente e função à instituição selecionada
        if 'instituicao' in self.data:
            try:
                instituicao_id = int(self.data.get('instituicao'))
                self.fields['cargo'].queryset = Cargo.objects.filter(instituicao_id=instituicao_id).order_by('nome')
                self.fields['patente'].queryset = Patente.objects.filter(instituicao_id=instituicao_id).order_by('ordem')
                self.fields['funcoes'].queryset = Funcao.objects.filter(instituicao_id=instituicao_id).order_by('nome')
            except (ValueError, TypeError):
                pass # Em caso de erro, mantém os querysets vazios
        elif self.instance.pk and self.instance.instituicao:
             self.fields['cargo'].queryset = self.instance.instituicao.cargos.order_by('nome')
             self.fields['patente'].queryset = self.instance.instituicao.patentes.order_by('ordem')
             self.fields['funcoes'].queryset = self.instance.instituicao.funcoes.order_by('nome')


class UserProfileEditForm(forms.ModelForm):
    """ Formulário para o Admin SI editar os dados de um usuário e seu perfil. """
    first_name = forms.CharField(label='Nome', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Sobrenome', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
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
        # Lógica para popular os campos dinamicamente, igual à de criação
        if self.instance.pk and self.instance.instituicao:
             self.fields['cargo'].queryset = self.instance.instituicao.cargos.order_by('nome')
             self.fields['patente'].queryset = self.instance.instituicao.patentes.order_by('ordem')
             self.fields['funcoes'].queryset = self.instance.instituicao.funcoes.order_by('nome')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.user.pk).exists():
            raise forms.ValidationError("Este e-mail já está sendo utilizado por outro usuário.")
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
            self.save_m2m() # Salva as relações ManyToMany
        return profile