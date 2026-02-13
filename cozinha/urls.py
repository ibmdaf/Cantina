from django.urls import path
from . import views

urlpatterns = [
    path('', views.cozinha_dashboard, name='cozinha_dashboard'),
    path('atualizar-status/<int:pedido_id>/', views.atualizar_status_pedido, name='atualizar_status_pedido'),
    path('listar-pedidos/', views.listar_pedidos_cozinha, name='listar_pedidos_cozinha'),
    path('api/pedidos/', views.api_pedidos_cozinha, name='api_pedidos_cozinha'),
]
