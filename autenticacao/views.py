# autenticacao/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View

class CustomLoginView(View):
    template_name = 'autenticacao/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Você já está logado. Redirecionando para o dashboard.")
            return redirect('painel:dashboard')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bem-vindo, {username}!")
            return redirect('painel:dashboard')
        else:
            messages.error(request, "Usuário ou senha inválidos.")
            return render(request, self.template_name)

def custom_logout(request):
    # Limpa mensagens existentes antes de adicionar a nova
    messages.get_messages(request).used = True  # Marca mensagens como exibidas
    logout(request)
    messages.success(request, "Você saiu do sistema com sucesso.")
    return redirect('painel:home')