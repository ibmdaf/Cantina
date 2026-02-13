# 🧪 Guia de Testes do Sistema

## Checklist de Testes Manuais

### ✅ 1. Autenticação

- [ ] Login com usuário admin funciona
- [ ] Login com usuário caixa funciona
- [ ] Login com usuário cozinha funciona
- [ ] Login com usuário gerente funciona
- [ ] Login com credenciais inválidas mostra erro
- [ ] Logout funciona corretamente
- [ ] Redirecionamento após login está correto

### ✅ 2. Caixa

- [ ] Dashboard do caixa carrega corretamente
- [ ] Lista de produtos aparece
- [ ] Filtro por categoria funciona
- [ ] Adicionar produto ao pedido funciona
- [ ] Alterar quantidade funciona (+/-)
- [ ] Remover item funciona
- [ ] Total é calculado corretamente
- [ ] Criar pedido funciona
- [ ] QR Code é gerado
- [ ] Pedidos recentes aparecem na lista

### ✅ 3. Cozinha

- [ ] Dashboard da cozinha carrega
- [ ] Pedidos pendentes aparecem
- [ ] Pedidos em preparo aparecem
- [ ] Pedidos prontos aparecem
- [ ] Mudar status de pendente para preparando funciona
- [ ] Mudar status de preparando para pronto funciona
- [ ] Mudar status de pronto para entregue funciona
- [ ] Auto-refresh funciona (30s)

### ✅ 4. Acompanhamento (QR Code)

- [ ] Página de acompanhamento carrega com QR Code válido
- [ ] Status do pedido é exibido corretamente
- [ ] Timeline visual funciona
- [ ] Itens do pedido aparecem
- [ ] Total está correto
- [ ] Auto-refresh funciona (15s)
- [ ] QR Code inválido mostra erro 404

### ✅ 5. Painel de Status

- [ ] Dashboard carrega
- [ ] Estatísticas do dia aparecem
- [ ] Total de pedidos está correto
- [ ] Total de vendas está correto
- [ ] Pedidos ativos aparecem na tabela
- [ ] Status badges estão corretos
- [ ] Auto-refresh funciona (10s)

### ✅ 6. Autoatendimento

- [ ] Tela de autoatendimento carrega
- [ ] Produtos aparecem
- [ ] Filtro por categoria funciona
- [ ] Adicionar ao carrinho funciona
- [ ] Carrinho flutuante aparece
- [ ] Modal do carrinho abre
- [ ] Alterar quantidade no carrinho funciona
- [ ] Finalizar pedido funciona
- [ ] Redireciona para acompanhamento
- [ ] QR Code é gerado

### ✅ 7. Cardápio Cliente

- [ ] Cardápio carrega
- [ ] Produtos organizados por categoria
- [ ] Informações da empresa aparecem
- [ ] Layout responsivo funciona

### ✅ 8. Admin Django

- [ ] Acesso ao admin funciona
- [ ] Criar empresa funciona
- [ ] Criar usuário funciona
- [ ] Criar categoria funciona
- [ ] Criar produto funciona
- [ ] Visualizar pedidos funciona
- [ ] Editar dados funciona

## Testes de Responsividade

### Desktop (1920x1080)
- [ ] Layout está correto
- [ ] Todos os elementos visíveis
- [ ] Grid funciona corretamente

### Tablet (768x1024)
- [ ] Layout se adapta
- [ ] Menu responsivo funciona
- [ ] Cards reorganizam

### Mobile (375x667)
- [ ] Layout mobile funciona
- [ ] Botões são clicáveis
- [ ] Texto legível
- [ ] Formulários funcionam

## Testes de Navegadores

- [ ] Chrome/Edge
- [ ] Firefox
- [ ] Safari
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

## Testes de Performance

### Tempo de Carregamento
- [ ] Página inicial < 2s
- [ ] Dashboard caixa < 2s
- [ ] Dashboard cozinha < 2s
- [ ] Autoatendimento < 2s

### Queries
- [ ] Listar produtos < 100ms
- [ ] Criar pedido < 500ms
- [ ] Atualizar status < 200ms

## Testes de Segurança

- [ ] Usuário não autenticado não acessa caixa
- [ ] Usuário não autenticado não acessa cozinha
- [ ] Usuário não autenticado não acessa painel
- [ ] Usuário de uma empresa não vê dados de outra
- [ ] CSRF token está presente em forms
- [ ] Senhas não aparecem em logs
- [ ] SQL injection não funciona

## Testes de Dados

