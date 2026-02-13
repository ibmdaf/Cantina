let itensPedido = [];

function adicionarProduto(id, nome, preco) {
    const itemExistente = itensPedido.find(item => item.produto_id === id);
    
    if (itemExistente) {
        itemExistente.quantidade++;
    } else {
        itensPedido.push({
            produto_id: id,
            nome: nome,
            preco: parseFloat(preco),
            quantidade: 1,
            observacoes: ''
        });
    }
    
    atualizarListaItens();
}

function removerProduto(index) {
    itensPedido.splice(index, 1);
    atualizarListaItens();
}

function alterarQuantidade(index, delta) {
    itensPedido[index].quantidade += delta;
    if (itensPedido[index].quantidade <= 0) {
        removerProduto(index);
    } else {
        atualizarListaItens();
    }
}

function atualizarListaItens() {
    const listaItens = document.getElementById('lista-itens');
    const totalElement = document.getElementById('total-pedido');
    const itensCount = document.getElementById('itens-count');
    const btnFinalizar = document.querySelector('.btn-finalizar-pedido-full');
    
    if (itensPedido.length === 0) {
        listaItens.innerHTML = `
            <div class="carrinho-vazio">
                <div class="carrinho-vazio-icon">🛒</div>
                <p>Carrinho vazio</p>
                <small>Clique nos itens do cardápio para adicionar</small>
            </div>
        `;
        totalElement.textContent = '0.00';
        itensCount.textContent = '0';
        btnFinalizar.disabled = true;
        
        // Limpar localStorage
        localStorage.removeItem('caixa_carrinho_temp');
        return;
    }
    
    let html = '';
    let total = 0;
    
    itensPedido.forEach((item, index) => {
        const subtotal = item.preco * item.quantidade;
        total += subtotal;
        
        html += `
            <div class="item-carrinho">
                <div class="item-info">
                    <div class="item-nome">${item.nome}</div>
                    <div class="item-detalhes">R$ ${item.preco.toFixed(2)} x ${item.quantidade} = R$ ${subtotal.toFixed(2)}</div>
                </div>
                <div class="item-acoes">
                    <button onclick="alterarQuantidade(${index}, -1)" class="btn-qty">-</button>
                    <span class="item-quantidade">${item.quantidade}</span>
                    <button onclick="alterarQuantidade(${index}, 1)" class="btn-qty">+</button>
                    <button onclick="removerProduto(${index})" class="btn-remove">🗑️</button>
                </div>
            </div>
        `;
    });
    
    listaItens.innerHTML = html;
    totalElement.textContent = total.toFixed(2);
    itensCount.textContent = itensPedido.length;
    btnFinalizar.disabled = false;
    
    // Salvar no localStorage para espelhamento em tempo real
    salvarCarrinhoTemporario();
}

function salvarCarrinhoTemporario() {
    try {
        const clienteNome = document.getElementById('cliente-nome')?.value || '';
        const tipo = document.getElementById('tipo-pedido')?.value || 'balcao';
        const pagamento = document.getElementById('forma-pagamento')?.value || 'dinheiro';
        
        const carrinho = {
            cliente_nome: clienteNome,
            tipo: tipo,
            pagamento: pagamento,
            itens: itensPedido,
            timestamp: new Date().getTime()
        };
        
        localStorage.setItem('caixa_carrinho_temp', JSON.stringify(carrinho));
    } catch (error) {
        console.error('Erro ao salvar carrinho temporário:', error);
    }
}

// Busca de produtos no cardápio
document.addEventListener('DOMContentLoaded', function() {
    const buscaInput = document.getElementById('busca-item');
    if (buscaInput) {
        buscaInput.addEventListener('input', function(e) {
            const termo = e.target.value.toLowerCase();
            const produtos = document.querySelectorAll('.produto-card-cardapio');
            
            produtos.forEach(produto => {
                const nome = produto.dataset.nome;
                const codigo = produto.dataset.codigo;
                
                if (nome.includes(termo) || codigo.includes(termo)) {
                    produto.style.display = 'flex';
                } else {
                    produto.style.display = 'none';
                }
            });
        });
    }
    
    // Listeners para atualizar carrinho em tempo real
    const clienteNomeInput = document.getElementById('cliente-nome');
    const tipoPedidoSelect = document.getElementById('tipo-pedido');
    const formaPagamentoSelect = document.getElementById('forma-pagamento');
    
    if (clienteNomeInput) {
        clienteNomeInput.addEventListener('input', salvarCarrinhoTemporario);
    }
    if (tipoPedidoSelect) {
        tipoPedidoSelect.addEventListener('change', salvarCarrinhoTemporario);
    }
    if (formaPagamentoSelect) {
        formaPagamentoSelect.addEventListener('change', salvarCarrinhoTemporario);
    }
});

async function finalizarPedido() {
    // Validação 1: Verificar se há itens no carrinho
    if (itensPedido.length === 0) {
        alert('❌ Adicione pelo menos um item ao pedido!');
        return;
    }
    
    // Validação 2: Verificar nome do cliente
    const clienteNome = document.getElementById('cliente-nome').value.trim();
    if (!clienteNome) {
        alert('❌ Por favor, informe o nome do cliente!');
        document.getElementById('cliente-nome').focus();
        return;
    }
    
    // Validação 3: Verificar forma de pagamento
    const formaPagamento = document.getElementById('forma-pagamento').value;
    if (!formaPagamento) {
        alert('❌ Por favor, selecione uma forma de pagamento!');
        document.getElementById('forma-pagamento').focus();
        return;
    }
    
    const dados = {
        tipo: document.getElementById('tipo-pedido').value,
        cliente_nome: clienteNome,
        forma_pagamento: formaPagamento,
        observacoes: document.getElementById('observacoes').value,
        itens: itensPedido
    };
    
    console.log('Enviando pedido:', dados);
    
    try {
        const response = await fetch('/caixa/criar-pedido/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(dados)
        });
        
        console.log('Response status:', response.status);
        const result = await response.json();
        console.log('Response data:', result);
        
        if (result.success) {
            // Limpar localStorage
            localStorage.removeItem('caixa_carrinho_temp');
            
            // Mostrar modal com QR Code
            mostrarQRCode(result.qr_code);
            
            // Limpar formulário
            itensPedido = [];
            atualizarListaItens();
            document.getElementById('cliente-nome').value = '';
            document.getElementById('observacoes').value = '';
            document.getElementById('tipo-pedido').selectedIndex = 0;
            document.getElementById('forma-pagamento').selectedIndex = 0;
        } else {
            alert('❌ Erro ao criar pedido: ' + (result.error || 'Erro desconhecido'));
        }
    } catch (error) {
        console.error('Erro completo:', error);
        alert('❌ Erro ao criar pedido! Verifique sua conexão.');
    }
}

// Filtro de categoria
document.getElementById('categoria-filter')?.addEventListener('change', function() {
    const categoriaId = this.value;
    const produtos = document.querySelectorAll('.produto-card');
    
    produtos.forEach(produto => {
        if (!categoriaId || produto.dataset.categoria === categoriaId) {
            produto.style.display = 'block';
        } else {
            produto.style.display = 'none';
        }
    });
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

