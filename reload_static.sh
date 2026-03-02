#!/bin/bash

# Script para recarregar arquivos estáticos
echo "🔄 Recarregando arquivos estáticos..."

# Ativar ambiente virtual
source venv/bin/activate

# Coletar arquivos estáticos
echo "📦 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ Arquivos estáticos recarregados!"
echo ""
echo "⚠️  IMPORTANTE: Reinicie o servidor Django para aplicar as mudanças:"
echo "   1. Pare o servidor (Ctrl+C)"
echo "   2. Execute: source venv/bin/activate"
echo "   3. Execute: python manage.py runserver"
echo ""
echo "💡 No navegador, faça um hard refresh:"
echo "   - Mac: Cmd + Shift + R"
echo "   - Windows/Linux: Ctrl + Shift + R"
