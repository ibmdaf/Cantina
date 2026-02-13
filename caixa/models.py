from django.db import models
from authentication.models import Empresa, Usuario
import uuid

class Categoria(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10, default='📂', blank=True)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    is_sistema = models.BooleanField(default=False, help_text='Categoria do sistema, não pode ser editada ou excluída')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome


class Produto(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    ativo = models.BooleanField(default=True)
    tempo_preparo = models.IntegerField(default=15, help_text='Tempo em minutos')
    quantidade_estoque = models.IntegerField(default=0, help_text='Quantidade em estoque')

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome
    
    def is_combo(self):
        """Verifica se o produto é um combo"""
        try:
            return self.combo is not None
        except:
            return False
    
    def get_combo_id(self):
        """Retorna o ID do combo se existir"""
        try:
            return self.combo.id if self.combo else None
        except:
            return None


class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('preparando', 'Preparando'),
        ('pronto', 'Pronto'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]
    
    TIPO_PEDIDO = [
        ('balcao', 'Balcão'),
        ('mesa', 'Mesa'),
        ('delivery', 'Delivery'),
        ('autoatendimento', 'Autoatendimento'),
    ]
    
    FORMA_PAGAMENTO = [
        ('dinheiro', 'Dinheiro'),
        ('debito', 'Débito'),
        ('credito', 'Crédito'),
        ('pix', 'PIX'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    numero_pedido = models.CharField(max_length=10, unique=True, editable=False)
    qr_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_PEDIDO, default='balcao')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    cliente_nome = models.CharField(max_length=200, blank=True)
    cliente_telefone = models.CharField(max_length=20, blank=True)
    mesa = models.CharField(max_length=10, blank=True)
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO, blank=True)
    observacoes = models.TextField(blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    operador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-criado_em']

    def __str__(self):
        return f"Pedido #{self.numero_pedido}"

    def save(self, *args, **kwargs):
        if not self.numero_pedido:
            ultimo = Pedido.objects.filter(empresa=self.empresa).order_by('-id').first()
            if ultimo and ultimo.numero_pedido:
                numero = int(ultimo.numero_pedido) + 1
            else:
                numero = 1
            self.numero_pedido = str(numero).zfill(4)
        super().save(*args, **kwargs)


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    observacoes = models.TextField(blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"

    def save(self, *args, **kwargs):
        self.subtotal = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)


# ========== MODELOS PARA SISTEMA DE COMBOS ==========

class Combo(models.Model):
    """
    Representa um produto do tipo combo.
    Relaciona-se com Produto através de OneToOne.
    """
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE, related_name='combo')
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Combo'
        verbose_name_plural = 'Combos'
    
    def __str__(self):
        return f"Combo: {self.produto.nome}"
    
    def validar_integridade(self):
        """Valida que o combo tem pelo menos um slot com itens"""
        slots = self.slots.all()
        if not slots.exists():
            return False, "Combo deve ter pelo menos um slot"
        
        for slot in slots:
            if not slot.itens.exists():
                return False, f"Slot '{slot.nome}' não possui itens vinculados"
        
        return True, "Combo válido"
    
    def obter_slots_ordenados(self):
        """Retorna slots ordenados por ordem de exibição"""
        return self.slots.all().order_by('ordem')


class ComboSlot(models.Model):
    """
    Representa um slot de escolha dentro de um combo.
    Ex: "Escolha seu Pastel", "Escolha sua Bebida"
    """
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE, related_name='slots')
    nome = models.CharField(max_length=100, help_text='Ex: Escolha seu Lanche, Escolha sua Bebida')
    emoji = models.CharField(max_length=10, default='📋', help_text='Emoji do slot')
    ordem = models.IntegerField(default=0, help_text='Ordem de exibição do slot')
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Slot do Combo'
        verbose_name_plural = 'Slots do Combo'
        ordering = ['ordem']
        unique_together = [['combo', 'ordem']]
    
    def __str__(self):
        return f"{self.combo.produto.nome} - {self.nome}"
    
    def obter_itens_ativos(self):
        """Retorna apenas itens componentes com produtos ativos"""
        return self.itens.filter(produto__ativo=True)


class ComboSlotItem(models.Model):
    """
    Representa um produto que pode ser escolhido em um slot.
    Define a quantidade que será abatida do estoque.
    Permite adicionar o mesmo produto múltiplas vezes (quantidade_abate sempre 1).
    """
    slot = models.ForeignKey(ComboSlot, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade_abate = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        default=1.0,
        help_text='Quantidade que será abatida do estoque (fixo em 1.0)'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Item do Slot'
        verbose_name_plural = 'Itens do Slot'
        # Removido unique_together para permitir o mesmo produto múltiplas vezes
    
    def __str__(self):
        return f"{self.produto.nome} ({self.quantidade_abate}x)"
    
    def validar_estoque_disponivel(self):
        """Verifica se há estoque suficiente do produto"""
        return self.produto.quantidade_estoque >= float(self.quantidade_abate)

class PedidoComboEscolha(models.Model):
    """
    Registra as escolhas feitas para cada slot de um combo vendido.
    """
    item_pedido = models.ForeignKey(ItemPedido, on_delete=models.CASCADE, related_name='escolhas_combo')
    slot = models.ForeignKey(ComboSlot, on_delete=models.PROTECT)
    produto_escolhido = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade_abatida = models.DecimalField(max_digits=10, decimal_places=3)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Escolha do Combo'
        verbose_name_plural = 'Escolhas do Combo'
        unique_together = [['item_pedido', 'slot']]
    
    def __str__(self):
        return f"{self.slot.nome}: {self.produto_escolhido.nome}"
