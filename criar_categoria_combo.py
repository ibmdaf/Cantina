#!/usr/bin/env python
"""
Script para criar a categoria 'Combo' para todas as empresas que ainda não a possuem.
Execute: python criar_categoria_combo.py
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cantina_system.settings')
django.setup()

from authentication.models import Empresa
from caixa.models import Categoria


def criar_categoria_combo():
    """Cria a categoria 'Combo' para todas as empresas"""
    empresas = Empresa.objects.all()
    criadas = 0
    ja_existentes = 0
    
    for empresa in empresas:
        # Verificar se já existe categoria Combo para esta empresa
        categoria, created = Categoria.objects.get_or_create(
            empresa=empresa,
            nome='Combo',
            defaults={
                'emoji': '🎁',
                'descricao': 'Categoria especial para produtos do tipo combo',
                'ativo': True,
                'is_sistema': True
            }
        )
        
        if created:
            criadas += 1
            print(f"✅ Categoria 'Combo' criada para empresa: {empresa.nome}")
        else:
            ja_existentes += 1
            # Garantir que está marcada como sistema
            if not categoria.is_sistema:
                categoria.is_sistema = True
                categoria.save()
                print(f"🔄 Categoria 'Combo' atualizada para empresa: {empresa.nome}")
            else:
                print(f"ℹ️  Categoria 'Combo' já existe para empresa: {empresa.nome}")
    
    print(f"\n📊 Resumo:")
    print(f"   - Categorias criadas: {criadas}")
    print(f"   - Categorias já existentes: {ja_existentes}")
    print(f"   - Total de empresas: {empresas.count()}")


if __name__ == '__main__':
    print("🚀 Iniciando criação de categorias 'Combo'...\n")
    criar_categoria_combo()
    print("\n✅ Processo concluído!")
