# 📋 Documentação - Gestão de Usuários

## Visão Geral

O sistema de gestão de usuários permite criar, editar, ativar/inativar e excluir usuários com diferentes níveis de acesso.

## Tipos de Usuários

### 1. Administrador (admin)
- **Acesso completo** a todas as funcionalidades
- Pode gerenciar usuários
- Pode acessar configurações do sistema
- Pode visualizar relatórios
- Pode gerenciar estoque e pedidos

### 2. Gerente (gerente)
- Acesso a todas as funcionalidades **exceto Configurações**
- Pode gerenciar usuários
- Pode visualizar relatórios
- Pode gerenciar estoque e pedidos
- Não pode alterar configurações do sistema

### 3. Caixa (caixa)
- Acesso operacional básico
- Pode criar e gerenciar pedidos
- Pode gerenciar cardápio do dia
- Pode gerenciar estoque
- Pode acessar links úteis
- **Não pode** acessar relatórios, usuários ou configurações

### 4. Cozinha (cozinha)
- Acesso apenas ao dashboard da cozinha
- Visualiza pedidos pendentes, em preparo e prontos
- Pode atualizar status dos pedidos
- Redirecionado automaticamente para tela da cozinha

## Funcionalidades

### Criar Novo Usuário

1. Acesse a aba **Usuários** (disponível para admin e gerente)
2. Clique no botão **+ Novo Usuário**
3. Preencha os campos:
   - **Nome**: Nome completo da pessoa (ex: "João Silva")
   - **Usuário**: Nome de usuário para login (sem espaços, minúsculas - ex: "joaosilva")
   - **Senha**: Senha de acesso (mínimo 4 caracteres)
   - **Confirmar Senha**: Repetir a senha
   - **Tipo de Usuário**: Selecione o nível de acesso
4. Clique em **Criar Usuário**

**Validações:**
- Nome é obrigatório
- Usuário é obrigatório e não pode conter espaços
- Usuário deve ser único no sistema
- Senha deve ter no mínimo 4 caracteres
- As duas senhas devem coincidir

### Editar Usuário

1. Na tabela de usuários, clique no menu **⋮** (três pontos)
2. Selecione **✏️ Editar**
3. Modifique os campos desejados:
   - Nome
   - Usuário
   - Nova Senha (deixe em branco para não alterar)
   - Tipo de Usuário
4. Clique em **Salvar Alterações**

**Observações:**
- O campo senha é opcional ao editar
- Se não preencher a senha, ela permanece inalterada
- Não é possível editar o próprio usuário logado

### Ativar/Inativar Usuário

1. Na tabela de usuários, clique no menu **⋮**
2. Selecione **🚫 Inativar** ou **✅ Ativar**
3. Confirme a ação no modal

**Regras:**
- Usuários inativos não podem fazer login
- Não é possível inativar o próprio usuário logado
- Status é exibido na coluna "Status" (Ativo/Inativo)

### Excluir Usuário

1. Na tabela de usuários, clique no menu **⋮**
2. Selecione **🗑️ Excluir**
3. Confirme a exclusão no modal

**Atenção:**
- Esta ação é **irreversível**
- Não é possível excluir o próprio usuário logado
- Todos os dados do usuário serão removidos

## Tabela de Usuários

A tabela exibe:
- **Nome**: Nome completo da pessoa
- **Usuário**: Nome de usuário para login
- **Tipo**: Badge colorido com o tipo de usuário
- **Status**: Ativo ou Inativo
- **Ações**: Menu com opções de editar, ativar/inativar e excluir

### Recursos da Tabela
- Cabeçalho fixo que não rola
- Barra de rolagem vertical para muitos usuários
- Larguras de colunas otimizadas
- Menu dropdown para ações

## Controle de Acesso

### Backend (caixa/views.py)
```python
# Operador de caixa não pode acessar usuários
if request.user.tipo == 'caixa' and aba in ['configuracoes', 'usuarios', 'relatorios']:
    return redirect('caixa_novo_pedido')

# Gerente não pode acessar configurações
if request.user.tipo == 'gerente' and aba == 'configuracoes':
    return redirect('caixa_novo_pedido')
```

### Frontend (templates/base.html)
```django
{% if user.tipo != 'caixa' %}
    <!-- Aba Usuários visível para admin e gerente -->
{% endif %}

{% if user.tipo == 'admin' %}
    <!-- Aba Configurações visível apenas para admin -->
{% endif %}
```

## API Endpoints

### Criar Usuário
- **URL**: `/caixa/usuarios/criar/`
- **Método**: POST
- **Payload**:
```json
{
  "nome": "João Silva",
  "username": "joaosilva",
  "password": "senha123",
  "tipo": "caixa"
}
```

### Buscar Usuário
- **URL**: `/caixa/usuarios/<id>/`
- **Método**: GET
- **Resposta**:
```json
{
  "success": true,
  "usuario": {
    "id": 1,
    "nome": "João Silva",
    "username": "joaosilva",
    "tipo": "caixa",
    "is_active": true
  }
}
```

### Editar Usuário
- **URL**: `/caixa/usuarios/<id>/editar/`
- **Método**: POST
- **Payload**:
```json
{
  "nome": "João Silva",
  "username": "joaosilva",
  "password": "novasenha123",  // opcional
  "tipo": "gerente"
}
```

### Ativar/Inativar Usuário
- **URL**: `/caixa/usuarios/<id>/toggle-ativo/`
- **Método**: POST

### Excluir Usuário
- **URL**: `/caixa/usuarios/<id>/excluir/`
- **Método**: DELETE

## Modelo de Dados

### Usuario (authentication/models.py)
```python
class Usuario(AbstractUser):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='usuarios')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='caixa')
    first_name = models.CharField(max_length=150)  # Nome da pessoa
    username = models.CharField(max_length=150, unique=True)  # Login
```

**Campos:**
- `first_name`: Nome completo da pessoa
- `username`: Nome de usuário para login (único)
- `tipo`: Tipo de usuário (admin, gerente, caixa, cozinha)
- `is_active`: Status ativo/inativo
- `empresa`: Empresa à qual o usuário pertence

## Script de Atualização

Para atualizar nomes de usuários existentes:

```bash
source venv/bin/activate
python atualizar_nomes_usuarios.py
```

O script permite preencher o campo `first_name` de usuários que estão com este campo vazio.

## Boas Práticas

1. **Nomes de Usuário**: Use padrão consistente (ex: primeironome.sobrenome)
2. **Senhas**: Oriente usuários a usar senhas fortes
3. **Tipos de Acesso**: Conceda apenas o acesso necessário
4. **Inativação**: Prefira inativar ao invés de excluir usuários
5. **Auditoria**: Mantenha registro de quem criou/modificou usuários

## Troubleshooting

### Usuário não consegue fazer login
- Verifique se o usuário está ativo
- Confirme se a senha está correta
- Verifique se o username está correto (sem espaços, minúsculas)

### Nome não aparece no cabeçalho
- Verifique se o campo `first_name` está preenchido
- Use o script `atualizar_nomes_usuarios.py` para preencher
- Ou edite o usuário manualmente pela aba Usuários

### Erro ao criar usuário
- Verifique se o username já existe
- Confirme que todos os campos obrigatórios estão preenchidos
- Verifique se as senhas coincidem
- Certifique-se que o username não tem espaços

## Segurança

- Senhas são armazenadas com hash (não em texto plano)
- Validação de permissões no backend e frontend
- Proteção CSRF em todas as requisições
- Não é possível modificar/excluir o próprio usuário
- Controle de acesso por tipo de usuário
