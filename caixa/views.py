from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from django.utils import timezone
from .models import Pedido, ItemPedido, Produto, Categoria, Combo, ComboSlot, ComboSlotItem, PedidoComboEscolha
from decimal import Decimal
import json

@login_required
def caixa_dashboard(request, aba='novo-pedido'):
    # Controle de acesso: usuário tipo "cozinha" não pode acessar
    if request.user.tipo == 'cozinha':
        return redirect('cozinha_dashboard')
    
    # Controle de acesso: operador de caixa não pode acessar abas restritas
    if request.user.tipo == 'caixa' and aba in ['configuracoes', 'usuarios']:
        return redirect('caixa_novo_pedido')
    
    empresa = request.user.empresa
    categorias = Categoria.objects.filter(empresa=empresa, ativo=True)
    
    # Mostrar todos os produtos na aba "Cardápio do Dia" para gerenciar disponibilidade
    todos_produtos_raw = Produto.objects.filter(empresa=empresa).select_related('categoria')
    todos_produtos = ordenar_produtos_customizado(todos_produtos_raw)
    
    # Apenas produtos ativos para venda na aba "Novo Pedido"
    produtos_disponiveis_raw = Produto.objects.filter(empresa=empresa, ativo=True).select_related('categoria')
    produtos_disponiveis = ordenar_produtos_customizado(produtos_disponiveis_raw)
    
    # PADRONIZADO: Mesma query da cozinha (pendente, preparando, pronto)
    pedidos_abertos = Pedido.objects.filter(
        empresa=empresa, 
        status__in=['pendente', 'preparando', 'pronto']
    ).order_by('criado_em').prefetch_related('itens__produto')
    
    # Calcular estatísticas iniciais
    total_pendente = pedidos_abertos.filter(status='pendente').count()
    total_preparando = pedidos_abertos.filter(status='preparando').count()
    total_pronto = pedidos_abertos.filter(status='pronto').count()
    
    # Calcular tempo médio dos pedidos entregues hoje
    from datetime import timedelta
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
            tempo_decorrido = (pedido.atualizado_em - pedido.criado_em).total_seconds()
            if tempo_decorrido <= 7200:  # Ignorar > 2h
                tempos.append(tempo_decorrido)
        
        if tempos:
            tempo_medio_segundos = int(sum(tempos) / len(tempos))
    
    context = {
        'categorias': categorias,
        'todos_produtos': todos_produtos,
        'produtos': produtos_disponiveis,
        'pedidos_abertos': pedidos_abertos,
        'aba_ativa': aba,
        'estatisticas': {
            'total_pendente': total_pendente,
            'total_preparando': total_preparando,
            'total_pronto': total_pronto,
            'tempo_medio_segundos': tempo_medio_segundos
        }
    }
    
    response = render(request, 'caixa/dashboard.html', context)
    
    # Desabilitar cache para forçar reload do template
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response


def ordenar_produtos_customizado(produtos_queryset):
    """
    Ordena produtos: Combos primeiro, Bebidas penúltimo, Sobremesas último.
    Dentro de cada grupo, ordena alfabeticamente por nome.
    """
    produtos_combo = []
    produtos_outros = []
    produtos_bebidas = []
    produtos_sobremesas = []
    
    for produto in produtos_queryset:
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
    return produtos_combo + produtos_outros + produtos_bebidas + produtos_sobremesas

