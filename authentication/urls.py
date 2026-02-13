from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('usuario/<int:usuario_id>/', views.obter_usuario, name='obter_usuario'),
    path('usuario/<int:usuario_id>/editar/', views.editar_usuario, name='editar_usuario'),
]
