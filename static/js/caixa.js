console.log('🚀 [CAIXA.JS] Arquivo carregado!');

let itensPedido = [];
let estoqueProdutos = {}; // Cache de estoque dos produtos

// Função para obter estoque de um produto
function obterEstoqueProduto(produtoId) {
    const card = document.querySelector(`.produto-card-cardapio[data-codigo="${produtoId}"]`);
    if (card) {
        const estoque = parseInt(card.dataset.estoque || '0');
        estoqueProdutos[produtoId] = estoque;
        return estoque;
    }
    return estoqueProdutos[produtoId] || 0;
}

function adicionarProduto(id, nome, preco) {
    console.log('adicionarProduto chamado:', {id, nome, preco});
    
    // Verificar estoque disponível
    const estoqueDisponivel = obterEstoqueProduto(id);
    const itemExistente = itensPedido.find(item => item.produto_id === id && !item.is_combo);
    const quantidadeAtual = itemExistente ? itemExistente.quantidade : 0;
    
    // Calcular quanto deste produto já está sendo usado em combos
    let quantidadeEmCombos = 0;
    itensPedido.forEach(item => {
        if (item.is_combo) {
            item.escolhas.forEach(escolha => {
                if (escolha.produto_id === id) {
                    quantidadeEmCombos += escolha.quantidade_abate * item.quantidade;
                }
            });
        }
    });
    
    const estoqueRestante = estoqueDisponivel - quantidadeEmCombos;
    
    console.log(`Estoque disponível: ${estoqueDisponivel}, Em combos: ${quantidadeEmCombos}, Restante: ${estoqueRestante}, Quantidade no carrinho: ${quantidadeAtual}`);
    
    // Validar se há estoque suficiente
    if (quantidadeAtual >= estoqueRestante) {
        alert(`❌ Estoque insuficiente!\n\n${nome}\nDisponível: ${estoqueDisponivel} unidade(s)\nEm combos: ${quantidadeEmCombos} unidade(s)\nRestante: ${estoqueRestante} unidade(s)\nNo carrinho: ${quantidadeAtual} unidade(s)`);
        return;
    }
    
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
    
    console.log('itensPedido após adicionar:', itensPedido);
    atualizarListaItens();
}

function removerProduto(index) {
    itensPedido.splice(index, 1);
    atualizarListaItens();
}

function alterarQuantidade(index, delta) {
    const item = itensPedido[index];
    const novaQuantidade = item.quantidade + delta;
    
    // Se está diminuindo, permitir
    if (delta < 0) {
        if (novaQuantidade <= 0) {
            removerProduto(index);
        } else {
            item.quantidade = novaQuantidade;
            atualizarListaItens();
        }
        return;
    }
    
    // Se está aumentando, verificar estoque
    if (item.is_combo) {
        // Para combos, verificar estoque de cada componente
        for (const escolha of item.escolhas) {
            const estoqueDisponivel = obterEstoqueProduto(escolha.produto_id);
            const quantidadeNecessaria = escolha.quantidade_abate * novaQuantidade;
            
            // Calcular quanto já está sendo usado por outros itens no carrinho
            let quantidadeUsada = 0;
            itensPedido.forEach((outroItem, outroIndex) => {
                if (outroIndex === index) return; // Pular o item atual
                
                if (outroItem.is_combo) {
                    // Verificar se este combo usa o mesmo produto
                    outroItem.escolhas.forEach(outraEscolha => {
                        if (outraEscolha.produto_id === escolha.produto_id) {
                            quantidadeUsada += outraEscolha.quantidade_abate * outroItem.quantidade;
                        }
                    });
                } else if (outroItem.produto_id === escolha.produto_id) {
                    quantidadeUsada += outroItem.quantidade;
                }
            });
            
            const estoqueRestante = estoqueDisponivel - quantidadeUsada;
            
            if (quantidadeNecessaria > estoqueRestante) {
                alert(`❌ Estoque insuficiente!\n\n${escolha.produto_nome}\nDisponível: ${estoqueDisponivel} unidade(s)\nEm uso: ${quantidadeUsada} unidade(s)\nRestante: ${estoqueRestante} unidade(s)\nNecessário: ${quantidadeNecessaria} unidade(s)`);
                return;
            }
        }
    } else {
        // Para produtos normais, verificar estoque considerando uso em combos
        const estoqueDisponivel = obterEstoqueProduto(item.produto_id);
        
        // Calcular quanto já está sendo usado em combos
        let quantidadeEmCombos = 0;
        itensPedido.forEach((outroItem, outroIndex) => {
            if (outroIndex === index) return; // Pular o item atual
            
            if (outroItem.is_combo) {
                outroItem.escolhas.forEach(escolha => {
                    if (escolha.produto_id === item.produto_id) {
                        quantidadeEmCombos += escolha.quantidade_abate * outroItem.quantidade;
                    }
                });
            }
        });
        
        const estoqueRestante = estoqueDisponivel - quantidadeEmCombos;
        
        if (novaQuantidade > estoqueRestante) {
            alert(`❌ Estoque insuficiente!\n\n${item.nome}\nDisponível: ${estoqueDisponivel} unidade(s)\nEm combos: ${quantidadeEmCombos} unidade(s)\nRestante: ${estoqueRestante} unidade(s)\nNo carrinho: ${item.quantidade} unidade(s)`);
            return;
        }
    }
    
    item.quantidade = novaQuantidade;
    atualizarListaItens();
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
        const observacoes = document.getElementById('observacoes')?.value || '';
        
        const carrinho = {
            cliente_nome: clienteNome,
            tipo: tipo,
            pagamento: pagamento,
            observacoes: observacoes,
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
    const observacoesTextarea = document.getElementById('observacoes');
    
    if (clienteNomeInput) {
        clienteNomeInput.addEventListener('input', salvarCarrinhoTemporario);
    }
    if (tipoPedidoSelect) {
        tipoPedidoSelect.addEventListener('change', salvarCarrinhoTemporario);
    }
    if (formaPagamentoSelect) {
        formaPagamentoSelect.addEventListener('change', salvarCarrinhoTemporario);
    }
    if (observacoesTextarea) {
        observacoesTextarea.addEventListener('input', salvarCarrinhoTemporario);
    }
});

