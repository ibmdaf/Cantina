from django.shortcuts import render, redirect
from django.http import JsonResponse
from caixa.models import Produto, Categoria, Pedido, ItemPedido
from authentication.models import Empresa
from decimal import Decimal
import json

def autoatendimento_home(request, empresa_id):
    empresa = Empresa.objects.get(id=empresa_id)
    categorias = Categoria.objects.filter(empresa=empresa, ativo=True)
    produtos = Produto.objects.filter(empresa=empresa, ativo=True)
    
    context = {
        'empresa': empresa,
        'categorias': categorias,
        'produtos': produtos,
    }
    return render(request, 'autoatendimento/home.html', context)

def criar_pedido_autoatendimento(request, empresa_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        empresa = Empresa.objects.get(id=empresa_id)
        
        pedido = Pedido.objects.create(
            empresa=empresa,
            tipo='autoatendimento',
            cliente_nome=data.get('cliente_nome', 'Cliente'),
            mesa=data.get('mesa', ''),
            observacoes=data.get('observacoes', '')
        )
        
        total = Decimal('0.00')
        for item in data.get('itens', []):
            produto = Produto.objects.get(id=item['produto_id'])
            item_pedido = ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=item['quantidade'],
                preco_unitario=produto.preco,
                observacoes=item.get('observacoes', '')
            )
            total += item_pedido.subtotal
        
        pedido.total = total
        pedido.save()
        
        return JsonResponse({
            'success': True,
            'pedido_id': pedido.id,
            'numero_pedido': pedido.numero_pedido,
            'qr_code': str(pedido.qr_code)
        })
    
    return JsonResponse({'success': False})

def confirmacao_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    context = {
        'pedido': pedido,
    }
    return render(request, 'autoatendimento/confirmacao.html', context)
