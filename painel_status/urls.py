from django.urls import path
from . import views

urlpatterns = [
    path('', views.painel_status, name='painel_status'),
    path('api/', views.painel_status_api, name='painel_status_api'),
]
