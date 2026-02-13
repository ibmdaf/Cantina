# 🚀 Início Rápido - Sistema Cantina

## ⚡ Começar em 3 Passos

### 1️⃣ Ativar Ambiente e Iniciar
```bash
./start.sh
```

### 2️⃣ Acessar o Sistema
Abra seu navegador em: **http://localhost:8000**

### 3️⃣ Fazer Login
Use uma das credenciais:
- **Caixa**: `caixa1` / `senha123`
- **Cozinha**: `cozinha1` / `senha123`
- **Gerente**: `gerente` / `senha123`
- **Admin**: `admin` / `senha123`

---

## 🎯 Fluxo Básico de Uso

### Cenário 1: Pedido no Balcão

1. **Operador de Caixa** faz login
2. Acessa automaticamente a tela do caixa
3. Seleciona produtos clicando neles
4. Ajusta quantidades se necessário
5. Preenche nome do cliente (opcional)
6. Clica em "Finalizar Pedido"
7. Sistema gera QR Code para o cliente

### Cenário 2: Preparação na Cozinha

1. **Cozinha** faz login
2. Vê pedidos pendentes na coluna da esquerda
3. Clica em "Iniciar Preparo"
4. Pedido move para coluna "Preparando"
5. Quando pronto, clica em "Marcar como Pronto"
6. Pedido move para coluna "Prontos"

### Cenário 3: Cliente Acompanha

1. Cliente recebe QR Code ou link
2. Acessa: `http://localhost:8000/acompanhamento/{QR_CODE}/`
3. Vê status em tempo real:
   - 📝 Pedido Recebido
   - 👨‍🍳 Em Preparo
   - ✅ Pronto
   - 🎉 Entregue

### Cenário 4: Autoatendimento

1. Cliente acessa: `http://localhost:8000/autoatendimento/1/`
2. Navega pelo cardápio
3. Adiciona produtos ao carrinho
4. Clica no carrinho flutuante
5. Preenche nome e mesa
6. Finaliza pedido
7. Recebe QR Code para acompanhamento

---

## 📱 URLs Principais

| Tela | URL | Acesso |
|------|-----|--------|
| Login | `/auth/login/` | Público |
| Caixa | `/caixa/` | Autenticado |
| Cozinha | `/cozinha/` | Autenticado |
| Painel | `/painel/` | Autenticado |
| Autoatendimento | `/autoatendimento/1/` | Público |
| Cardápio | `/cardapio/1/` | Público |
| Acompanhamento | `/acompanhamento/{QR}/` | Público |
| Admin | `/admin/` | Superusuário |

---

## 🎨 Personalização Rápida

### Mudar Nome da Empresa
Edite `populate_db.py` linha 17:
```python
'nome': 'Seu Nome Aqui',
```

### Mudar Cores
Edite `static/css/style.css` linhas 1-7:
```css
--primary-color: #FF6B35;  /* Sua cor principal */
--secondary-color: #000000; /* Sua cor secundária */
```

### Adicionar Produtos
1. Acesse `/admin/`
2. Login com `admin` / `senha123`
3. Vá em "Produtos" → "Adicionar produto"
4. Preencha os campos e salve

---

## 🔧 Comandos Úteis

### Criar Superusuário
```bash
python manage.py createsuperuser
```

### Resetar Banco de Dados
```bash
rm db.sqlite3
python manage.py migrate
python populate_db.py
```

### Ver Logs em Tempo Real
```bash
python manage.py runserver --verbosity 2
```

### Coletar Arquivos Estáticos (Produção)
```bash
python manage.py collectstatic
```

---

## 🐛 Problemas Comuns

### Erro: "Port already in use"
```bash
# Matar processo na porta 8000
lsof -ti:8000 | xargs kill -9
```

### Erro: "No module named 'PIL'"
```bash
pip install Pillow
```

### Erro: "CSRF token missing"
- Limpe cookies do navegador
- Faça logout e login novamente

### Produtos não aparecem
```bash
python populate_db.py
```

---

## 📊 Testando o Sistema

### Teste Completo em 5 Minutos

1. **Login como Caixa** (`caixa1` / `senha123`)
   - Crie um pedido com 2-3 produtos
   - Anote o número do pedido

2. **Abra nova aba anônima**
   - Acesse o QR Code do pedido
   - Veja o status "Pendente"

3. **Login como Cozinha** (nova aba)
   - Veja o pedido na coluna "Pendentes"
   - Mova para "Preparando"
   - Depois para "Pronto"

4. **Volte para aba do QR Code**
   - Veja o status atualizado automaticamente

5. **Login como Gerente** (nova aba)
   - Veja estatísticas do dia
   - Veja todos os pedidos ativos

---

## 🎓 Próximos Passos

Depois de testar o básico:

1. **Leia a documentação completa**: `README.md`
2. **Entenda a estrutura**: `ESTRUTURA_BD.md`
3. **Personalize o sistema**: `CUSTOMIZACAO.md`
4. **Configure URLs**: `GUIA_URLS.md`
5. **Execute testes**: `TESTES.md`

---

## 💡 Dicas

- **Auto-refresh**: Cozinha e Painel atualizam sozinhos
- **Multi-empresa**: Cada empresa tem seus próprios dados
- **QR Code único**: Cada pedido tem um UUID único
- **Responsivo**: Funciona em desktop, tablet e mobile
- **Sem dependências externas**: Tudo funciona offline

---

## 🆘 Precisa de Ajuda?

1. Verifique os logs no terminal
2. Abra o console do navegador (F12)
3. Consulte a documentação completa
4. Verifique se todos os serviços estão rodando

---

## ✅ Checklist de Verificação

Antes de usar em produção:

- [ ] Testei todos os fluxos
- [ ] Personalizei nome e cores
- [ ] Adicionei produtos reais
- [ ] Configurei backup
- [ ] Li documentação de segurança
- [ ] Testei em diferentes dispositivos
- [ ] Configurei banco de dados de produção

---

## 🎉 Pronto!

Seu sistema está funcionando! Agora é só personalizar e usar.

**Bom trabalho! 🍽️**
