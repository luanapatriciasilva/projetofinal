document.addEventListener('DOMContentLoaded', function() {
    // Atualizar ano no footer
    const currentYearSpan = document.getElementById('currentYear');
    if (currentYearSpan) {
        currentYearSpan.textContent = new Date().getFullYear();
    }

    // Adicionar classe 'scrolled' ao header ao rolar a página (opcional, para efeitos)
    const headerNavbar = document.querySelector('header .navbar');
    if (headerNavbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                headerNavbar.classList.add('scrolled');
            } else {
                headerNavbar.classList.remove('scrolled');
            }
        });
    }
    // Para usar o efeito 'scrolled', adicione no seu style.css:
    /*
    .custom-navbar.scrolled {
        background: linear-gradient(90deg, #083b73, #16518f); // Um pouco mais escuro
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        padding-top: 0.6rem; // Exemplo de como pode encolher um pouco
        padding-bottom: 0.6rem;
    }
    .custom-navbar.scrolled .navbar-brand {
        font-size: 1.4rem; // Exemplo
    }
    */
});