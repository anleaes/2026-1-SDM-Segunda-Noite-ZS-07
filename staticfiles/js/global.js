document.addEventListener("DOMContentLoaded", function () {
    const verMaisEsp = document.getElementById('ver-mais-esp');
    const verMaisChar = document.getElementById('ver-mais-char');

    if (verMaisEsp) {
        verMaisEsp.addEventListener('click', function () {
            const itensExtras = document.querySelectorAll('.extra-specie');
            
            if (itensExtras.length === 0) return;

            const estaoEscondidos = itensExtras[0].classList.contains('d-none');

            if (estaoEscondidos) {
                itensExtras.forEach(item => item.classList.remove('d-none'));
                
                this.textContent = 'Ver menos';
            } else {
                itensExtras.forEach(item => item.classList.add('d-none'));
                
                this.textContent = 'Ver mais';
            }
        });
    }

    if (verMaisChar) {
        verMaisChar.addEventListener('click', function () {
            const itensExtras = document.querySelectorAll('.extra-char');
            
            if (itensExtras.length === 0) return;

            const estaoEscondidos = itensExtras[0].classList.contains('d-none');

            if (estaoEscondidos) {
                itensExtras.forEach(item => item.classList.remove('d-none'));
                
                this.textContent = 'Ver menos';
            } else {
                itensExtras.forEach(item => item.classList.add('d-none'));
                
                this.textContent = 'Ver mais';
            }
        });
    }
});