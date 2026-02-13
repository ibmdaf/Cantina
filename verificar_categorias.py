#!/usr/bin/env python3
"""
Script para verificar todas as categorias no banco de dados.
Mostra categorias ativas e inativas.
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cantina_system.settings')
django.setup()

from caixa.models import Categoria
from authentication.models import Empresa

def verificar_categorias():
    print("\n" + "="*60)
    print("VERIFICAÇÃO DE CATEGORIAS NO BANCO DE DADOS")
    print("="*60 + "\n")
    
    empresas = Empresa.objects.all()
    
    for empresa in empresas:
        print(f"\n📊 EMPRESA: {empresa.nome}")
        print("-" * 60)
        
        categorias_ativas = Categoria.objects.filter(empresa=empresa, ativo=True)
        categorias_inativas = Categoria.objects.filter(empresa=empresa, ativo=False)
        
        print(f"\n✅ CATEGORIAS ATIVAS ({categorias_ativas.count()}):")
        if categorias_ativas.exists():
            for cat in categorias_ativas:
                sistema = " (SISTEMA)" if cat.is_sistema else ""
                print(f"   {cat.emoji} {cat.nome}{sistema} [ID: {cat.id}]")
        else:
            print("   Nenhuma categoria ativa")
        
        print(f"\n❌ CATEGORIAS INATIVAS ({categorias_inativas.count()}):")
        if categorias_inativas.exists():
            for cat in categorias_inativas:
                sistema = " (SISTEMA)" if cat.is_sistema else ""
                print(f"   {cat.emoji} {cat.nome}{sistema} [ID: {cat.id}]")
        else:
            print("   Nenhuma categoria inativa")
        
        print("\n" + "-" * 60)
    
    print("\n" + "="*60)
    print("VERIFICAÇÃO CONCLUÍDA")
    print("="*60 + "\n")

if __name__ == '__main__':
    verificar_categorias()
