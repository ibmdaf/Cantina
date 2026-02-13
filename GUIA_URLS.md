# 📍 Guia de URLs do Sistema

## 🔐 Autenticação

| URL | Descrição | Acesso |
|-----|-----------|--------|
| `/auth/login/` | Tela de login | Público |
| `/auth/logout/` | Logout do sistema | Autenticado |
| `/auth/dashboard/` | Dashboard (redireciona conforme tipo de usuário) | Autenticado |

## 💰 Caixa (Operador)

| URL | Descrição | Acesso |
|-----|-----------|--------|
| `/caixa/` | Dashboard do caixa | Autenticado (Caixa) |
| `/caixa/criar-pedido/` | API para criar pedido | Autenticado (POST) |
| `/caixa/produtos/` | API listar produtos | Autenticado |
| `/caixa/pedido/{id}/` | Detalhes do pedido | Autenticado |

## 👨‍🍳 Cozinha

| URL | Descrição | Acesso |
|-----|-----------|--------|
| `/cozinha/` | Dashboard da cozinha | Autenticado (Cozinha) |
| `/cozinha/atualizar-status/{id}/` | Atualizar status do pedido | Autenticado (POST) |
| `/cozinha/listar-pedidos/` | API listar pedidos | Autenticado |

## 📱 Acompanhamento (Cliente via QR Code)

| URL | Descrição | Acesso |
|-----|-----------|--------|
| `/acompanhamento/{qr_code}/` | Acompanhar pedido | Público |
| `/acompanhamento/api/{qr_code}/` | API status do pedido | Público |

**Exemplo de QR Code**: Cada pedido gera um UUID único
```
http://localhost:8000/acompanhamento/550e8400-e29b-41d4-a716-446655440000/
```

## 📊 Painel de Status

| URL | Descrição | Acesso |
|-----|-----------|--------|
| `/painel/` | Painel de status geral | Autenticado (Gerente/Admin) |
| `/painel/api/` | API dados do painel | Autenticado |

## 🖥️ Autoatendimento (Totem)

| URL | Descrição | Acesso |
|-----|-----------|--------|
| `/autoatendimento/{empresa_id}/` | Tela de autoatendimento | Público |
| `/autoatendimento/{empresa_id}/criar-pedido/` | API criar pedido | Público (POST) |
| `/autoatendimento/confirmacao/{pedido_id}/` | Confirmação do pedido | Público |

**Exemplo**: 
```
http://localhost:8000/autoatendimento/1/
```

## 📖 Cardápio (Cliente)

| URL | Descrição | Acesso |
|-----|-----------|--------|
| `/cardapio/{empresa_id}/` | Visualizar cardápio | Público |

**Exemplo**: 
```
http://localhost:8000/cardapio/1/
```

## ⚙️ Admin Django

| URL | Descrição | Acesso |
|-----|-----------|--------|
| `/admin/` | Painel administrativo | Superusuário |

## 🎯 Fluxo de Uso Típico

### Para Operador de Caixa:
1. Login em `/auth/login/` com usuário `caixa1`
2. Acessa automaticamente `/caixa/`
3. Seleciona produtos e cria pedido
4. Sistema gera QR Code para o cliente

### Para Cozinha:
1. Login em `/auth/login/` com usuário `cozinha1`
2. Acessa automaticamente `/cozinha/`
3. Visualiza pedidos pendentes
4. Atualiza status: Pendente → Preparando → Pronto → Entregue

### Para Cliente (Autoatendimento):
1. Acessa `/autoatendimento/1/` (sem login)
2. Seleciona produtos
3. Finaliza pedido
4. Recebe QR Code para acompanhamento
5. Acessa `/acompanhamento/{qr_code}/` para ver status

### Para Gerente:
1. Login em `/auth/login/` com usuário `gerente`
2. Acessa automaticamente `/painel/`
3. Visualiza estatísticas e todos os pedidos ativos

## 🔄 APIs JSON

Todas as APIs retornam JSON e requerem autenticação (exceto acompanhamento e autoatendimento):

### Criar Pedido (Caixa)
```javascript
POST /caixa/criar-pedido/
{
  "tipo": "balcao",
  "cliente_nome": "João Silva",
  "mesa": "5",
  "itens": [
    {
      "produto_id": 1,
      "quantidade": 2,
      "observacoes": "Sem cebola"
    }
  ]
}
```

### Atualizar Status (Cozinha)
```javascript
POST /cozinha/atualizar-status/1/
{
  "status": "preparando"
}
```

### Status do Pedido (Acompanhamento)
```javascript
GET /acompanhamento/api/{qr_code}/
```

## 📝 Notas Importantes

1. **IDs de Empresa**: Por padrão, a empresa criada tem ID 1
2. **QR Codes**: São UUIDs gerados automaticamente ao criar pedido
3. **Auto-refresh**: Cozinha e Painel atualizam automaticamente
4. **CSRF Token**: Necessário para todas as requisições POST autenticadas
5. **Media Files**: Imagens de produtos ficam em `/media/produtos/`

## 🎨 Personalizações

Para adicionar uma nova empresa:
1. Acesse `/admin/`
2. Crie nova empresa em "Empresas"
3. URLs de autoatendimento e cardápio usarão o novo ID
4. Exemplo: `/autoatendimento/2/` para empresa ID 2
