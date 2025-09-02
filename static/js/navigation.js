// Navigation accessible (burger + focus trap)
document.addEventListener('DOMContentLoaded', () => {
    const burger = document.getElementById('burger-btn');
    const nav = document.getElementById('primary-nav');
    if (!burger || !nav) return;

    const focusableSelectors = 'a, button, [tabindex]:not([tabindex="-1"])';
    let lastFocused = null;

    function openMenu() {
        lastFocused = document.activeElement;
        burger.setAttribute('aria-expanded', 'true');
        nav.classList.add('open');
        document.body.classList.add('nav-open');
        const first = nav.querySelector(focusableSelectors);
        if (first) first.focus();
    }

    function closeMenu() {
        burger.setAttribute('aria-expanded', 'false');
        nav.classList.remove('open');
        document.body.classList.remove('nav-open');
        if (lastFocused) lastFocused.focus();
    }

    burger.addEventListener('click', () => {
        const expanded = burger.getAttribute('aria-expanded') === 'true';
        if (expanded) closeMenu(); else openMenu();
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') {
            e.preventDefault();
            closeMenu();
        }
        if (e.key === 'Tab' && burger.getAttribute('aria-expanded') === 'true') {
            const items = Array.from(nav.querySelectorAll(focusableSelectors));
            if (items.length === 0) return;
            const first = items[0];
            const last = items[items.length - 1];
            if (e.shiftKey && document.activeElement === first) {
                e.preventDefault();
                last.focus();
            } else if (!e.shiftKey && document.activeElement === last) {
                e.preventDefault();
                first.focus();
            }
        }
    });

    // Fermer au clic extérieur
    document.addEventListener('click', (e) => {
        if (burger.getAttribute('aria-expanded') !== 'true') return;
        if (!nav.contains(e.target) && e.target !== burger) {
            closeMenu();
        }
    });
});


