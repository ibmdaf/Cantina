# 🎨 Guia de Customização

## Alterando Cores do Sistema

As cores principais estão definidas em `static/css/style.css`:

```css
:root {
    --primary-color: #FF6B35;      /* Laranja principal */
    --secondary-color: #000000;     /* Preto */
    --accent-color: #FFFFFF;        /* Branco */
    --bg-dark: #1a1a1a;            /* Fundo escuro */
    --bg-light: #f5f5f5;           /* Fundo claro */
}
```

### Exemplos de Paletas Alternativas:

**Azul e Branco:**
```css
--primary-color: #2196F3;
--secondary-color: #1565C0;
```

**Verde e Preto:**
```css
--primary-color: #4CAF50;
--secondary-color: #000000;
```

**Roxo e Dourado:**
```css
--primary-color: #9C27B0;
--secondary-color: #FFD700;
```

## Adicionando Logo da Empresa

### 1. No Header (templates/base.html):
```html
<div class="logo">
    <img src="/static/images/logo.png" alt="Logo" style="height: 40px;">
    Cantina System
</div>
```

### 2. Na Tela de Login:
```html
<div class="login-logo">
    <img src="/static/images/logo.png" alt="Logo" style="max-width: 200px;">
</div>
```

## Personalizando Nome do Sistema

Altere em vários arquivos:

1. **templates/base.html** - Título e header
2. **templates/authentication/login.html** - Tela de login
3. **README.md** - Documentação

## Adicionando Novos Campos aos Produtos

Em `caixa/models.py`:

```python
class Produto(models.Model):
    # ... campos existentes ...
    
    # Novos campos
    codigo_barras = models.CharField(max_length=50, blank=True)
    estoque = models.IntegerField(default=0)
    destaque = models.BooleanField(default=False)
    calorias = models.IntegerField(null=True, blank=True)
```

Depois execute:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Adicionando Novos Status de Pedido

Em `caixa/models.py`:

```python
class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('preparando', 'Preparando'),
        ('pronto', 'Pronto'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
        # Adicione novos status aqui
        ('aguardando_pagamento', 'Aguardando Pagamento'),
        ('em_entrega', 'Em Entrega'),
    ]
```

## Configurando Impressora de Comandas

Adicione em `caixa/views.py`:

```python
from escpos.printer import Network

def imprimir_comanda(pedido):
    printer = Network("192.168.1.100")  # IP da impressora
    printer.text(f"Pedido #{pedido.numero_pedido}\n")
    printer.text(f"Mesa: {pedido.mesa}\n")
    printer.text("-" * 32 + "\n")
    
    for item in pedido.itens.all():
        printer.text(f"{item.quantidade}x {item.produto.nome}\n")
        if item.observacoes:
            printer.text(f"  Obs: {item.observacoes}\n")
    
    printer.text("-" * 32 + "\n")
    printer.text(f"Total: R$ {pedido.total}\n")
    printer.cut()
```

## Adicionando Notificações Sonoras

Em `static/js/cozinha.js`:

```javascript
function tocarNotificacao() {
    const audio = new Audio('/static/sounds/notification.mp3');
    audio.play();
}

// Ao receber novo pedido
async function verificarNovosPedidos() {
    const response = await fetch('/cozinha/listar-pedidos/');
    const data = await response.json();
    
    if (data.pedidos.length > pedidosAnteriores) {
        tocarNotificacao();
    }
}
```

## Integrando com WhatsApp

Adicione em `requirements.txt`:
```
twilio
```

Em `caixa/views.py`:
```python
from twilio.rest import Client

def enviar_whatsapp(pedido):
    client = Client('ACCOUNT_SID', 'AUTH_TOKEN')
    
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=f'Seu pedido #{pedido.numero_pedido} está pronto!',
        to=f'whatsapp:+55{pedido.cliente_telefone}'
    )
```

## Adicionando Relatórios

Crie `painel_status/reports.py`:

```python
from django.db.models import Sum, Count
from datetime import datetime, timedelta

def relatorio_vendas_dia():
    hoje = datetime.now().date()
    pedidos = Pedido.objects.filter(
        criado_em__date=hoje,
        status='entregue'
    )
    
    return {
        'total_vendas': pedidos.aggregate(Sum('total'))['total__sum'],
        'total_pedidos': pedidos.count(),
        'ticket_medio': pedidos.aggregate(Sum('total'))['total__sum'] / pedidos.count()
    }
```

## Configurando Email

Em `cantina_system/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'seu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'sua-senha-app'
```

## Adicionando Desconto/Cupom

Em `caixa/models.py`:

```python
class Cupom(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    desconto_percentual = models.DecimalField(max_digits=5, decimal_places=2)
    ativo = models.BooleanField(default=True)
    validade = models.DateField()

class Pedido(models.Model):
    # ... campos existentes ...
    cupom = models.ForeignKey(Cupom, null=True, blank=True, on_delete=models.SET_NULL)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
```

## Backup Automático

Crie `backup.sh`:

```bash
#!/bin/bash
DATA=$(date +%Y%m%d_%H%M%S)
python manage.py dumpdata > backup_$DATA.json
```

Configure no crontab:
```bash
0 2 * * * /caminho/para/backup.sh
```

## Modo Escuro/Claro

Adicione em `static/js/main.js`:

```javascript
function toggleTema() {
    const body = document.body;
    body.classList.toggle('dark-mode');
    localStorage.setItem('tema', body.classList.contains('dark-mode') ? 'dark' : 'light');
}

// Carregar tema salvo
window.addEventListener('load', () => {
    if (localStorage.getItem('tema') === 'dark') {
        document.body.classList.add('dark-mode');
    }
});
```

## Dicas de Performance

1. **Use cache para produtos**:
```python
from django.core.cache import cache

def listar_produtos(request):
    produtos = cache.get('produtos_ativos')
    if not produtos:
        produtos = Produto.objects.filter(ativo=True)
        cache.set('produtos_ativos', produtos, 300)  # 5 minutos
```

2. **Otimize queries**:
```python
# Use select_related e prefetch_related
pedidos = Pedido.objects.select_related('empresa', 'operador').prefetch_related('itens__produto')
```

3. **Comprima arquivos estáticos**:
```bash
pip install django-compressor
```

## Segurança em Produção

Em `settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['seudominio.com']
SECRET_KEY = os.environ.get('SECRET_KEY')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## Suporte

Para mais customizações, consulte:
- Documentação Django: https://docs.djangoproject.com/
- Bootstrap (se quiser adicionar): https://getbootstrap.com/
- Django REST Framework (para APIs): https://www.django-rest-framework.org/
