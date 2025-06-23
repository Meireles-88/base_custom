from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from .models import UserProfile

class CustomUserCreationForm(forms.ModelForm):
    """
    Formulário para um admin criar um novo usuário e seu perfil.
    Com validação e método save à prova de falhas (usando get_or_create).
    """
    username = forms.CharField(label='Nome de Usuário', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['cargo', 'instituicao', 'cpf', 'celular', 'fone', 'foto', 'ativo']
        widgets = {
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'instituicao': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'fone': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso. Por favor, escolha outro.")
        return username

    @transaction.atomic
    def save(self, commit=True):
        """
        Método save definitivo. Ele cria o User e depois usa get_or_create
        para obter ou criar o perfil, evitando conflitos com signals.
        """
        # 1. Cria o objeto User. Isso pode disparar o sinal.
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )

        # 2. Obtenha o perfil que o sinal criou, ou crie um se o sinal não existir.
        #    Esta linha é à prova de falhas.
        profile, created = UserProfile.objects.get_or_create(user=user)

        # 3. Agora, atualizamos o perfil (seja ele novo ou recém-obtido)
        #    com os dados do formulário.
        profile.cargo = self.cleaned_data.get('cargo')
        profile.instituicao = self.cleaned_data.get('instituicao')
        profile.cpf = self.cleaned_data.get('cpf')
        profile.celular = self.cleaned_data.get('celular')
        profile.fone = self.cleaned_data.get('fone')
        profile.foto = self.cleaned_data.get('foto')
        profile.ativo = self.cleaned_data.get('ativo', False)
        
        if commit:
            profile.save() # Salva o perfil com os dados atualizados.
            
        return profile


class UserProfileEditForm(forms.ModelForm):
    """
    Formulário para editar os dados de um usuário existente e seu perfil.
    """
    first_name = forms.CharField(label='Nome', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Sobrenome', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['cargo', 'instituicao', 'cpf', 'celular', 'fone', 'foto', 'ativo']
        widgets = {
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'instituicao': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'fone': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
            raise forms.ValidationError("Este endereço de e-mail já está sendo utilizado por outro usuário.")
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
            
        return profile