async function finalizarPedido() {
    console.log('🎯 [FINALIZAR] Função finalizarPedido chamada!');
    
    // Validação 1: Verificar se há itens no carrinho
    if (itensPedido.length === 0) {
        console.log('❌ [FINALIZAR] Carrinho vazio');
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
            console.log('✅ [FINALIZAR] Pedido criado com sucesso!', result);
            
            // Limpar localStorage do carrinho
            localStorage.removeItem('caixa_carrinho_temp');
            
            // Notificar visão cliente para limpar a tela
            localStorage.setItem('pedido_finalizado', JSON.stringify({
                action: 'limpar_tela',
                pedido_id: result.pedido_id,
                timestamp: Date.now()
            }));
            
            // Remover após 100ms para permitir que outras abas detectem
            setTimeout(() => {
                localStorage.removeItem('pedido_finalizado');
            }, 100);
            
            // Salvar QR Code no localStorage para reabrir após reload
            localStorage.setItem('qrcode_pendente', JSON.stringify({
                qr_code: result.qr_code,
                numero_pedido: result.numero_pedido,
                timestamp: Date.now()
            }));
            
            // Disparar evento de atualização de estoque
            const eventoEstoque = {
                action: 'pedido_finalizado',
                timestamp: Date.now(),
                pedido_id: result.pedido_id
            };
            console.log('📦 [FINALIZAR] Disparando evento de atualização de estoque:', eventoEstoque);
            localStorage.setItem('estoque_atualizado', JSON.stringify(eventoEstoque));
            
            // Remover após 100ms para permitir que outras abas detectem
            setTimeout(() => {
                localStorage.removeItem('estoque_atualizado');
            }, 100);
            
            // ATUALIZAÇÃO IMEDIATA: Recarregar a página após 500ms
            console.log('🔄 [FINALIZAR] Agendando reload da página em 500ms...');
            setTimeout(() => {
                console.log('🔄 [FINALIZAR] Recarregando página...');
                window.location.reload();
            }, 500);
            
            // Limpar formulário
            itensPedido = [];
            atualizarListaItens();
            document.getElementById('cliente-nome').value = '';
            document.getElementById('observacoes').value = '';
            document.getElementById('tipo-pedido').selectedIndex = 0;
            document.getElementById('forma-pagamento').selectedIndex = 0;
        } else {
            console.log('❌ [FINALIZAR] Erro ao criar pedido:', result.error);
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

