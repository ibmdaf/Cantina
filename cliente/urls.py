from django.urls import path
from . import views

urlpatterns = [
    path('<int:empresa_id>/', views.cardapio_cliente, name='cardapio_cliente'),
    path('pedido-ativo/<int:empresa_id>/', views.pedido_ativo_cliente, name='pedido_ativo_cliente'),
]