### Criar Pedido Completo
```python
# No shell do Django
python manage.py shell

from authentication.models import Empresa, Usuario
from caixa.models import Produto, Pedido, ItemPedido

empresa = Empresa.objects.first()
produto = Produto.objects.first()
usuario = Usuario.objects.filter(tipo='caixa').first()

pedido = Pedido.objects.create(
    empresa=empresa,
    tipo='balcao',
    cliente_nome='Teste',
    operador=usuario
)

item = ItemPedido.objects.create(
    pedido=pedido,
    produto=produto,
    quantidade=2,
    preco_unitario=produto.preco
)

print(f"Pedido #{pedido.numero_pedido} criado!")
print(f"QR Code: {pedido.qr_code}")
```

### Verificar Integridade
```python
# Verificar se todos os pedidos têm itens
pedidos_sem_itens = Pedido.objects.filter(itens__isnull=True)
print(f"Pedidos sem itens: {pedidos_sem_itens.count()}")

# Verificar se totais estão corretos
for pedido in Pedido.objects.all():
    total_calculado = sum(item.subtotal for item in pedido.itens.all())
    if pedido.total != total_calculado:
        print(f"Pedido #{pedido.numero_pedido} com total incorreto!")
```

## Testes Automatizados (Opcional)

Crie `caixa/tests.py`:

```python
from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import Empresa, Usuario
from caixa.models import Produto, Categoria, Pedido

class CaixaTestCase(TestCase):
    def setUp(self):
        self.empresa = Empresa.objects.create(
            nome='Teste',
            cnpj='12.345.678/0001-90'
        )
        self.usuario = Usuario.objects.create_user(
            username='teste',
            password='senha123',
            empresa=self.empresa,
            tipo='caixa'
        )
        self.client = Client()
        
    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'teste',
            'password': 'senha123'
        })
        self.assertEqual(response.status_code, 302)
        
    def test_criar_pedido(self):
        self.client.login(username='teste', password='senha123')
        categoria = Categoria.objects.create(
            empresa=self.empresa,
            nome='Teste'
        )
        produto = Produto.objects.create(
            empresa=self.empresa,
            categoria=categoria,
            nome='Produto Teste',
            preco=10.00
        )
        
        response = self.client.post(reverse('criar_pedido'), {
            'tipo': 'balcao',
            'itens': [{'produto_id': produto.id, 'quantidade': 1}]
        }, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
```

Executar testes:
```bash
python manage.py test
```

## Testes de Carga (Opcional)

Usando Locust:

```python
# locustfile.py
from locust import HttpUser, task, between

class CantinaUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        self.client.post("/auth/login/", {
            "username": "caixa1",
            "password": "senha123"
        })
    
    @task
    def view_dashboard(self):
        self.client.get("/caixa/")
    
    @task
    def list_products(self):
        self.client.get("/caixa/produtos/")
```

Executar:
```bash
pip install locust
locust -f locustfile.py
```

## Checklist de Deploy

Antes de colocar em produção:

- [ ] DEBUG = False
- [ ] SECRET_KEY em variável de ambiente
- [ ] ALLOWED_HOSTS configurado
- [ ] Banco de dados PostgreSQL
- [ ] Arquivos estáticos coletados
- [ ] HTTPS configurado
- [ ] Backup automático configurado
- [ ] Logs configurados
- [ ] Monitoramento configurado
- [ ] Testes passando
- [ ] Documentação atualizada

## Problemas Comuns

### Pedido não aparece na cozinha
- Verificar se status é 'pendente'
- Verificar se empresa_id está correto
- Verificar auto-refresh

### QR Code não funciona
- Verificar se UUID está correto
- Verificar URL completa
- Verificar se pedido existe

### Total do pedido incorreto
- Verificar cálculo de subtotal
- Verificar save() do ItemPedido
- Recalcular total manualmente

### Imagens não aparecem
- Verificar MEDIA_URL e MEDIA_ROOT
- Verificar permissões da pasta media/
- Verificar se Pillow está instalado

## Logs Úteis

Adicionar em `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

## Monitoramento

Ferramentas recomendadas:
- **Sentry**: Rastreamento de erros
- **New Relic**: Performance
- **Datadog**: Monitoramento completo
- **Prometheus + Grafana**: Métricas customizadas

## Conclusão

Execute todos os testes antes de:
1. Fazer deploy
2. Atualizar versão
3. Adicionar novas funcionalidades
4. Modificar banco de dados

Mantenha este checklist atualizado conforme o sistema evolui!
