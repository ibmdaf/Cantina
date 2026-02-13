# 🗄️ Estrutura do Banco de Dados

## Diagrama de Relacionamentos

```
┌─────────────┐
│   Empresa   │
└──────┬──────┘
       │
       ├──────────┐
       │          │
       ▼          ▼
┌─────────┐  ┌──────────┐
│ Usuario │  │Categoria │
└─────────┘  └────┬─────┘
       │          │
       │          ▼
       │     ┌─────────┐
       │     │ Produto │
       │     └────┬────┘
       │          │
       ▼          ▼
   ┌────────────────┐
   │     Pedido     │
   └────────┬───────┘
            │
            ▼
      ┌──────────┐
      │ItemPedido│
      └──────────┘
```

## Tabelas Principais

### 1. Empresa
Armazena informações das empresas (multi-tenant)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Chave primária |
| nome | String(200) | Nome da empresa |
| cnpj | String(18) | CNPJ único |
| endereco | Text | Endereço completo |
| telefone | String(20) | Telefone de contato |
| ativo | Boolean | Status ativo/inativo |
| criado_em | DateTime | Data de criação |
| atualizado_em | DateTime | Última atualização |

**Relacionamentos:**
- 1:N com Usuario
- 1:N com Categoria
- 1:N com Produto
- 1:N com Pedido

---

### 2. Usuario (extends AbstractUser)
Usuários do sistema com diferentes perfis

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Chave primária |
| username | String(150) | Nome de usuário único |
| email | String(254) | Email |
| password | String(128) | Senha hash |
| empresa_id | ForeignKey | Referência à empresa |
| tipo | String(20) | admin/caixa/cozinha/gerente |
| telefone | String(20) | Telefone |
| is_active | Boolean | Usuário ativo |
| is_staff | Boolean | Acesso ao admin |
| is_superuser | Boolean | Superusuário |

**Relacionamentos:**
- N:1 com Empresa
- 1:N com Pedido (como operador)

---

### 3. Categoria
Categorias de produtos

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Chave primária |
| empresa_id | ForeignKey | Referência à empresa |
| nome | String(100) | Nome da categoria |
| descricao | Text | Descrição |
| ativo | Boolean | Status ativo/inativo |

**Relacionamentos:**
- N:1 com Empresa
- 1:N com Produto

---

### 4. Produto
Produtos/itens do cardápio

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Chave primária |
| empresa_id | ForeignKey | Referência à empresa |
| categoria_id | ForeignKey | Referência à categoria |
| nome | String(200) | Nome do produto |
| descricao | Text | Descrição detalhada |
| preco | Decimal(10,2) | Preço unitário |
| imagem | ImageField | Imagem do produto |
| ativo | Boolean | Status ativo/inativo |
| tempo_preparo | Integer | Tempo em minutos |

**Relacionamentos:**
- N:1 com Empresa
- N:1 com Categoria
- 1:N com ItemPedido

---

### 5. Pedido
Pedidos realizados

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Chave primária |
| empresa_id | ForeignKey | Referência à empresa |
| numero_pedido | String(10) | Número sequencial único |
| qr_code | UUID | UUID único para acompanhamento |
| tipo | String(20) | balcao/mesa/delivery/autoatendimento |
| status | String(20) | pendente/preparando/pronto/entregue/cancelado |
| cliente_nome | String(200) | Nome do cliente |
| cliente_telefone | String(20) | Telefone do cliente |
| mesa | String(10) | Número da mesa |
| observacoes | Text | Observações gerais |
| total | Decimal(10,2) | Valor total |
| operador_id | ForeignKey | Usuário que criou |
| criado_em | DateTime | Data/hora de criação |
| atualizado_em | DateTime | Última atualização |

**Relacionamentos:**
- N:1 com Empresa
- N:1 com Usuario (operador)
- 1:N com ItemPedido

**Índices:**
- numero_pedido (único)
- qr_code (único)
- status
- criado_em

---

