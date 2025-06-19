// static/js/public_scripts.js

document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.public-header-navbar-floating');
    if (navbar) {
        // Adiciona um listener para o evento de scroll da janela
        window.addEventListener('scroll', function() {
            // Verifica se a posição de scroll vertical é maior que 50 pixels
            if (window.scrollY > 50) { 
                // Se sim, adiciona a classe 'scrolled' ao body
                document.body.classList.add('scrolled');
            } else {
                // Se não, remove a classe 'scrolled' do body
                document.body.classList.remove('scrolled');
            }
        });
    }
});