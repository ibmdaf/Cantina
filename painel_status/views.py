from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from caixa.models import Pedido
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta

@login_required
def painel_status(request):
    empresa = request.user.empresa
    
    # Estatísticas do dia
    hoje = timezone.now().date()
    pedidos_hoje = Pedido.objects.filter(
        empresa=empresa,
        criado_em__date=hoje
    )
    
    stats = {
        'total_pedidos': pedidos_hoje.count(),
        'total_vendas': pedidos_hoje.aggregate(Sum('total'))['total__sum'] or 0,
        'pedidos_pendentes': pedidos_hoje.filter(status='pendente').count(),
        'pedidos_preparando': pedidos_hoje.filter(status='preparando').count(),
        'pedidos_prontos': pedidos_hoje.filter(status='pronto').count(),
        'pedidos_entregues': pedidos_hoje.filter(status='entregue').count(),
    }
    
    # Pedidos ativos
    pedidos_ativos = Pedido.objects.filter(
        empresa=empresa,
        status__in=['pendente', 'preparando', 'pronto']
    ).order_by('criado_em')
    
    context = {
        'stats': stats,
        'pedidos_ativos': pedidos_ativos,
    }
    return render(request, 'painel_status/painel.html', context)

@login_required
def painel_status_api(request):
    empresa = request.user.empresa
    
    pedidos = Pedido.objects.filter(
        empresa=empresa,
        status__in=['pendente', 'preparando', 'pronto']
    ).order_by('criado_em')
    
    data = [{
        'id': p.id,
        'numero_pedido': p.numero_pedido,
        'tipo': p.get_tipo_display(),
        'mesa': p.mesa,
        'status': p.status,
        'status_display': p.get_status_display(),
        'total': str(p.total),
        'tempo_decorrido': str(timezone.now() - p.criado_em).split('.')[0],
        'itens_count': p.itens.count()
    } for p in pedidos]
    
    return JsonResponse({'pedidos': data})
