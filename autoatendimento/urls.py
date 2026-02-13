from django.urls import path
from . import views

urlpatterns = [
    path('<int:empresa_id>/', views.autoatendimento_home, name='autoatendimento_home'),
    path('<int:empresa_id>/criar-pedido/', views.criar_pedido_autoatendimento, name='criar_pedido_autoatendimento'),
    path('confirmacao/<int:pedido_id>/', views.confirmacao_pedido, name='confirmacao_pedido'),
]
