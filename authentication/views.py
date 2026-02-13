from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        # Redirecionar baseado no tipo de usuário
        if request.user.tipo == 'caixa':
            return redirect('caixa_novo_pedido')
        elif request.user.tipo == 'cozinha':
            return redirect('cozinha_dashboard')
        elif request.user.tipo in ['admin', 'gerente']:
            return redirect('caixa_novo_pedido')
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirecionar baseado no tipo de usuário
            if user.tipo == 'caixa':
                return redirect('caixa_novo_pedido')
            elif user.tipo == 'cozinha':
                return redirect('cozinha_dashboard')
            elif user.tipo in ['admin', 'gerente']:
                return redirect('caixa_novo_pedido')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
    
    return render(request, 'authentication/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user
    context = {
        'user': user,
    }
    
    # Redirecionar baseado no tipo de usuário
    if user.tipo == 'caixa':
        return redirect('caixa_novo_pedido')
    elif user.tipo == 'cozinha':
        return redirect('cozinha_dashboard')
    elif user.tipo in ['admin', 'gerente']:
        return redirect('caixa_novo_pedido')
    
    return render(request, 'dashboard.html', context)


from django.http import JsonResponse
from .models import Usuario
import json

@login_required
def obter_usuario(request, usuario_id):
    """
    API para retornar dados de um usuário
    """
    try:
        usuario = Usuario.objects.get(id=usuario_id, empresa=request.user.empresa)
        
        return JsonResponse({
            'success': True,
            'usuario': {
                'id': usuario.id,
                'username': usuario.username,
                'email': usuario.email,
                'tipo': usuario.tipo,
                'telefone': usuario.telefone,
                'is_active': usuario.is_active
            }
        })
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuário não encontrado'})

@login_required
def editar_usuario(request, usuario_id):
    """
    API para editar um usuário
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            usuario = Usuario.objects.get(id=usuario_id, empresa=request.user.empresa)
            
            # Atualizar campos
            usuario.username = data.get('username', usuario.username)
            usuario.email = data.get('email', usuario.email)
            usuario.tipo = data.get('tipo', usuario.tipo)
            usuario.telefone = data.get('telefone', usuario.telefone)
            usuario.is_active = data.get('is_active', usuario.is_active)
            
            # Atualizar senha se fornecida
            if 'senha' in data and data['senha']:
                usuario.set_password(data['senha'])
            
            usuario.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Usuário atualizado com sucesso'
            })
        except Usuario.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Usuário não encontrado'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})
