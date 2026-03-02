#!/usr/bin/env python
"""
Script para atualizar o campo first_name dos usuários existentes
Execute: python atualizar_nomes_usuarios.py
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cantina_system.settings')
django.setup()

from authentication.models import Usuario

def atualizar_nomes():
    """Atualizar first_name dos usuários que estão vazios"""
    usuarios = Usuario.objects.filter(first_name='')
    
    print(f"Encontrados {usuarios.count()} usuários sem nome (first_name vazio)")
    print("\nPara cada usuário, digite o nome da pessoa:")
    print("(Pressione Enter para pular)\n")
    
    for usuario in usuarios:
        print(f"\nUsuário: {usuario.username}")
        print(f"Tipo: {usuario.get_tipo_display()}")
        nome = input("Digite o nome da pessoa: ").strip()
        
        if nome:
            usuario.first_name = nome
            usuario.save()
            print(f"✅ Nome '{nome}' salvo para {usuario.username}")
        else:
            print(f"⏭️  Pulado")
    
    print("\n✅ Atualização concluída!")
    
    # Mostrar resumo
    print("\n📋 Resumo dos usuários:")
    for usuario in Usuario.objects.all():
        nome = usuario.first_name or "(sem nome)"
        print(f"  - {usuario.username}: {nome} ({usuario.get_tipo_display()})")

if __name__ == '__main__':
    atualizar_nomes()
