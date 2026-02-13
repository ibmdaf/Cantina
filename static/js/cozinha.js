async function atualizarStatus(pedidoId, novoStatus) {
    try {
        const formData = new FormData();
        formData.append('status', novoStatus);
        formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
        
        const response = await fetch(`/cozinha/atualizar-status/${pedidoId}/`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            location.reload();
        } else {
            alert('Erro ao atualizar status!');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao atualizar status!');
    }
}

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

// Auto-refresh a cada 30 segundos
setInterval(() => {
    location.reload();
}, 30000);