@login_required
def criar_pedido(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            empresa = request.user.empresa
            
            # DEBUG: Log dos dados recebidos
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'=== CRIAR PEDIDO DEBUG ===')
            logger.error(f'Itens recebidos: {data.get("itens", [])}')
            
            # Validação 1: Verificar se há itens
            itens = data.get('itens', [])
            if not itens or len(itens) == 0:
                return JsonResponse({
                    'success': False,
                    'error': 'O pedido deve conter pelo menos um item'
                })
            
            # Validação 2: Verificar nome do cliente
            cliente_nome = data.get('cliente_nome', '').strip()
            if not cliente_nome:
                return JsonResponse({
                    'success': False,
                    'error': 'O nome do cliente é obrigatório'
                })
            
            # Validação 3: Verificar forma de pagamento
            forma_pagamento = data.get('forma_pagamento', '').strip()
            if not forma_pagamento:
                return JsonResponse({
                    'success': False,
                    'error': 'A forma de pagamento é obrigatória'
                })
            
            pedido = Pedido.objects.create(
                empresa=empresa,
                tipo=data.get('tipo', 'balcao'),
                cliente_nome=cliente_nome,
                cliente_telefone=data.get('cliente_telefone', ''),
                mesa=data.get('mesa', ''),
                forma_pagamento=forma_pagamento,
                observacoes=data.get('observacoes', ''),
                operador=request.user
            )
            
            total = Decimal('0.00')
            for item in itens:
                try:
                    produto = Produto.objects.get(id=item['produto_id'])
                except Produto.DoesNotExist:
                    pedido.delete()  # Deletar pedido criado
                    return JsonResponse({
                        'success': False,
                        'error': f'Produto com ID {item["produto_id"]} não encontrado. Por favor, atualize a página.'
                    })
                
                item_pedido = ItemPedido.objects.create(
                    pedido=pedido,
                    produto=produto,
                    quantidade=item['quantidade'],
                    preco_unitario=produto.preco,
                    observacoes=item.get('observacoes', '')
                )
                total += item_pedido.subtotal
                
                # Se for combo, processar escolhas e abater estoque
                if item.get('is_combo') and item.get('escolhas'):
                    for escolha in item['escolhas']:
                        try:
                            # Criar registro de escolha
                            slot = ComboSlot.objects.get(id=escolha['slot_id'])
                            produto_escolhido = Produto.objects.get(id=escolha['produto_id'])
                        except (ComboSlot.DoesNotExist, Produto.DoesNotExist):
                            pedido.delete()  # Deletar pedido criado
                            return JsonResponse({
                                'success': False,
                                'error': f'Item do combo não encontrado (Slot ID: {escolha.get("slot_id")}, Produto ID: {escolha.get("produto_id")}). Por favor, atualize a página.'
                            })
                        
                        PedidoComboEscolha.objects.create(
                            item_pedido=item_pedido,
                            slot=slot,
                            produto_escolhido=produto_escolhido,
                            quantidade_abatida=escolha['quantidade_abate']
                        )
                        
                        # Abater estoque do produto escolhido
                        produto_escolhido.quantidade_estoque -= int(escolha['quantidade_abate']) * item['quantidade']
                        produto_escolhido.save()
                else:
                    # Produto normal - abater estoque
                    produto.quantidade_estoque -= item['quantidade']
                    produto.save()
            
            pedido.total = total
            pedido.save()
            
            return JsonResponse({
                'success': True,
                'pedido_id': pedido.id,
                'numero_pedido': pedido.numero_pedido,
                'qr_code': str(pedido.qr_code)
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

@login_required
def buscar_pedido(request, pedido_id):
    try:
        pedido = Pedido.objects.get(id=pedido_id, empresa=request.user.empresa)
        
        data = {
            'success': True,
            'data': {
                'id': pedido.id,
                'numero_pedido': pedido.numero_pedido,
                'cliente_nome': pedido.cliente_nome,
                'tipo': pedido.tipo,
                'forma_pagamento': getattr(pedido, 'forma_pagamento', ''),
                'observacoes': pedido.observacoes,
                'total': str(pedido.total),
                'status': pedido.status,
                'itens': [{
                    'id': item.id,
                    'produto_id': item.produto.id,
                    'produto_nome': item.produto.nome,
                    'quantidade': item.quantidade,
                    'preco_unitario': str(item.preco_unitario),
                    'subtotal': str(item.subtotal),
                    'observacoes': item.observacoes
                } for item in pedido.itens.all()]
            }
        }
        
        return JsonResponse(data)
    except Pedido.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Pedido não encontrado'})

@login_required
def editar_pedido(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pedido_id = data.get('pedido_id')
            
            # Validação 1: Verificar se há itens
            itens = data.get('itens', [])
            if not itens or len(itens) == 0:
                return JsonResponse({
                    'success': False,
                    'error': 'O pedido deve conter pelo menos um item'
                })
            
            # Validação 2: Verificar nome do cliente
            cliente_nome = data.get('cliente_nome', '').strip()
            if not cliente_nome:
                return JsonResponse({
                    'success': False,
                    'error': 'O nome do cliente é obrigatório'
                })
            
            # Validação 3: Verificar forma de pagamento
            forma_pagamento = data.get('forma_pagamento', '').strip()
            if not forma_pagamento:
                return JsonResponse({
                    'success': False,
                    'error': 'A forma de pagamento é obrigatória'
                })
            
            pedido = Pedido.objects.get(id=pedido_id, empresa=request.user.empresa)
            
            # Atualizar dados do pedido
            pedido.cliente_nome = cliente_nome
            pedido.tipo = data.get('tipo', 'balcao')
            pedido.forma_pagamento = forma_pagamento
            pedido.observacoes = data.get('observacoes', '')
            
            # Deletar itens antigos
            pedido.itens.all().delete()
            
            # Adicionar novos itens
            total = Decimal('0.00')
            for item in itens:
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
                'numero_pedido': pedido.numero_pedido
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

@login_required
def listar_produtos(request):
    empresa = request.user.empresa
    categoria_id = request.GET.get('categoria')
    
    produtos = Produto.objects.filter(empresa=empresa, ativo=True)
    if categoria_id:
        produtos = produtos.filter(categoria_id=categoria_id)
    
    data = [{
        'id': p.id,
        'nome': p.nome,
        'descricao': p.descricao,
        'preco': str(p.preco),
        'categoria': p.categoria.nome if p.categoria else ''
    } for p in produtos]
    
    return JsonResponse({'produtos': data})

@login_required
def detalhes_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, empresa=request.user.empresa)
    return render(request, 'caixa/detalhes_pedido.html', {'pedido': pedido})

@login_required
def salvar_configuracoes(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            empresa = request.user.empresa
            
            # Atualizar nome da empresa
            nome_sistema = data.get('nome_sistema', '').strip()
            if nome_sistema:
                empresa.nome = nome_sistema
                empresa.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Configurações salvas com sucesso!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Nome do sistema não pode estar vazio'
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

@login_required
def alterar_status_pedido(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pedido_id = data.get('pedido_id')
            novo_status = data.get('status')
            
            # Validar status
            status_validos = ['pendente', 'preparando', 'pronto', 'entregue', 'cancelado']
            if novo_status not in status_validos:
                return JsonResponse({
                    'success': False,
                    'error': 'Status inválido'
                })
            
            # Buscar e atualizar pedido
            pedido = get_object_or_404(Pedido, id=pedido_id, empresa=request.user.empresa)
            pedido.status = novo_status
            pedido.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Status atualizado com sucesso!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

@login_required
def atualizar_disponibilidade_produto(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            produto_id = data.get('produto_id')
            disponivel = data.get('disponivel', False)
            
            # Buscar e atualizar produto
            produto = get_object_or_404(Produto, id=produto_id, empresa=request.user.empresa)
            produto.ativo = disponivel
            produto.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Disponibilidade atualizada com sucesso!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

@login_required
def buscar_produto(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id, empresa=request.user.empresa)
        
        data = {
            'success': True,
            'produto': {
                'id': produto.id,
                'nome': produto.nome,
                'descricao': produto.descricao,
                'preco': str(produto.preco),
                'quantidade_estoque': produto.quantidade_estoque,
                'categoria': produto.categoria.id if produto.categoria else '',
                'categoria_nome': produto.categoria.nome if produto.categoria else '',
                'tempo_preparo': produto.tempo_preparo,
                'ativo': produto.ativo,
                'imagem': produto.imagem.url if produto.imagem else None
            }
        }
        
        return JsonResponse(data)
    except Produto.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Produto não encontrado'})

@login_required
def criar_produto_item(request):
    if request.method == 'POST':
        try:
            empresa = request.user.empresa
            
            # Validações
            nome = request.POST.get('nome', '').strip()
            preco = request.POST.get('preco', '').strip()
            categoria_nome = request.POST.get('categoria', '').strip()
            
            if not nome:
                return JsonResponse({'success': False, 'error': 'Nome do produto é obrigatório'})
            
            if not preco:
                return JsonResponse({'success': False, 'error': 'Preço do produto é obrigatório'})
            
            if not categoria_nome:
                return JsonResponse({'success': False, 'error': 'Categoria do produto é obrigatória'})
            
            try:
                preco_decimal = Decimal(preco)
                if preco_decimal <= 0:
                    return JsonResponse({'success': False, 'error': 'Preço deve ser maior que zero'})
            except:
                return JsonResponse({'success': False, 'error': 'Preço inválido'})
            
            # Buscar categoria
            try:
                categoria = Categoria.objects.get(empresa=empresa, nome=categoria_nome)
            except Categoria.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Categoria não encontrada'})
            
            # Criar produto
            produto = Produto.objects.create(
                empresa=empresa,
                nome=nome,
                descricao=request.POST.get('descricao', ''),
                preco=preco_decimal,
                quantidade_estoque=int(request.POST.get('quantidade_estoque', 0)),
                categoria=categoria,
                tempo_preparo=int(request.POST.get('tempo_preparo', 15)),
                ativo=request.POST.get('ativo', 'false').lower() == 'true'
            )
            
            # Adicionar imagem se foi enviada
            if 'imagem' in request.FILES:
                produto.imagem = request.FILES['imagem']
                produto.save()
            
            return JsonResponse({
                'success': True,
                'produto_id': produto.id,
                'message': 'Produto criado com sucesso!'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

@login_required
def editar_produto_item(request):
    if request.method == 'POST':
        try:
            produto_id = request.POST.get('produto_id')
            produto = get_object_or_404(Produto, id=produto_id, empresa=request.user.empresa)
            
            # Validações
            nome = request.POST.get('nome', '').strip()
            preco = request.POST.get('preco', '').strip()
            categoria_nome = request.POST.get('categoria', '').strip()
            
            if not nome:
                return JsonResponse({'success': False, 'error': 'Nome do produto é obrigatório'})
            
            if not preco:
                return JsonResponse({'success': False, 'error': 'Preço do produto é obrigatório'})
            
            if not categoria_nome:
                return JsonResponse({'success': False, 'error': 'Categoria do produto é obrigatória'})
            
            try:
                preco_decimal = Decimal(preco)
                if preco_decimal <= 0:
                    return JsonResponse({'success': False, 'error': 'Preço deve ser maior que zero'})
            except:
                return JsonResponse({'success': False, 'error': 'Preço inválido'})
            
            # Atualizar produto
            produto.nome = nome
            produto.descricao = request.POST.get('descricao', '')
            produto.preco = preco_decimal
            produto.quantidade_estoque = int(request.POST.get('quantidade_estoque', 0))
            produto.tempo_preparo = int(request.POST.get('tempo_preparo', 15))
            produto.ativo = request.POST.get('ativo', 'false').lower() == 'true'
            
            # Atualizar categoria
            try:
                categoria = Categoria.objects.get(empresa=request.user.empresa, nome=categoria_nome)
                produto.categoria = categoria
            except Categoria.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Categoria não encontrada'})
            
            # Atualizar imagem se foi enviada
            if 'imagem' in request.FILES:
                produto.imagem = request.FILES['imagem']
            
            produto.save()
            
            return JsonResponse({
                'success': True,
                'produto_id': produto.id,
                'message': 'Produto atualizado com sucesso!'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})



# ========== VIEWS PARA SISTEMA DE COMBOS ==========

from .models import Combo, ComboSlot, ComboSlotItem, PedidoComboEscolha
import json

@login_required
def configurar_combo(request, produto_id=None):
    """
    View para configurar slots e itens de um combo.
    GET: Retorna dados atuais do combo em JSON
    POST: Atualiza configuração do combo
    """
    if request.method == 'GET':
        if not produto_id:
            return JsonResponse({'success': False, 'error': 'ID do produto não fornecido'})
        
        try:
            produto = get_object_or_404(Produto, id=produto_id, empresa=request.user.empresa)
            
            # Verificar se já existe combo para este produto
            try:
                combo = Combo.objects.get(produto=produto)
            except Combo.DoesNotExist:
                # Criar combo se não existir
                combo = Combo.objects.create(produto=produto)
            
            # Montar estrutura de dados
            slots_data = []
            for slot in combo.obter_slots_ordenados():
                itens_data = []
                for item in slot.itens.all():
                    itens_data.append({
                        'id': item.id,
                        'produto_id': item.produto.id,
                        'produto_nome': item.produto.nome,
                        'quantidade_abate': float(item.quantidade_abate),
                        'estoque_disponivel': item.produto.quantidade_estoque
                    })
                
                slots_data.append({
                    'id': slot.id,
                    'nome': slot.nome,
                    'emoji': slot.emoji,
                    'ordem': slot.ordem,
                    'itens': itens_data
                })
            
            return JsonResponse({
                'success': True,
                'combo_id': combo.id,
                'produto_id': produto.id,
                'produto_nome': produto.nome,
                'slots': slots_data
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            produto_id = data.get('produto_id')
            slots_data = data.get('slots', [])
            
            if not produto_id:
                return JsonResponse({'success': False, 'error': 'ID do produto não fornecido'})
            
            produto = get_object_or_404(Produto, id=produto_id, empresa=request.user.empresa)
            
            # Criar ou obter combo
            combo, created = Combo.objects.get_or_create(produto=produto)
            
            # Remover slots existentes
            combo.slots.all().delete()
            
            # Criar novos slots
            for slot_data in slots_data:
                slot = ComboSlot.objects.create(
                    combo=combo,
                    nome=slot_data['nome'],
                    emoji=slot_data.get('emoji', '📋'),
                    ordem=slot_data['ordem']
                )
                
                # Adicionar itens ao slot
                for item_data in slot_data.get('itens', []):
                    ComboSlotItem.objects.create(
                        slot=slot,
                        produto_id=item_data['produto_id'],
                        quantidade_abate=item_data['quantidade_abate']
                    )
            
            return JsonResponse({
                'success': True,
                'message': 'Combo configurado com sucesso!',
                'combo_id': combo.id
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})


@login_required
def obter_opcoes_combo(request, combo_id):
    """
    Retorna opções disponíveis para cada slot do combo.
    Usado para popular o modal de seleção no PDV.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"=== OBTER OPÇÕES DO COMBO {combo_id} ===")
        combo = get_object_or_404(Combo, id=combo_id, produto__empresa=request.user.empresa)
        logger.info(f"Combo encontrado: {combo.produto.nome}")
        
        # Validar integridade do combo
        valido, mensagem = combo.validar_integridade()
        if not valido:
            logger.error(f"Combo inválido: {mensagem}")
            return JsonResponse({'success': False, 'error': mensagem})
        
        slots_data = []
        slots = combo.obter_slots_ordenados()
        logger.info(f"Total de slots: {slots.count()}")
        
        for slot in slots:
            logger.info(f"Processando slot: {slot.nome} (ID: {slot.id})")
            itens_data = []
            
            # MUDANÇA: Buscar TODOS os itens, não apenas os ativos
            itens = slot.itens.all()
            logger.info(f"  Total de itens no slot: {itens.count()}")
            
            for item in itens:
                # Verificar se o produto está ativo
                produto_ativo = item.produto.ativo
                
                # Verificar estoque apenas se o produto estiver ativo
                tem_estoque = item.validar_estoque_disponivel() if produto_ativo else False
                
                logger.info(f"    Item: {item.produto.nome} - Ativo: {produto_ativo} - Estoque: {item.produto.quantidade_estoque} - Tem estoque suficiente: {tem_estoque}")
                
                itens_data.append({
                    'produto_id': item.produto.id,
                    'nome': item.produto.nome,
                    'quantidade_abate': float(item.quantidade_abate),
                    'estoque_disponivel': item.produto.quantidade_estoque,
                    'produto_ativo': produto_ativo,
                    'tem_estoque_suficiente': tem_estoque
                })
            
            if len(itens_data) == 0:
                logger.warning(f"  ⚠️ Slot '{slot.nome}' não tem itens!")
            
            slots_data.append({
                'id': slot.id,
                'nome': slot.nome,
                'emoji': slot.emoji,
                'ordem': slot.ordem,
                'itens': itens_data
            })
        
        logger.info(f"Retornando {len(slots_data)} slots com total de itens")
        
        return JsonResponse({
            'success': True,
            'combo_id': combo.id,
            'nome': combo.produto.nome,
            'preco': float(combo.produto.preco),
            'slots': slots_data
        })
    except Exception as e:
        logger.error(f"Erro ao obter opções do combo: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def adicionar_combo_pedido(request):
    """
    Adiciona um combo ao pedido com as escolhas selecionadas.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            combo_id = data.get('combo_id')
            escolhas = data.get('escolhas', [])
            
            combo = get_object_or_404(Combo, id=combo_id, produto__empresa=request.user.empresa)
            
            # Validar que todos os slots foram preenchidos
            slots_combo = combo.slots.all()
            if len(escolhas) != slots_combo.count():
                return JsonResponse({
                    'success': False,
                    'error': 'Todos os slots devem ser preenchidos'
                })
            
            # Validar estoque disponível
            for escolha in escolhas:
                slot = get_object_or_404(ComboSlot, id=escolha['slot_id'])
                item = get_object_or_404(ComboSlotItem, slot=slot, produto_id=escolha['produto_id'])
                
                if not item.validar_estoque_disponivel():
                    return JsonResponse({
                        'success': False,
                        'error': f'Estoque insuficiente para {item.produto.nome}'
                    })
            
            # Retornar dados para adicionar ao carrinho (o abate de estoque será feito ao finalizar o pedido)
            escolhas_detalhes = []
            for escolha in escolhas:
                try:
                    slot = ComboSlot.objects.get(id=escolha['slot_id'])
                    produto = Produto.objects.get(id=escolha['produto_id'])
                    item = ComboSlotItem.objects.get(slot=slot, produto=produto)
                except (ComboSlot.DoesNotExist, Produto.DoesNotExist, ComboSlotItem.DoesNotExist) as e:
                    return JsonResponse({
                        'success': False,
                        'error': f'Item do combo não encontrado. Por favor, atualize a página.'
                    })
                
                escolhas_detalhes.append({
                    'slot_id': slot.id,
                    'slot_nome': slot.nome,
                    'produto_id': produto.id,
                    'produto_nome': produto.nome,
                    'quantidade_abate': float(item.quantidade_abate)
                })
            
            return JsonResponse({
                'success': True,
                'combo': {
                    'produto_id': combo.produto.id,  # ID do produto, não do combo
                    'combo_id': combo.id,  # ID do combo para referência
                    'nome': combo.produto.nome,
                    'preco': float(combo.produto.preco),
                    'escolhas': escolhas_detalhes
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})


@login_required
def listar_produtos_para_combo(request):
    """
    Retorna lista de TODOS os produtos (ativos e inativos) para vincular a slots de combo.
    Exclui produtos que são combos.
    """
    try:
        # Buscar todos os produtos que NÃO são combos
        produtos = Produto.objects.filter(
            empresa=request.user.empresa
        ).exclude(
            combo__isnull=False  # Exclui produtos que têm um combo associado
        ).values('id', 'nome', 'preco', 'quantidade_estoque', 'ativo').order_by('nome')
        
        return JsonResponse({
            'success': True,
            'produtos': list(produtos)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def listar_categorias(request):
    """
    Retorna lista de categorias da empresa.
    """
    try:
        categorias = Categoria.objects.filter(
            empresa=request.user.empresa,
            ativo=True
        ).values('id', 'nome', 'emoji', 'is_sistema').order_by('nome')
        
        return JsonResponse({
            'success': True,
            'categorias': list(categorias)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def criar_categoria(request):
    """
    Cria uma nova categoria.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nome = data.get('nome', '').strip()
            emoji = data.get('emoji', '📂')
            
            if not nome:
                return JsonResponse({'success': False, 'error': 'Nome é obrigatório'})
            
            # Verificar se já existe categoria com esse nome
            if Categoria.objects.filter(empresa=request.user.empresa, nome=nome).exists():
                return JsonResponse({'success': False, 'error': 'Já existe uma categoria com este nome'})
            
            # Criar nova categoria
            categoria = Categoria.objects.create(
                empresa=request.user.empresa,
                nome=nome,
                emoji=emoji,
                ativo=True
            )
            
            return JsonResponse({
                'success': True,
                'categoria': {
                    'id': categoria.id,
                    'nome': categoria.nome,
                    'emoji': categoria.emoji
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})


@login_required
def excluir_categoria(request, categoria_id):
    """
    Exclui uma categoria permanentemente.
    """
    if request.method == 'DELETE':
        try:
            categoria = get_object_or_404(Categoria, id=categoria_id, empresa=request.user.empresa)
            
            # Proteger categorias do sistema
            if categoria.is_sistema:
                return JsonResponse({
                    'success': False,
                    'error': 'Esta categoria é do sistema e não pode ser excluída.'
                })
            
            # Verificar se há produtos usando esta categoria
            produtos_count = Produto.objects.filter(empresa=request.user.empresa, categoria=categoria).count()
            
            if produtos_count > 0:
                return JsonResponse({
                    'success': False,
                    'error': f'Não é possível excluir. Existem {produtos_count} produto(s) usando esta categoria.'
                })
            
            # Hard delete (exclusão permanente)
            nome_categoria = categoria.nome
            categoria.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Categoria "{nome_categoria}" excluída permanentemente.'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

@login_required
def editar_categoria(request, categoria_id):
    """
    Edita uma categoria existente (nome e/ou emoji).
    """
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            categoria = get_object_or_404(Categoria, id=categoria_id, empresa=request.user.empresa)
            
            # Proteger categorias do sistema
            if categoria.is_sistema:
                return JsonResponse({
                    'success': False,
                    'error': 'Esta categoria é do sistema e não pode ser editada.'
                })
            
            # Atualizar nome se fornecido
            if 'nome' in data:
                novo_nome = data['nome'].strip()
                if not novo_nome:
                    return JsonResponse({'success': False, 'error': 'Nome não pode estar vazio'})
                
                # Verificar se já existe outra categoria com esse nome
                if Categoria.objects.filter(
                    empresa=request.user.empresa, 
                    nome=novo_nome
                ).exclude(id=categoria_id).exists():
                    return JsonResponse({'success': False, 'error': 'Já existe uma categoria com este nome'})
                
                categoria.nome = novo_nome
            
            # Atualizar emoji se fornecido
            if 'emoji' in data:
                categoria.emoji = data['emoji']
            
            categoria.save()
            
            return JsonResponse({
                'success': True,
                'categoria': {
                    'id': categoria.id,
                    'nome': categoria.nome,
                    'emoji': categoria.emoji
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

@login_required
def excluir_pedido(request):
    """
    Exclui um pedido e devolve os itens ao estoque.
    Remove os valores dos relatórios.
    """
    if request.method == 'POST':
        try:
            pedido_id = request.POST.get('pedido_id')
            
            if not pedido_id:
                return JsonResponse({'success': False, 'error': 'ID do pedido não fornecido'})
            
            # Buscar o pedido
            pedido = get_object_or_404(Pedido, id=pedido_id, empresa=request.user.empresa)
            
            # Guardar informações para a mensagem
            numero_pedido = pedido.numero_pedido
            total_itens = 0
            
            # Devolver itens ao estoque
            for item in pedido.itens.all():
                produto = item.produto
                quantidade_devolver = item.quantidade
                
                # Devolver ao estoque
                produto.quantidade_estoque += quantidade_devolver
                produto.save()
                
                total_itens += quantidade_devolver
            
            # Verificar se há escolhas de combo para devolver ao estoque
            escolhas_combo = PedidoComboEscolha.objects.filter(item_pedido__pedido=pedido)
            for escolha in escolhas_combo:
                produto_escolhido = escolha.produto_escolhido
                quantidade_devolver = escolha.quantidade_abatida
                
                # Devolver ao estoque
                produto_escolhido.quantidade_estoque += quantidade_devolver
                produto_escolhido.save()
            
            # Excluir o pedido (cascade vai excluir itens e escolhas automaticamente)
            pedido.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Pedido #{numero_pedido} excluído com sucesso! {total_itens} itens devolvidos ao estoque.'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})


@login_required
def toggle_ativo_produto(request, produto_id):
    """
    Ativa ou inativa um produto.
    """
    if request.method == 'POST':
        try:
            produto = get_object_or_404(Produto, id=produto_id, empresa=request.user.empresa)
            
            # Toggle do status ativo
            produto.ativo = not produto.ativo
            produto.save()
            
            status = 'ativado' if produto.ativo else 'inativado'
            
            return JsonResponse({
                'success': True,
                'message': f'Produto {status} com sucesso!',
                'ativo': produto.ativo
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})


@login_required
def excluir_produto(request, produto_id):
    """
    Exclui um produto permanentemente.
    """
    if request.method == 'POST':
        try:
            produto = get_object_or_404(Produto, id=produto_id, empresa=request.user.empresa)
            
            # Verificar se o produto está sendo usado em pedidos ativos
            itens_ativos = ItemPedido.objects.filter(
                produto=produto,
                pedido__status__in=['pendente', 'preparando', 'pronto']
            ).count()
            
            if itens_ativos > 0:
                return JsonResponse({
                    'success': False,
                    'error': f'Não é possível excluir este produto pois ele está em {itens_ativos} pedido(s) ativo(s).'
                })
            
            # Verificar se o produto está sendo usado em combos
            from caixa.models import ComboSlotItem
            combos_usando = ComboSlotItem.objects.filter(produto=produto).select_related('slot__combo__produto')
            
            if combos_usando.exists():
                nomes_combos = ', '.join([item.slot.combo.produto.nome for item in combos_usando[:3]])
                total_combos = combos_usando.count()
                
                if total_combos > 3:
                    nomes_combos += f' e mais {total_combos - 3}'
                
                return JsonResponse({
                    'success': False,
                    'error': f'Não é possível excluir este produto pois ele está sendo usado nos combos: {nomes_combos}. Remova o produto dos combos primeiro.'
                })
            
            # Verificar se é um combo e tem slots
            if hasattr(produto, 'combo'):
                combo = produto.combo
                
                # Verificar se o combo está em pedidos ativos
                from caixa.models import PedidoComboEscolha
                escolhas_ativas = PedidoComboEscolha.objects.filter(
                    slot__combo=combo,
                    item_pedido__pedido__status__in=['pendente', 'preparando', 'pronto']
                ).count()
                
                if escolhas_ativas > 0:
                    return JsonResponse({
                        'success': False,
                        'error': f'Não é possível excluir este combo pois ele está em {escolhas_ativas} pedido(s) ativo(s).'
                    })
                
                # Deletar escolhas de combos antigos (pedidos finalizados/cancelados)
                PedidoComboEscolha.objects.filter(slot__combo=combo).delete()
                
                # Agora pode excluir o combo (cascade para slots e itens)
                combo.delete()
            
            nome_produto = produto.nome
            produto.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Produto "{nome_produto}" excluído com sucesso!'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})


@login_required
def api_pedidos_ativos(request):
    """
    API para retornar pedidos ativos em tempo real (JSON)
    Usada pelo frame de pedidos ativos no caixa
    """
    from datetime import timedelta
    
    empresa = request.user.empresa
    
    pedidos_ativos = Pedido.objects.filter(
        empresa=empresa,
        status__in=['pendente', 'preparando', 'pronto']
    ).order_by('criado_em').prefetch_related('itens__produto')
    
    # Calcular estatísticas
    total_pendente = pedidos_ativos.filter(status='pendente').count()
    total_preparando = pedidos_ativos.filter(status='preparando').count()
    total_pronto = pedidos_ativos.filter(status='pronto').count()
    
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
            tempo_decorrido = (pedido.atualizado_em - pedido.criado_em).total_seconds()
            if tempo_decorrido <= 7200:  # Ignorar pedidos > 2h
                tempos.append(tempo_decorrido)
        
        if tempos:
            tempo_medio_segundos = sum(tempos) / len(tempos)
    
    pedidos_data = []
    for pedido in pedidos_ativos:
        # Calcular tempo decorrido
        tempo_decorrido = (timezone.now() - pedido.criado_em).total_seconds()
        
        # Buscar itens do pedido
        itens_data = []
        for item in pedido.itens.all():
            itens_data.append({
                'quantidade': item.quantidade,
                'produto_nome': item.produto.nome,
                'preco_unitario': str(item.preco_unitario),
                'subtotal': str(item.subtotal)
            })
        
        # Contar total de itens
        total_itens = sum(item.quantidade for item in pedido.itens.all())
        
        pedidos_data.append({
            'id': pedido.id,
            'numero_pedido': pedido.numero_pedido,
            'cliente_nome': pedido.cliente_nome or 'Cliente',
            'tipo': pedido.tipo,
            'tipo_display': pedido.get_tipo_display(),
            'status': pedido.status,
            'status_display': pedido.get_status_display(),
            'forma_pagamento': pedido.get_forma_pagamento_display() if pedido.forma_pagamento else 'Não informado',
            'total': str(pedido.total),
            'total_itens': total_itens,
            'tempo_decorrido': int(tempo_decorrido),
            'criado_em': pedido.criado_em.isoformat(),
            'itens': itens_data
        })
    
    return JsonResponse({
        'success': True,
        'pedidos': pedidos_data,
        'total': len(pedidos_data),
        'estatisticas': {
            'total_pendente': total_pendente,
            'total_preparando': total_preparando,
            'total_pronto': total_pronto,
            'tempo_medio_segundos': int(tempo_medio_segundos)
        }
    })


@login_required
def relatorios_dados(request):
    """
    API para retornar dados de relatórios (resumo, top itens, histórico)
    """
    from datetime import datetime, timedelta
    from django.db.models import Sum, Count, F
    import logging
    
    logger = logging.getLogger(__name__)
    logger.info(f"=== RELATÓRIOS DADOS CHAMADO ===")
    logger.info(f"User: {request.user.username}")
    logger.info(f"GET params: {request.GET}")
    
    empresa = request.user.empresa
    filtro = request.GET.get('filtro', 'hoje')
    
    logger.info(f"Empresa: {empresa.nome}")
    logger.info(f"Filtro: {filtro}")
    
    # Calcular datas baseado no filtro
    hoje = datetime.now().date()
    
    if filtro == 'hoje':
        data_inicio = hoje
        data_fim = hoje
    elif filtro == 'ontem':
        data_inicio = hoje - timedelta(days=1)
        data_fim = hoje - timedelta(days=1)
    elif filtro == 'semana':
        data_inicio = hoje - timedelta(days=hoje.weekday())
        data_fim = hoje
    elif filtro == 'mes':
        data_inicio = hoje.replace(day=1)
        data_fim = hoje
    elif filtro == 'personalizado':
        data_inicio = datetime.strptime(request.GET.get('data_inicio'), '%Y-%m-%d').date()
        data_fim = datetime.strptime(request.GET.get('data_fim'), '%Y-%m-%d').date()
    else:
        data_inicio = hoje
        data_fim = hoje
    
    logger.info(f"Período: {data_inicio} até {data_fim}")
    
    # Buscar pedidos do período (todos exceto cancelados)
    pedidos = Pedido.objects.filter(
        empresa=empresa,
        criado_em__date__gte=data_inicio,
        criado_em__date__lte=data_fim
    ).exclude(status='cancelado')
    
    logger.info(f"Pedidos encontrados: {pedidos.count()}")
    
    # Calcular resumo
    total_vendas = pedidos.aggregate(total=Sum('total'))['total'] or 0
    total_pedidos = pedidos.count()
    ticket_medio = total_vendas / total_pedidos if total_pedidos > 0 else 0
    total_itens = ItemPedido.objects.filter(pedido__in=pedidos).aggregate(total=Sum('quantidade'))['total'] or 0
    
    resumo = {
        'total_vendas': float(total_vendas),
        'total_pedidos': total_pedidos,
        'ticket_medio': float(ticket_medio),
        'total_itens': int(total_itens)
    }
    
    logger.info(f"Resumo: {resumo}")
    
    # Top itens mais vendidos
    top_itens = ItemPedido.objects.filter(
        pedido__in=pedidos
    ).values(
        'produto__nome'
    ).annotate(
        quantidade=Sum('quantidade'),
        total=Sum(F('quantidade') * F('preco_unitario'))
    ).order_by('-quantidade')[:10]
    
    top_itens_data = [
        {
            'nome': item['produto__nome'],
            'quantidade': item['quantidade'],
            'total': float(item['total'])
        }
        for item in top_itens
    ]
    
    logger.info(f"Top itens: {len(top_itens_data)} itens")
    
    # Histórico de vendas (todos os pedidos do período)
    historico = []
    for pedido in pedidos.order_by('-criado_em'):  # Todos os pedidos do período
        total_itens_pedido = pedido.itens.aggregate(total=Sum('quantidade'))['total'] or 0
        historico.append({
            'numero_pedido': pedido.numero_pedido,
            'criado_em': pedido.criado_em.isoformat(),
            'cliente_nome': pedido.cliente_nome or '',
            'tipo_display': pedido.get_tipo_display(),
            'forma_pagamento_display': pedido.get_forma_pagamento_display() if pedido.forma_pagamento else '',
            'total_itens': total_itens_pedido,
            'total': str(pedido.total)
        })
    
    logger.info(f"Histórico: {len(historico)} pedidos")
    logger.info("=== RETORNANDO DADOS ===")
    
    return JsonResponse({
        'success': True,
        'resumo': resumo,
        'top_itens': top_itens_data,
        'historico': historico
    })
