from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Empresa, Usuario

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj', 'telefone', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'cnpj']

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'empresa', 'tipo', 'is_active']
    list_filter = ['tipo', 'empresa', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('empresa', 'tipo', 'telefone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('empresa', 'tipo', 'telefone')}),
    )
