#!/usr/bin/env python3
"""
Script para limpar categorias inativas do banco de dados.
ATENÇÃO: Este script deleta permanentemente as categorias inativas!
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cantina_system.settings')
django.setup()

from caixa.models import Categoria

def limpar_categorias_inativas():
    print("\n" + "="*60)
    print("LIMPEZA DE CATEGORIAS INATIVAS")
    print("="*60 + "\n")
    
    categorias_inativas = Categoria.objects.filter(ativo=False)
    total = categorias_inativas.count()
    
    if total == 0:
        print("✅ Não há categorias inativas para deletar.\n")
        return
    
    print(f"⚠️  Encontradas {total} categoria(s) inativa(s):\n")
    for cat in categorias_inativas:
        print(f"   {cat.emoji} {cat.nome} [ID: {cat.id}] - Empresa: {cat.empresa.nome}")
    
    print("\n" + "-" * 60)
    resposta = input("\n❓ Deseja DELETAR permanentemente estas categorias? (sim/não): ")
    
    if resposta.lower() in ['sim', 's', 'yes', 'y']:
        categorias_inativas.delete()
        print(f"\n✅ {total} categoria(s) deletada(s) com sucesso!\n")
    else:
        print("\n❌ Operação cancelada. Nenhuma categoria foi deletada.\n")
    
    print("="*60 + "\n")

if __name__ == '__main__':
    limpar_categorias_inativas()
