// static/js/logged_in_scripts.js

document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.querySelector('.sidebar');
    const toggleSidebarBtn = document.querySelector('.toggle-sidebar-btn'); // Botão na sidebar
    const toggleSidebarMobileBtn = document.querySelector('.toggle-sidebar-mobile'); // Botão na top-navbar para mobile
    const dashboardWrapper = document.querySelector('.dashboard-wrapper');

    // Função para alternar a classe 'minimized'
    function toggleSidebar() {
        sidebar.classList.toggle('minimized');
        dashboardWrapper.classList.toggle('sidebar-minimized'); // Adiciona classe ao wrapper principal
    }

    // Event listener para o botão na sidebar (desktop)
    if (toggleSidebarBtn) {
        toggleSidebarBtn.addEventListener('click', toggleSidebar);
    }

    // Event listener para o botão na top-navbar (mobile)
    if (toggleSidebarMobileBtn) {
        toggleSidebarMobileBtn.addEventListener('click', function() {
            sidebar.classList.toggle('open'); // Abre/fecha a sidebar em mobile
        });
    }

    // Fechar sidebar ao clicar fora em mobile (se for overlay)
    // Isso é mais complexo e pode exigir um overlay, por enquanto, apenas o toggle.

});