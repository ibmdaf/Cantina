from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from caixa.models import Pedido

def acompanhar_pedido(request, qr_code):
    pedido = get_object_or_404(Pedido, qr_code=qr_code)
    context = {
        'pedido': pedido,
    }
    return render(request, 'acompanhamento/acompanhar.html', context)

def status_pedido_api(request, qr_code):
    pedido = get_object_or_404(Pedido, qr_code=qr_code)
    
    data = {
        'numero_pedido': pedido.numero_pedido,
        'status': pedido.status,
        'status_display': pedido.get_status_display(),
        'tipo': pedido.get_tipo_display(),
        'mesa': pedido.mesa,
        'total': str(pedido.total),
        'itens': [{
            'produto': item.produto.nome,
            'quantidade': item.quantidade,
            'preco': str(item.preco_unitario),
            'subtotal': str(item.subtotal)
        } for item in pedido.itens.all()],
        'criado_em': pedido.criado_em.strftime('%d/%m/%Y %H:%M'),
        'atualizado_em': pedido.atualizado_em.strftime('%d/%m/%Y %H:%M')
    }
    
    return JsonResponse(data)
