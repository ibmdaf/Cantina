from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from caixa.models import Pedido
from django.utils import timezone

@login_required
def cozinha_dashboard(request):
    empresa = request.user.empresa
    
    # Buscar apenas pedidos ativos (pendente, preparando, pronto)
    pedidos_ativos = Pedido.objects.filter(
        empresa=empresa,
        status__in=['pendente', 'preparando', 'pronto']
    ).order_by('criado_em').prefetch_related('itens__produto')
    
    context = {
        'pedidos_ativos': pedidos_ativos,
    }
    
    response = render(request, 'cozinha/dashboard_new.html', context)
    
    # Desabilitar cache para forçar reload do template
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

@login_required
def atualizar_status_pedido(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id, empresa=request.user.empresa)
        novo_status = request.POST.get('status')
        
        if novo_status in dict(Pedido.STATUS_CHOICES):
            pedido.status = novo_status
            pedido.save()
            return JsonResponse({'success': True, 'status': novo_status})
    
    return JsonResponse({'success': False})

@login_required
def listar_pedidos_cozinha(request):
    empresa = request.user.empresa
    status = request.GET.get('status', 'pendente')
    
    pedidos = Pedido.objects.filter(
        empresa=empresa,
        status=status
    ).order_by('criado_em')
    
    data = [{
        'id': p.id,
        'numero_pedido': p.numero_pedido,
        'tipo': p.get_tipo_display(),
        'mesa': p.mesa,
        'status': p.get_status_display(),
        'itens': [{
            'produto': item.produto.nome,
            'quantidade': item.quantidade,
            'observacoes': item.observacoes
        } for item in p.itens.all()],
        'criado_em': p.criado_em.strftime('%H:%M')
    } for p in pedidos]
    
    return JsonResponse({'pedidos': data})


@login_required
def api_pedidos_cozinha(request):
    """
    API para retornar pedidos ativos em tempo real (JSON)
    Inclui estatísticas de status e tempo médio
    """
    from datetime import timedelta
    from django.db.models import Avg, Count, Q
    import logging
    
    logger = logging.getLogger(__name__)
    empresa = request.user.empresa
    
    pedidos_ativos = Pedido.objects.filter(
        empresa=empresa,
        status__in=['pendente', 'preparando', 'pronto']
    ).order_by('criado_em').prefetch_related('itens__produto')
    
    # Calcular estatísticas
    total_pendente = pedidos_ativos.filter(status='pendente').count()
    total_preparando = pedidos_ativos.filter(status='preparando').count()
    total_pronto = pedidos_ativos.filter(status='pronto').count()
    
    logger.info(f"Pedidos ativos - Pendente: {total_pendente}, Preparando: {total_preparando}, Pronto: {total_pronto}")
    
    # Calcular tempo médio dos pedidos ENTREGUES HOJE
    hoje = timezone.now().date()
    
    pedidos_entregues_hoje = Pedido.objects.filter(
        empresa=empresa,
        status='entregue',
        atualizado_em__date=hoje
    )
    
    tempo_medio_segundos = 0
    if pedidos_entregues_hoje.exists():
        tempos = []
        for pedido in pedidos_entregues_hoje:
            # Tempo desde criação até entrega (atualizado_em)
            tempo_decorrido = (pedido.atualizado_em - pedido.criado_em).total_seconds()
            
            # Ignorar pedidos com tempo muito alto (mais de 2 horas = possível erro)
            if tempo_decorrido <= 7200:  # 2 horas em segundos
                tempos.append(tempo_decorrido)
        
        if tempos:
            tempo_medio_segundos = sum(tempos) / len(tempos)
            logger.info(f"Tempo médio de entrega (hoje): {tempo_medio_segundos}s ({tempo_medio_segundos/60:.1f}min)")
        else:
            logger.info("Nenhum pedido válido para calcular tempo médio (todos > 2h)")
    else:
        logger.info("Nenhum pedido entregue hoje para calcular tempo médio")
    
    pedidos_data = []
    for pedido in pedidos_ativos:
        itens_data = []
        for item in pedido.itens.all():
            itens_data.append({
                'quantidade': item.quantidade,
                'produto_nome': item.produto.nome,
                'observacoes': item.observacoes or ''
            })
        
        pedidos_data.append({
            'id': pedido.id,
            'numero_pedido': pedido.numero_pedido,
            'cliente_nome': pedido.cliente_nome or '',
            'tipo': pedido.tipo,
            'status': pedido.status,
            'criado_em': pedido.criado_em.isoformat(),
            'itens': itens_data
        })
    
    estatisticas = {
        'total_pendente': total_pendente,
        'total_preparando': total_preparando,
        'total_pronto': total_pronto,
        'tempo_medio_segundos': int(tempo_medio_segundos),
        'total_pedidos': len(pedidos_data)
    }
    
    logger.info(f"Retornando estatísticas: {estatisticas}")
    
    return JsonResponse({
        'success': True,
        'pedidos': pedidos_data,
        'estatisticas': estatisticas
    })
