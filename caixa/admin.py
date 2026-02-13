from django.contrib import admin
from .models import Categoria, Produto, Pedido, ItemPedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'ativo']
    list_filter = ['empresa', 'ativo']
    search_fields = ['nome']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'preco', 'empresa', 'ativo']
    list_filter = ['categoria', 'empresa', 'ativo']
    search_fields = ['nome', 'descricao']

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['numero_pedido', 'empresa', 'tipo', 'status', 'total', 'criado_em']
    list_filter = ['status', 'tipo', 'empresa', 'criado_em']
    search_fields = ['numero_pedido', 'cliente_nome']
    inlines = [ItemPedidoInline]
    readonly_fields = ['numero_pedido', 'qr_code']


# ========== ADMIN PARA SISTEMA DE COMBOS ==========

from .models import Combo, ComboSlot, ComboSlotItem, PedidoComboEscolha

class ComboSlotItemInline(admin.TabularInline):
    model = ComboSlotItem
    extra = 1
    fields = ['produto', 'quantidade_abate']
    autocomplete_fields = ['produto']

class ComboSlotInline(admin.TabularInline):
    model = ComboSlot
    extra = 1
    fields = ['nome', 'ordem']
    show_change_link = True

@admin.register(Combo)
class ComboAdmin(admin.ModelAdmin):
    list_display = ['produto', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['produto__nome']
    inlines = [ComboSlotInline]
    readonly_fields = ['criado_em', 'atualizado_em']

@admin.register(ComboSlot)
class ComboSlotAdmin(admin.ModelAdmin):
    list_display = ['combo', 'nome', 'ordem']
    list_filter = ['combo']
    search_fields = ['nome', 'combo__produto__nome']
    inlines = [ComboSlotItemInline]
    ordering = ['combo', 'ordem']

@admin.register(ComboSlotItem)
class ComboSlotItemAdmin(admin.ModelAdmin):
    list_display = ['slot', 'produto', 'quantidade_abate']
    list_filter = ['slot__combo']
    search_fields = ['produto__nome', 'slot__nome']
    autocomplete_fields = ['produto']

@admin.register(PedidoComboEscolha)
class PedidoComboEscolhaAdmin(admin.ModelAdmin):
    list_display = ['item_pedido', 'slot', 'produto_escolhido', 'quantidade_abatida', 'criado_em']
    list_filter = ['criado_em']
    search_fields = ['item_pedido__pedido__numero_pedido', 'produto_escolhido__nome']
    readonly_fields = ['criado_em']
