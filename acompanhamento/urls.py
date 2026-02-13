from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:qr_code>/', views.acompanhar_pedido, name='acompanhar_pedido'),
    path('api/<uuid:qr_code>/', views.status_pedido_api, name='status_pedido_api'),
]
