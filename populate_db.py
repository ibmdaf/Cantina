import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cantina_system.settings')
django.setup()

from authentication.models import Empresa, Usuario
from caixa.models import Categoria, Produto

def popular_banco():
    print("🍽️ Populando banco de dados...")
    
    # Criar empresa
    empresa, created = Empresa.objects.get_or_create(
        cnpj='12.345.678/0001-90',
        defaults={
            'nome': 'Cantina Delícias',
            'endereco': 'Rua das Flores, 123 - Centro',
            'telefone': '(11) 98765-4321',
            'ativo': True
        }
    )
    print(f"✅ Empresa: {empresa.nome}")
    
    # Criar usuários
    usuarios_data = [
        {'username': 'admin', 'tipo': 'admin', 'email': 'admin@cantina.com'},
        {'username': 'caixa1', 'tipo': 'caixa', 'email': 'caixa@cantina.com'},
        {'username': 'cozinha1', 'tipo': 'cozinha', 'email': 'cozinha@cantina.com'},
        {'username': 'gerente', 'tipo': 'gerente', 'email': 'gerente@cantina.com'},
    ]
    
    for user_data in usuarios_data:
        user, created = Usuario.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'empresa': empresa,
                'tipo': user_data['tipo'],
                'email': user_data['email'],
                'is_staff': True if user_data['tipo'] == 'admin' else False,
                'is_superuser': True if user_data['tipo'] == 'admin' else False,
            }
        )
        if created:
            user.set_password('senha123')
            user.save()
            print(f"✅ Usuário criado: {user.username} (senha: senha123)")
    
    # Criar categorias
    categorias_data = [
        {'nome': 'Lanches', 'descricao': 'Sanduíches e hambúrgueres'},
        {'nome': 'Bebidas', 'descricao': 'Refrigerantes, sucos e água'},
        {'nome': 'Sobremesas', 'descricao': 'Doces e sobremesas'},
        {'nome': 'Pratos Executivos', 'descricao': 'Refeições completas'},
    ]
    
    categorias = {}
    for cat_data in categorias_data:
        cat, created = Categoria.objects.get_or_create(
            empresa=empresa,
            nome=cat_data['nome'],
            defaults={'descricao': cat_data['descricao']}
        )
        categorias[cat_data['nome']] = cat
        print(f"✅ Categoria: {cat.nome}")
    
    # Criar produtos
    produtos_data = [
        # Lanches
        {'nome': 'X-Burger', 'categoria': 'Lanches', 'preco': 15.90, 'descricao': 'Hambúrguer com queijo, alface e tomate'},
        {'nome': 'X-Bacon', 'categoria': 'Lanches', 'preco': 18.90, 'descricao': 'Hambúrguer com bacon, queijo e molho especial'},
        {'nome': 'X-Salada', 'categoria': 'Lanches', 'preco': 16.90, 'descricao': 'Hambúrguer com salada completa'},
        {'nome': 'Hot Dog', 'categoria': 'Lanches', 'preco': 12.90, 'descricao': 'Cachorro-quente tradicional'},
        
        # Bebidas
        {'nome': 'Coca-Cola 350ml', 'categoria': 'Bebidas', 'preco': 5.00, 'descricao': 'Refrigerante lata'},
        {'nome': 'Suco Natural', 'categoria': 'Bebidas', 'preco': 8.00, 'descricao': 'Suco de frutas natural 500ml'},
        {'nome': 'Água Mineral', 'categoria': 'Bebidas', 'preco': 3.00, 'descricao': 'Água mineral 500ml'},
        {'nome': 'Café Expresso', 'categoria': 'Bebidas', 'preco': 4.50, 'descricao': 'Café expresso tradicional'},
        
        # Sobremesas
        {'nome': 'Pudim', 'categoria': 'Sobremesas', 'preco': 8.00, 'descricao': 'Pudim de leite condensado'},
        {'nome': 'Brownie', 'categoria': 'Sobremesas', 'preco': 9.00, 'descricao': 'Brownie de chocolate'},
        {'nome': 'Sorvete', 'categoria': 'Sobremesas', 'preco': 7.00, 'descricao': 'Sorvete 2 bolas'},
        
        # Pratos Executivos
        {'nome': 'Prato Feito', 'categoria': 'Pratos Executivos', 'preco': 25.00, 'descricao': 'Arroz, feijão, carne e salada'},
        {'nome': 'Filé de Frango', 'categoria': 'Pratos Executivos', 'preco': 28.00, 'descricao': 'Filé de frango grelhado com acompanhamentos'},
        {'nome': 'Lasanha', 'categoria': 'Pratos Executivos', 'preco': 30.00, 'descricao': 'Lasanha à bolonhesa'},
    ]
    
    for prod_data in produtos_data:
        prod, created = Produto.objects.get_or_create(
            empresa=empresa,
            nome=prod_data['nome'],
            defaults={
                'categoria': categorias[prod_data['categoria']],
                'preco': prod_data['preco'],
                'descricao': prod_data['descricao'],
                'tempo_preparo': 15
            }
        )
        if created:
            print(f"✅ Produto: {prod.nome} - R$ {prod.preco}")
    
    print("\n✨ Banco de dados populado com sucesso!")
    print("\n📋 Credenciais de acesso:")
    print("   Admin: admin / senha123")
    print("   Caixa: caixa1 / senha123")
    print("   Cozinha: cozinha1 / senha123")
    print("   Gerente: gerente / senha123")

if __name__ == '__main__':
    popular_banco()
