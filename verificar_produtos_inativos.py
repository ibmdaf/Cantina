#!/usr/bin/env python3
"""
Script para verificar produtos inativos no banco de dados.
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cantina_system.settings')
django.setup()

from caixa.models import Produto
from authentication.models import Empresa

def verificar_produtos():
    print("\n" + "="*60)
    print("VERIFICAÇÃO DE PRODUTOS NO BANCO DE DADOS")
    print("="*60 + "\n")
    
    empresas = Empresa.objects.all()
    
    for empresa in empresas:
        print(f"\n📊 EMPRESA: {empresa.nome}")
        print("-" * 60)
        
        produtos_ativos = Produto.objects.filter(empresa=empresa, ativo=True)
        produtos_inativos = Produto.objects.filter(empresa=empresa, ativo=False)
        
        print(f"\n✅ PRODUTOS ATIVOS ({produtos_ativos.count()}):")
        if produtos_ativos.exists():
            for prod in produtos_ativos[:10]:  # Mostrar apenas os 10 primeiros
                combo = " (COMBO)" if prod.is_combo() else ""
                print(f"   {prod.nome}{combo} - R$ {prod.preco} [ID: {prod.id}]")
            if produtos_ativos.count() > 10:
                print(f"   ... e mais {produtos_ativos.count() - 10} produtos")
        else:
            print("   Nenhum produto ativo")
        
        print(f"\n❌ PRODUTOS INATIVOS ({produtos_inativos.count()}):")
        if produtos_inativos.exists():
            for prod in produtos_inativos:
                combo = " (COMBO)" if prod.is_combo() else ""
                categoria = prod.categoria.nome if prod.categoria else "Sem categoria"
                print(f"   {prod.nome}{combo} - {categoria} - R$ {prod.preco} [ID: {prod.id}]")
        else:
            print("   Nenhum produto inativo")
        
        print("\n" + "-" * 60)
    
    print("\n" + "="*60)
    print("VERIFICAÇÃO CONCLUÍDA")
    print("="*60 + "\n")

if __name__ == '__main__':
    verificar_produtos()
