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

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function abrirModalTexto(id, entidade, acao, titulo, valorAtual) {
    document.getElementById('modalTextoId').value = id;
    document.getElementById('modalTextoAcao').value = acao;
    document.getElementById('modalTextoEntidade').value = entidade;
    document.getElementById('modalTextoTitulo').innerText = titulo;
    
    const input = document.getElementById('modalTextoInput');
    input.value = valorAtual;
    input.type = acao === 'password' ? 'password' : 'text'; 

    new bootstrap.Modal(document.getElementById('modalEdicaoTexto')).show();
}

function abrirModalNivel(id, nivelAtual) {
    document.getElementById('modalNivelId').value = id;
    
    const badge = document.getElementById('nivelAtualBadge');
    if (nivelAtual === 'admin') {
        badge.innerText = 'Administrador';
        badge.className = 'badge bg-danger fs-6 ms-2';
        document.getElementById('radioAdmin').checked = true;
    } else {
        badge.innerText = 'Moderador';
        badge.className = 'badge bg-primary fs-6 ms-2';
        document.getElementById('radioMod').checked = true;
    }

    new bootstrap.Modal(document.getElementById('modalEdicaoNivel')).show();
}

async function enviarRequisicao(id, entidade, endpointPatch, payload) {
    const rotaBase = entidade === 'employee' ? '/funcionarios' : '/adotantes';
    
    try {
        const response = await fetch(`${rotaBase}/${id}/${endpointPatch}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        
        if (response.ok) {
            window.location.reload(); 
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
        alert('Erro de conexão com o servidor.');
    }
}

function enviarEdicaoTexto() {
    const id = document.getElementById('modalTextoId').value;
    const acao = document.getElementById('modalTextoAcao').value;
    const entidade = document.getElementById('modalTextoEntidade').value;
    const valor = document.getElementById('modalTextoInput').value;

    if (!valor) return alert("O campo não pode estar vazio!");

    let endpoint = '';
    let payload = {};

    if (acao === 'username') {
        endpoint = 'alterar_username';
        payload = { username: valor };
    } else if (acao === 'password') {
        endpoint = 'alterar_senha';
        payload = { new_password: valor };
    } else if (acao === 'position') {
        endpoint = 'alterar_cargo';
        payload = { position: valor }; 
    } else if (acao === 'address') {
        endpoint = 'alterar_endereco';
        payload = { address: valor };
    }

    enviarRequisicao(id, entidade, endpoint, payload);
}

function enviarEdicaoNivel() {
    const id = document.getElementById('modalNivelId').value;
    const valor = document.querySelector('input[name="nivelRadio"]:checked').value;
    
    enviarRequisicao(id, 'employee', 'alterar_cargo', { role: valor });
}