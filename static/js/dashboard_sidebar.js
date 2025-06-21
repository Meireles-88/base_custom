// static/js/dashboard_sidebar.js

document.addEventListener('DOMContentLoaded', function() {
    const body = document.body;
    const sidebar = document.querySelector('.sidebar');
    const toggleBtn = document.querySelector('.toggle-sidebar-btn'); // Botão principal (navbar)
    const closeSidebarMobileBtn = document.querySelector('.close-sidebar-mobile-btn'); // Botão 'X' dentro da sidebar (mobile)
    const overlayMobile = document.querySelector('.overlay-mobile-sidebar');

    // Define um ID para a sidebar para o aria-controls
    sidebar.id = 'sidebar-navigation';

    const DESKTOP_BREAKPOINT = 768; // Mesma breakpoint

    // Função para alternar o estado da sidebar no desktop
    function toggleSidebarDesktop() {
        const isExpanded = body.classList.toggle('sidebar-expanded-desktop'); // Alterna e retorna o estado atual
        body.classList.toggle('sidebar-minimized-desktop', !isExpanded); // Garante que a outra classe esteja correta
        toggleBtn.setAttribute('aria-expanded', isExpanded); // Atualiza atributo ARIA
        // updateToggleIcon(isExpanded); // REMOVIDO: Não precisamos mais alternar o ícone do toggle
    }

    // Função para abrir a sidebar (mobile)
    function openSidebarMobile() {
        body.classList.add('sidebar-open-mobile');
        body.classList.remove('sidebar-closed-mobile');
        overlayMobile.style.display = 'block';
        toggleBtn.setAttribute('aria-expanded', true); // Sidebar está aberta
    }

    // Função para fechar a sidebar (mobile)
    function closeSidebarMobile() {
        body.classList.remove('sidebar-open-mobile');
        body.classList.add('sidebar-closed-mobile');
        overlayMobile.style.display = 'none';
        toggleBtn.setAttribute('aria-expanded', false); // Sidebar está fechada
    }

    // REMOVIDO: A função updateToggleIcon não é mais necessária, pois o ícone é sempre o mesmo
    /*
    function updateToggleIcon(isSidebarExpanded) {
        const barsIcon = toggleBtn.querySelector('.toggle-icon-bars');
        const timesIcon = toggleBtn.querySelector('.toggle-icon-times');

        if (window.innerWidth > DESKTOP_BREAKPOINT) {
            if (isSidebarExpanded) {
                barsIcon.classList.add('d-none');
                timesIcon.classList.remove('d-none');
            } else {
                barsIcon.classList.remove('d-none');
                timesIcon.classList.add('d-none');
            }
        } else { // Mobile
            barsIcon.classList.remove('d-none');
            timesIcon.classList.add('d-none');
        }
    }
    */

    // Event Listener para o botão de toggle principal (na top-navbar)
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            if (window.innerWidth > DESKTOP_BREAKPOINT) {
                toggleSidebarDesktop();
            } else {
                openSidebarMobile();
            }
        });
    }

    // Event Listener para o botão de fechar dentro da sidebar (só mobile)
    if (closeSidebarMobileBtn) {
        closeSidebarMobileBtn.addEventListener('click', closeSidebarMobile);
    }

    // Event Listener para o overlay mobile
    if (overlayMobile) {
        overlayMobile.addEventListener('click', closeSidebarMobile);
    }

    // Lógica inicial e no redimensionamento da tela
    function adjustSidebarState() {
        if (window.innerWidth > DESKTOP_BREAKPOINT) {
            if (!body.classList.contains('sidebar-expanded-desktop')) {
                body.classList.add('sidebar-minimized-desktop');
                body.classList.remove('sidebar-expanded-desktop');
                toggleBtn.setAttribute('aria-expanded', false);
            } else {
                toggleBtn.setAttribute('aria-expanded', true);
            }
            body.classList.remove('sidebar-open-mobile');
            body.classList.remove('sidebar-closed-mobile');
            overlayMobile.style.display = 'none';
        } else {
            body.classList.remove('sidebar-expanded-desktop');
            body.classList.remove('sidebar-minimized-desktop');
            body.classList.add('sidebar-closed-mobile');
            body.classList.remove('sidebar-open-mobile');
            overlayMobile.style.display = 'none';
            toggleBtn.setAttribute('aria-expanded', false);
        }
        // REMOVIDO: updateToggleIcon() não é mais chamada aqui
    }

    // Ajusta o estado da sidebar ao carregar a página
    adjustSidebarState();

    // Ajusta o estado da sidebar ao redimensionar a janela
    window.addEventListener('resize', adjustSidebarState);

    // Fecha a sidebar ao clicar em um item de menu (apenas em mobile)
    const sidebarLinks = document.querySelectorAll('.sidebar-menu-item a');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= DESKTOP_BREAKPOINT) {
                closeSidebarMobile();
            }
        });
    });

    // Ajuste do título da página na top-navbar (exemplo)
    const currentPageTitle = document.querySelector('.current-page-title');
    const updatePageTitle = () => {
        const path = window.location.pathname;
        let title = 'Dashboard';
        if (path.includes('/dashboard')) {
            title = 'Dashboard';
        } else if (path.includes('/users')) {
            title = 'Usuários';
        } else if (path.includes('/reports')) {
            title = 'Relatórios';
        } else if (path.includes('/settings')) {
            title = 'Configurações';
        }
        currentPageTitle.textContent = title;
    };

    updatePageTitle();
});