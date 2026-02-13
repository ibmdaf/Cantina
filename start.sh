#!/bin/bash

echo "🍽️ Iniciando Sistema Cantina..."
echo ""

# Ativar ambiente virtual
source venv/bin/activate

# Verificar se o banco existe
if [ ! -f "db.sqlite3" ]; then
    echo "📦 Criando banco de dados..."
    python manage.py migrate
    echo ""
    echo "📝 Populando com dados de exemplo..."
    python populate_db.py
    echo ""
fi

echo "🚀 Iniciando servidor..."
echo ""
echo "✅ Sistema disponível em: http://localhost:8000"
echo ""
echo "📋 Credenciais:"
echo "   Admin: admin / senha123"
echo "   Caixa: caixa1 / senha123"
echo "   Cozinha: cozinha1 / senha123"
echo "   Gerente: gerente / senha123"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo ""

python manage.py runserver
