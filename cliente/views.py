from django.shortcuts import render
from django.http import JsonResponse
from caixa.models import Produto, Categoria, Pedido
from authentication.models import Empresa

def cardapio_cliente(request, empresa_id):
    empresa = Empresa.objects.get(id=empresa_id)
    categorias = Categoria.objects.filter(empresa=empresa, ativo=True)
    produtos = Produto.objects.filter(empresa=empresa, ativo=True).order_by('nome')
    
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
        ).order_by('-criado_em').first()
        
        if pedido:
            # Mapear tipo para display
            tipo_map = {
                'balcao': '⛪ Local',
                'delivery': '🚗 Viagem',
                'mesa': '🪑 Mesa',
                'autoatendimento': '🖥️ Autoatendimento'
            }
            
            itens = [{
                'produto_nome': item.produto.nome,
                'quantidade': item.quantidade,
                'preco_unitario': str(item.preco_unitario),
                'subtotal': str(item.subtotal)
            } for item in pedido.itens.all()]
            
            return JsonResponse({
                'pedido': {
                    'id': pedido.id,
                    'numero_pedido': pedido.numero_pedido,
                    'cliente_nome': pedido.cliente_nome or 'Cliente',
                    'tipo_display': tipo_map.get(pedido.tipo, pedido.tipo),
                    'pagamento': 'Não informado',  # Pode adicionar campo no modelo depois
                    'itens': itens,
                    'total': str(pedido.total),
                    'atualizado': pedido.atualizado_em.isoformat()
                }
            })
        else:
            return JsonResponse({'pedido': None})
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
