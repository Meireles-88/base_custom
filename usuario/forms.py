from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from .models import UserProfile, Cargo, Patente, Funcao, Instituicao

# --- FORMULÁRIOS DE GERENCIAMENTO (PARA ADMIN SI) ---

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PatenteForm(forms.ModelForm):
    class Meta:
        model = Patente
        fields = ['nome', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'ordem': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class FuncaoForm(forms.ModelForm):
    class Meta:
        model = Funcao
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }

# --- FORMULÁRIOS DE USUÁRIO (Existentes e atualizados) ---

class AdminUserCreationForm(forms.ModelForm):
    username = forms.CharField(label='Nome de Usuário', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = UserProfile
        fields = ['instituicao', 'cargo', 'patente', 'funcoes', 'cpf', 'celular', 'foto', 'is_admin_instituicao']
        widgets = {
            'instituicao': forms.Select(attrs={'class': 'form-select'}),
            'cargo': forms.Select(attrs={'class': 'form-select'}),
            'patente': forms.Select(attrs={'class': 'form-select'}),
            'funcoes': forms.CheckboxSelectMultiple, # Melhor widget para ManyToMany
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'is_admin_instituicao': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username

    @transaction.atomic
    def save(self, commit=True):
        user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        profile = user.userprofile
        # Atualiza os campos do perfil
        profile.instituicao = self.cleaned_data.get('instituicao')
        profile.cargo = self.cleaned_data.get('cargo')
        profile.patente = self.cleaned_data.get('patente')
        profile.cpf = self.cleaned_data.get('cpf')
        profile.celular = self.cleaned_data.get('celular')
        profile.foto = self.cleaned_data.get('foto')
        profile.is_admin_instituicao = self.cleaned_data.get('is_admin_instituicao', False)
        if commit:
            profile.save()
            # O save de ManyToMany deve ocorrer após o save da instância principal
            profile.funcoes.set(self.cleaned_data.get('funcoes'))
        return profile


class UserProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(label='Nome', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Sobrenome', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['instituicao', 'cargo', 'patente', 'funcoes', 'cpf', 'celular', 'foto', 'is_admin_instituicao']
        widgets = {
            'instituicao': forms.Select(attrs={'class': 'form-select'}),
            'cargo': forms.Select(attrs={'class': 'form-select'}),
            'patente': forms.Select(attrs={'class': 'form-select'}),
            'funcoes': forms.CheckboxSelectMultiple,
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'is_admin_instituicao': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

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