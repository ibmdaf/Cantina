# 🔐 Documentação - Permissões e Controle de Acesso

## Visão Geral

O sistema implementa controle de acesso baseado em tipos de usuário, com permissões granulares para cada funcionalidade.

---

## 👥 Tipos de Usuário e Permissões

### 🔴 Administrador (admin)

**Acesso Completo ao Sistema**

#### Abas Disponíveis
- ✅ Pedido
- ✅ Cardápio
- ✅ Estoque
- ✅ Relatórios
- ✅ Links
- ✅ Usuários
- ✅ Configurações

#### Permissões Especiais
- Criar, editar e excluir usuários
- Alterar configurações do sistema
- Visualizar todos os relatórios
- Gerenciar todas as funcionalidades
- Excluir itens do estoque

---

### 🟡 Gerente (gerente)

**Acesso Gerencial (exceto Configurações)**

#### Abas Disponíveis
- ✅ Pedido
- ✅ Cardápio
- ✅ Estoque
- ✅ Relatórios
- ✅ Links
- ✅ Usuários
- ❌ Configurações

#### Permissões
- Criar, editar e excluir usuários
- Visualizar todos os relatórios
- Gerenciar pedidos e estoque
- Gerenciar cardápio do dia
- **Não pode** alterar configurações do sistema

#### Restrições
- Redirecionado para "Pedido" se tentar acessar Configurações
- Não pode alterar nome do sistema
- Não pode configurar impressoras (futuro)

---

### 🟢 Caixa (caixa)

**Acesso Operacional**

#### Abas Disponíveis
- ✅ Pedido
- ✅ Cardápio
- ✅ Estoque
- ❌ Relatórios
- ✅ Links
- ❌ Usuários
- ❌ Configurações

#### Permissões
- Criar e gerenciar pedidos
- Gerenciar cardápio do dia
- Gerenciar estoque (adicionar, editar produtos)
- Acessar links úteis
- Visualizar pedidos ativos

#### Restrições
- **Não pode** visualizar relatórios
- **Não pode** gerenciar usuários
- **Não pode** acessar configurações
- **Não pode** excluir itens do estoque (apenas admin)
- Redirecionado para "Pedido" se tentar acessar áreas restritas

---

### 🔵 Cozinha (cozinha)

**Acesso Apenas à Cozinha**

#### Tela Disponível
- ✅ Dashboard da Cozinha

#### Permissões
- Visualizar pedidos pendentes
- Visualizar pedidos em preparo
- Visualizar pedidos prontos
- Atualizar status dos pedidos
- Marcar pedidos como entregues

#### Restrições
- **Não pode** acessar tela do caixa
- Redirecionado automaticamente para dashboard da cozinha
- Não tem acesso a nenhuma outra funcionalidade

---

## 🛡️ Implementação de Segurança

### Backend (caixa/views.py)

```python
@login_required
def caixa_dashboard(request, aba='novo-pedido'):
    # Controle de acesso: usuário tipo "cozinha" não pode acessar
    if request.user.tipo == 'cozinha':
        return redirect('cozinha_dashboard')
    
    # Controle de acesso: operador de caixa não pode acessar abas restritas
    if request.user.tipo == 'caixa' and aba in ['configuracoes', 'usuarios', 'relatorios']:
        return redirect('caixa_novo_pedido')
    
    # Controle de acesso: gerente não pode acessar configurações
    if request.user.tipo == 'gerente' and aba == 'configuracoes':
        return redirect('caixa_novo_pedido')
```

### Frontend (templates/base.html)

```django
<!-- Relatórios: apenas admin e gerente -->
{% if user.tipo == "admin" or user.tipo == "gerente" %}
    <a href="{% url 'caixa_relatorios' %}">📊 Relatórios</a>
{% endif %}

<!-- Usuários: admin e gerente -->
{% if user.tipo != 'caixa' %}
    <a href="{% url 'caixa_usuarios' %}">👥 Usuários</a>
{% endif %}

<!-- Configurações: apenas admin -->
{% if user.tipo == 'admin' %}
    <a href="{% url 'caixa_configuracoes' %}">⚙️ Configurações</a>
{% endif %}
```

---

## 📊 Matriz de Permissões

| Funcionalidade | Admin | Gerente | Caixa | Cozinha |
|---|---|---|---|---|
| **Pedidos** |
| Criar pedido | ✅ | ✅ | ✅ | ❌ |
| Editar pedido | ✅ | ✅ | ✅ | ❌ |
| Excluir pedido | ✅ | ✅ | ✅ | ❌ |
| Visualizar pedidos | ✅ | ✅ | ✅ | ✅ |
| Atualizar status | ✅ | ✅ | ✅ | ✅ |
| **Cardápio** |
| Gerenciar cardápio do dia | ✅ | ✅ | ✅ | ❌ |
| Publicar alterações | ✅ | ✅ | ✅ | ❌ |
| **Estoque** |
| Adicionar produto | ✅ | ✅ | ✅ | ❌ |
| Editar produto | ✅ | ✅ | ✅ | ❌ |
| Inativar produto | ✅ | ✅ | ✅ | ❌ |
| Excluir produto | ✅ | ❌ | ❌ | ❌ |
| Gerenciar categorias | ✅ | ✅ | ✅ | ❌ |
| Gerenciar combos | ✅ | ✅ | ✅ | ❌ |
| **Relatórios** |
| Visualizar relatórios | ✅ | ✅ | ❌ | ❌ |
| Exportar dados | ✅ | ✅ | ❌ | ❌ |
| **Usuários** |
| Criar usuário | ✅ | ✅ | ❌ | ❌ |
| Editar usuário | ✅ | ✅ | ❌ | ❌ |
| Inativar usuário | ✅ | ✅ | ❌ | ❌ |
| Excluir usuário | ✅ | ✅ | ❌ | ❌ |
| **Configurações** |
| Alterar nome sistema | ✅ | ❌ | ❌ | ❌ |
| Configurar impressora | ✅ | ❌ | ❌ | ❌ |
| Personalizar tema | ✅ | ❌ | ❌ | ❌ |
| **Links** |
| Acessar links úteis | ✅ | ✅ | ✅ | ❌ |

