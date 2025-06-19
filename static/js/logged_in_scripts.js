// static/js/logged_in_scripts.js

document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const mobileSidebarToggle = document.getElementById('mobileSidebarToggle');
    const mainContentArea = document.querySelector('.main-content-area');
    const mainFooter = document.querySelector('.main-footer'); // Seleciona o rodapé

    // Função para ajustar a largura do rodapé quando a sidebar é minimizada/expandida
    function adjustFooterWidth() {
        if (mainFooter) {
            const sidebarWidth = sidebar.offsetWidth;
            const sidebarLeftOffset = 20; // Corresponde ao `left: 20px` da sidebar
            const dashboardPaddingRight = 20; // Corresponde ao `padding: 20px` do .dashboard-wrapper
            
            // Largura total da tela menos (sidebar_width + sidebar_left_margin + dashboard_right_padding)
            mainFooter.style.width = `calc(100% - (${sidebarWidth}px + ${sidebarLeftOffset}px + ${dashboardPaddingRight}px))`;
            mainFooter.style.marginLeft = `${sidebarWidth + sidebarLeftOffset}px`;
        }
    }

    // Toggle para desktop
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('minimized');
            mainContentArea.classList.toggle('sidebar-minimized-main'); // Adiciona/remove classe para ajuste do main-content-area (se usar CSS)
            adjustFooterWidth(); // Ajusta o rodapé ao minimizar/expandir
        });
    }

    // Toggle para mobile (gaveta)
    if (mobileSidebarToggle) {
        mobileSidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');
            // Você pode querer adicionar um overlay aqui para fechar a sidebar clicando fora
            // const overlay = document.createElement('div');
            // overlay.classList.add('sidebar-overlay');
            // document.body.appendChild(overlay);
            // overlay.addEventListener('click', function() {
            //     sidebar.classList.remove('open');
            //     overlay.remove();
            // });
        });
    }

    // Ajustar o rodapé na carga inicial da página
    adjustFooterWidth();

    // Reajustar o rodapé e main-content-area em caso de redimensionamento da janela
    window.addEventListener('resize', function() {
        adjustFooterWidth();
        // Se você tiver um breakpoint de CSS que muda a largura da sidebar,
        // pode ser necessário recalcular o mainContentArea.style.marginLeft aqui também
        // ou confiar puramente no CSS com o seletor `+`
    });

    // Submenu toggle (opcional, se você tiver submenus)
    const menuItemsWithSubmenu = document.querySelectorAll('.sidebar-menu .menu-item.has-submenu');
    menuItemsWithSubmenu.forEach(item => {
        item.addEventListener('click', function(e) {
            // Evita que o link principal seja seguido se houver submenu
            e.preventDefault(); 
            const submenu = this.nextElementSibling; // O próximo elemento é o <ul> do submenu
            const dropdownIcon = this.querySelector('.dropdown-icon');

            if (submenu) {
                // Fecha outros submenus abertos (opcional)
                menuItemsWithSubmenu.forEach(otherItem => {
                    if (otherItem !== item && otherItem.classList.contains('expanded')) {
                        otherItem.classList.remove('expanded');
                        otherItem.nextElementSibling.style.display = 'none';
                        otherItem.querySelector('.dropdown-icon').style.transform = 'rotate(0deg)';
                    }
                });

                // Abre/fecha o submenu clicado
                this.classList.toggle('expanded');
                if (submenu.style.display === 'block') {
                    submenu.style.display = 'none';
                    dropdownIcon.style.transform = 'rotate(0deg)';
                } else {
                    submenu.style.display = 'block';
                    dropdownIcon.style.transform = 'rotate(180deg)';
                }
            }
        });
    });

    // Se o elemento .main-content-area não estiver sendo ajustado via CSS com `+`,
    // podemos fazer o ajuste via JS. O CSS puro com `+` é geralmente preferível,
    // mas este JS seria um fallback ou alternativa.
    /*
    if (sidebar && mainContentArea) {
        // Função para ajustar a margem esquerda do main-content-area
        const adjustMainContentMargin = () => {
            const sidebarWidth = sidebar.offsetWidth;
            const sidebarLeftOffset = 20; // Corresponde ao `left: 20px` da sidebar
            mainContentArea.style.marginLeft = `${sidebarWidth + sidebarLeftOffset}px`;
        };

        // Chama a função na carga inicial
        adjustMainContentMargin();

        // Chama a função quando a sidebar é minimizada/expandida
        sidebarToggle.addEventListener('click', adjustMainContentMargin);
        window.addEventListener('resize', adjustMainContentMargin); // Para responsividade
    }
    */
});