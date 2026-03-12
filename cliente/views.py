from django.shortcuts import render
from django.http import JsonResponse
from caixa.models import Produto, Categoria, Pedido
from authentication.models import Empresa

def cardapio_cliente(request, empresa_id):
    from django.db.models import Q
    
    empresa = Empresa.objects.get(id=empresa_id)
    categorias = Categoria.objects.filter(empresa=empresa, ativo=True)
    
    # Filtrar apenas produtos ativos E com estoque > 0 ou combos
    produtos_raw = Produto.objects.filter(
        empresa=empresa, 
        ativo=True
    ).filter(
        Q(quantidade_estoque__gt=0) | Q(combo__isnull=False)
    ).select_related('categoria')
    
    # Ordenação customizada: Combos primeiro, Bebidas penúltimo, Sobremesas último
    produtos_combo = []
    produtos_outros = []
    produtos_bebidas = []
    produtos_sobremesas = []
    
    for produto in produtos_raw:
        categoria_nome = produto.categoria.nome.lower() if produto.categoria else ''
        
        if produto.categoria and produto.categoria.is_sistema:  # Combo
            produtos_combo.append(produto)
        elif 'sobremesa' in categoria_nome:
            produtos_sobremesas.append(produto)
        elif 'bebida' in categoria_nome:
            produtos_bebidas.append(produto)
        else:
            produtos_outros.append(produto)
    
    # Ordenar cada grupo por nome
    produtos_combo.sort(key=lambda p: p.nome)
    produtos_outros.sort(key=lambda p: p.nome)
    produtos_bebidas.sort(key=lambda p: p.nome)
    produtos_sobremesas.sort(key=lambda p: p.nome)
    
    # Concatenar na ordem desejada
    produtos = produtos_combo + produtos_outros + produtos_bebidas + produtos_sobremesas
    
    context = {
        'empresa': empresa,
        'categorias': categorias,
        'produtos': produtos,
    }
    return render(request, 'cliente/cardapio.html', context)

def pedido_ativo_cliente(request, empresa_id):
    """Retorna o pedido mais recente que está sendo montado (status pendente)"""
    try:
        empresa = Empresa.objects.get(id=empresa_id)
        
        # Buscar o pedido mais recente com status pendente
        pedido = Pedido.objects.filter(
            empresa=empresa,
            status='pendente'
        ).order_by('-criado_em').prefetch_related(
            'itens__produto',
            'itens__escolhas_combo__produto_escolhido'
        ).first()
        
        if pedido:
            # Mapear tipo para display
            tipo_map = {
                'balcao': '⛪ Local',
                'delivery': '🚗 Viagem',
                'mesa': '🪑 Mesa',
                'autoatendimento': '🖥️ Autoatendimento'
            }
            
            itens = []
            for item in pedido.itens.all():
                item_dict = {
                    'produto_nome': item.produto.nome,
                    'quantidade': item.quantidade,
                    'preco_unitario': str(item.preco_unitario),
                    'subtotal': str(item.subtotal),
                    'observacoes': item.observacoes or '',
                    'is_combo': item.produto.is_combo()
                }
                
                # Se for combo, adicionar escolhas
                if item.produto.is_combo():
                    escolhas = []
                    for escolha in item.escolhas_combo.all():
                        escolhas.append({
                            'produto_nome': escolha.produto_escolhido.nome
                        })
                    item_dict['escolhas'] = escolhas
                
                itens.append(item_dict)
            
            return JsonResponse({
                'pedido': {
                    'id': pedido.id,
                    'numero_pedido': pedido.numero_pedido,
                    'cliente_nome': pedido.cliente_nome or 'Cliente',
                    'tipo_display': tipo_map.get(pedido.tipo, pedido.tipo),
                    'pagamento': 'Não informado',  # Pode adicionar campo no modelo depois
                    'observacoes': pedido.observacoes or '',
                    'itens': itens,
                    'total': str(pedido.total),
                    'atualizado': pedido.atualizado_em.isoformat()
                }
            })
        else:
            return JsonResponse({'pedido': None})
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