---

## 🔒 Regras de Segurança

### Autenticação
- ✅ Todas as views requerem login (`@login_required`)
- ✅ Sessões expiram após inatividade
- ✅ Senhas armazenadas com hash (bcrypt)
- ✅ Proteção CSRF em todos os formulários

### Autorização
- ✅ Verificação de tipo de usuário no backend
- ✅ Verificação de tipo de usuário no frontend
- ✅ Redirecionamento automático para áreas permitidas
- ✅ Mensagens de erro para acessos não autorizados

### Proteções Especiais
- ✅ Usuário não pode editar/excluir a si mesmo
- ✅ Usuário não pode inativar a si mesmo
- ✅ Categoria "Combos" não pode ser excluída
- ✅ Validação de empresa (usuário só acessa dados da própria empresa)

---

## 🚨 Validações de Segurança

### No Backend

#### Validação de Empresa
```python
# Usuário só pode acessar dados da própria empresa
produto = get_object_or_404(Produto, id=produto_id, empresa=request.user.empresa)
```

#### Validação de Tipo de Usuário
```python
# Apenas admin pode excluir produtos
if request.user.tipo != 'admin':
    return JsonResponse({'success': False, 'error': 'Apenas administradores podem excluir produtos'})
```

#### Validação de Auto-Modificação
```python
# Não permitir excluir o próprio usuário
if usuario.id == request.user.id:
    return JsonResponse({'success': False, 'error': 'Você não pode excluir seu próprio usuário'})
```

### No Frontend

#### Ocultação de Elementos
```javascript
// Mostrar botão excluir apenas para admin
{% if user.tipo == 'admin' %}
    <button onclick="excluirProduto()">🗑️ Excluir</button>
{% endif %}
```

#### Validação de Ações
```javascript
// Confirmar ações críticas
function excluirProduto(id) {
    if (confirm('Tem certeza? Esta ação é irreversível!')) {
        // Executar exclusão
    }
}
```

---

## 🔄 Fluxo de Autenticação

### 1. Login
```
Usuário → Login Form → authentication/views.py
    ↓
Validação de credenciais
    ↓
Criação de sessão
    ↓
Redirecionamento baseado em tipo:
    - admin/gerente/caixa → caixa_dashboard
    - cozinha → cozinha_dashboard
```

### 2. Acesso a Recursos
```
Request → @login_required
    ↓
Verificação de sessão
    ↓
Verificação de tipo de usuário
    ↓
Verificação de empresa
    ↓
Autorização concedida/negada
```

### 3. Logout
```
Usuário → Botão Sair → logout view
    ↓
Destruição de sessão
    ↓
Redirecionamento para login
```

---

## 🛠️ Customização de Permissões

### Adicionar Novo Tipo de Usuário

1. **Atualizar modelo** (authentication/models.py):
```python
TIPO_CHOICES = [
    ('admin', 'Administrador'),
    ('gerente', 'Gerente'),
    ('caixa', 'Caixa'),
    ('cozinha', 'Cozinha'),
    ('novo_tipo', 'Novo Tipo'),  # Adicionar aqui
]
```

2. **Atualizar controle de acesso** (caixa/views.py):
```python
if request.user.tipo == 'novo_tipo' and aba in ['lista_restrita']:
    return redirect('caixa_novo_pedido')
```

3. **Atualizar frontend** (templates/base.html):
```django
{% if user.tipo == 'novo_tipo' %}
    <!-- Abas específicas -->
{% endif %}
```

4. **Criar migração**:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 📝 Boas Práticas

### Desenvolvimento
1. ✅ Sempre validar permissões no backend
2. ✅ Usar decorators para proteção de views
3. ✅ Validar empresa em todas as queries
4. ✅ Não confiar apenas em validações frontend

### Produção
1. ✅ Revisar logs de acesso regularmente
2. ✅ Monitorar tentativas de acesso não autorizado
3. ✅ Manter senhas fortes
4. ✅ Atualizar dependências de segurança

### Auditoria
1. ✅ Registrar ações críticas (criar, editar, excluir)
2. ✅ Manter histórico de mudanças
3. ✅ Revisar permissões periodicamente
4. ✅ Remover usuários inativos

---

## 🆘 Troubleshooting

### Usuário não consegue acessar funcionalidade
1. Verificar tipo de usuário
2. Verificar se está ativo
3. Verificar empresa associada
4. Verificar logs do servidor

### Redirecionamento inesperado
1. Verificar tipo de usuário
2. Verificar regras de acesso no backend
3. Limpar cache do navegador
4. Verificar sessão

### Erro de permissão
1. Verificar se usuário está logado
2. Verificar tipo de usuário
3. Verificar se tem acesso à empresa
4. Verificar logs de erro
