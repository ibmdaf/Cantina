from django.urls import path
from . import views

urlpatterns = [
    path('', views.caixa_dashboard, name='caixa_dashboard'),
    path('novo-pedido/', views.caixa_dashboard, {'aba': 'novo-pedido'}, name='caixa_novo_pedido'),
    path('cardapio-dia/', views.caixa_dashboard, {'aba': 'cardapio'}, name='caixa_cardapio_dia'),
    path('estoque/', views.caixa_dashboard, {'aba': 'estoque'}, name='caixa_estoque'),
    path('relatorios/', views.caixa_dashboard, {'aba': 'relatorios'}, name='caixa_relatorios'),
    path('links/', views.caixa_dashboard, {'aba': 'links'}, name='caixa_links'),
    path('usuarios/', views.caixa_dashboard, {'aba': 'usuarios'}, name='caixa_usuarios'),
    path('configuracoes/', views.caixa_dashboard, {'aba': 'configuracoes'}, name='caixa_configuracoes'),
    path('criar-pedido/', views.criar_pedido, name='criar_pedido'),
    path('editar-pedido/', views.editar_pedido, name='editar_pedido'),
    path('pedido/<int:pedido_id>/', views.buscar_pedido, name='buscar_pedido'),
    path('produtos/', views.listar_produtos, name='listar_produtos'),
    path('salvar-configuracoes/', views.salvar_configuracoes, name='salvar_configuracoes'),
    path('alterar-status-pedido/', views.alterar_status_pedido, name='alterar_status_pedido'),
    path('atualizar-disponibilidade/', views.atualizar_disponibilidade_produto, name='atualizar_disponibilidade_produto'),
    path('produto/<int:produto_id>/', views.buscar_produto, name='buscar_produto'),
    path('criar-produto-item/', views.criar_produto_item, name='criar_produto_item'),
    path('editar-produto-item/', views.editar_produto_item, name='editar_produto_item'),
    
    # URLs para sistema de combos
    path('combo/configurar/', views.configurar_combo, name='configurar_combo'),
    path('combo/configurar/<int:produto_id>/', views.configurar_combo, name='configurar_combo_produto'),
    path('combo/<int:combo_id>/opcoes/', views.obter_opcoes_combo, name='obter_opcoes_combo'),
    path('combo/adicionar-pedido/', views.adicionar_combo_pedido, name='adicionar_combo_pedido'),
    path('combo/produtos/', views.listar_produtos_para_combo, name='listar_produtos_para_combo'),
    
    # URLs para gerenciamento de categorias
    path('categorias/listar/', views.listar_categorias, name='listar_categorias'),
    path('categorias/criar/', views.criar_categoria, name='criar_categoria'),
    path('categorias/<int:categoria_id>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:categoria_id>/excluir/', views.excluir_categoria, name='excluir_categoria'),
    
    # URL para excluir pedido
    path('excluir-pedido/', views.excluir_pedido, name='excluir_pedido'),
    
    # URLs para gerenciar produtos
    path('produto/<int:produto_id>/toggle-ativo/', views.toggle_ativo_produto, name='toggle_ativo_produto'),
    path('produto/<int:produto_id>/excluir/', views.excluir_produto, name='excluir_produto'),
    
    # URL para API de pedidos ativos
    path('api/pedidos-ativos/', views.api_pedidos_ativos, name='api_pedidos_ativos'),
    
    # URL para dados de relatórios
    path('relatorios/dados/', views.relatorios_dados, name='relatorios_dados'),
]