### 6. ItemPedido
Itens individuais de cada pedido

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Chave primária |
| pedido_id | ForeignKey | Referência ao pedido |
| produto_id | ForeignKey | Referência ao produto |
| quantidade | Integer | Quantidade |
| preco_unitario | Decimal(10,2) | Preço no momento |
| observacoes | Text | Observações do item |
| subtotal | Decimal(10,2) | Quantidade × Preço |

**Relacionamentos:**
- N:1 com Pedido
- N:1 com Produto

---

## Queries Úteis

### Pedidos do Dia
```python
from django.utils import timezone
hoje = timezone.now().date()
pedidos_hoje = Pedido.objects.filter(criado_em__date=hoje)
```

### Total de Vendas por Período
```python
from django.db.models import Sum
from datetime import datetime, timedelta

inicio = datetime.now() - timedelta(days=7)
total = Pedido.objects.filter(
    criado_em__gte=inicio,
    status='entregue'
).aggregate(Sum('total'))
```

### Produtos Mais Vendidos
```python
from django.db.models import Count, Sum

produtos_top = ItemPedido.objects.values(
    'produto__nome'
).annotate(
    total_vendido=Sum('quantidade')
).order_by('-total_vendido')[:10]
```

### Pedidos por Status
```python
pedidos_por_status = Pedido.objects.values('status').annotate(
    total=Count('id')
)
```

### Tempo Médio de Preparo
```python
from django.db.models import Avg, F, ExpressionWrapper, DurationField

tempo_medio = Pedido.objects.filter(
    status='entregue'
).annotate(
    tempo_preparo=ExpressionWrapper(
        F('atualizado_em') - F('criado_em'),
        output_field=DurationField()
    )
).aggregate(Avg('tempo_preparo'))
```

## Migrações

### Criar Nova Migração
```bash
python manage.py makemigrations
```

### Aplicar Migrações
```bash
python manage.py migrate
```

### Ver SQL de uma Migração
```bash
python manage.py sqlmigrate caixa 0001
```

### Reverter Migração
```bash
python manage.py migrate caixa 0001
```

## Backup e Restore

### Backup (JSON)
```bash
python manage.py dumpdata > backup.json
```

### Backup (SQL)
```bash
sqlite3 db.sqlite3 .dump > backup.sql
```

### Restore (JSON)
```bash
python manage.py loaddata backup.json
```

### Restore (SQL)
```bash
sqlite3 db.sqlite3 < backup.sql
```

## Otimizações

### Índices Recomendados
```python
class Pedido(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['empresa', 'status']),
            models.Index(fields=['criado_em']),
            models.Index(fields=['numero_pedido']),
        ]
```

### Select Related
```python
# Evita N+1 queries
pedidos = Pedido.objects.select_related(
    'empresa', 'operador'
).prefetch_related(
    'itens__produto'
)
```

## Constraints e Validações

### Validação de CNPJ
```python
from django.core.validators import RegexValidator

cnpj_validator = RegexValidator(
    regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
    message='CNPJ inválido'
)
```

### Validação de Preço
```python
from django.core.validators import MinValueValidator

preco = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    validators=[MinValueValidator(0.01)]
)
```

## Triggers e Signals

### Auto-calcular Total do Pedido
```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=ItemPedido)
def atualizar_total_pedido(sender, instance, **kwargs):
    pedido = instance.pedido
    total = sum(item.subtotal for item in pedido.itens.all())
    pedido.total = total
    pedido.save()
```

## Considerações de Segurança

1. **Senhas**: Sempre use `set_password()` para hash
2. **SQL Injection**: Use ORM, evite raw SQL
3. **Permissões**: Valide empresa_id em todas as queries
4. **Soft Delete**: Considere usar `ativo=False` ao invés de deletar

## Migração para PostgreSQL

Para produção, recomenda-se PostgreSQL:

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cantina_db',
        'USER': 'cantina_user',
        'PASSWORD': 'senha_segura',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Instale o driver:
```bash
pip install psycopg2-binary
```
