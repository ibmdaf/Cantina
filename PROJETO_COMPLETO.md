# 📋 Documentação Completa do Sistema de Cantina

## 📑 Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Módulos e Funcionalidades](#módulos-e-funcionalidades)
4. [Fluxo de Trabalho](#fluxo-de-trabalho)
5. [Tecnologias Utilizadas](#tecnologias-utilizadas)
6. [Estrutura de Arquivos](#estrutura-de-arquivos)
7. [Guia de Desenvolvimento](#guia-de-desenvolvimento)

---

## 🎯 Visão Geral

Sistema completo de gestão de cantina desenvolvido em Django, com foco em eficiência operacional e experiência do usuário. O sistema integra múltiplas interfaces para diferentes perfis de usuários e automatiza processos desde o pedido até a entrega.

### Características Principais

- **Multi-perfil**: Caixa, Cozinha, Cliente, Acompanhamento
- **Tempo Real**: Sincronização automática entre telas
- **Sistema de Combos**: Gestão completa de combos personalizáveis
- **Controle de Estoque**: Abate automático por pedido
- **QR Code**: Acompanhamento de pedidos via código
- **Relatórios**: Dashboard com estatísticas e análises

---

## 🏗️ Arquitetura do Sistema

### Modelo MVC (Model-View-Controller)

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │  Caixa   │  │ Cozinha  │  │ Cliente  │          │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│       │             │              │                 │
│       └─────────────┴──────────────┘                │
│                     │                                │
├─────────────────────┼────────────────────────────────┤
│                  BACKEND                             │
│       ┌─────────────┴─────────────┐                 │
│       │      Django Views         │                 │
│       │  (caixa, cozinha, etc)    │                 │
│       └─────────────┬─────────────┘                 │
│                     │                                │
│       ┌─────────────┴─────────────┐                 │
│       │      Django Models        │                 │
│       │  (Pedido, Produto, etc)   │                 │
│       └─────────────┬─────────────┘                 │
├─────────────────────┼────────────────────────────────┤
│                 DATABASE                             │
│       ┌─────────────┴─────────────┐                 │
│       │        SQLite             │                 │
│       │     (db.sqlite3)          │                 │
│       └───────────────────────────┘                 │
└─────────────────────────────────────────────────────┘
```

### Comunicação em Tempo Real

- **Polling**: Atualização automática a cada 1 segundo
- **LocalStorage**: Sincronização entre abas do navegador
- **WebSocket-like**: Eventos de mudança de status

---

## 📦 Módulos e Funcionalidades

### 1. Módulo Caixa (`/caixa/`)

**Responsabilidades:**
- Criação e gestão de pedidos
- Controle de estoque
- Gestão de produtos e categorias
- Configuração de combos
- Relatórios e estatísticas

**Principais Views:**
- `caixa_dashboard()`: Dashboard principal com abas
- `criar_pedido()`: Criação de novos pedidos
- `configurar_combo()`: Configuração de slots e itens
- `api_pedidos_ativos()`: API para pedidos em tempo real

**Funcionalidades Especiais:**
- Filtro de categorias no cardápio
- Busca de produtos por nome/código
- Abate automático de estoque
- Toast notifications
- Modal de QR Code sincronizado

### 2. Módulo Cozinha (`/cozinha/`)

**Responsabilidades:**
- Visualização de pedidos pendentes
- Atualização de status (Preparando → Pronto)
- Cronômetro de tempo de preparo
- Alertas visuais por tempo

**Principais Views:**
- `dashboard()`: Tela principal da cozinha
- `atualizar_status()`: Mudança de status do pedido

**Funcionalidades Especiais:**
- Cards coloridos por status
- Cronômetro em tempo real
- Sincronização automática com caixa

### 3. Módulo Cliente (`/cliente/`)

**Responsabilidades:**
- Visualização do cardápio
- Acompanhamento de pedido via QR Code
- Interface responsiva para mobile

**Principais Views:**
- `cardapio()`: Exibição do cardápio
- Modal de QR Code sincronizado com caixa

### 4. Módulo Acompanhamento (`/acompanhamento/`)

**Responsabilidades:**
- Tela pública de acompanhamento
- Exibição de status do pedido
- Interface para TV/monitor

**Principais Views:**
- `acompanhar()`: Tela de acompanhamento por QR Code

### 5. Módulo Autoatendimento (`/autoatendimento/`)

**Responsabilidades:**
- Interface de autoatendimento para clientes
- Seleção de produtos
- Finalização de pedidos

### 6. Módulo Painel Status (`/painel_status/`)

**Responsabilidades:**
- Painel público de pedidos prontos
- Exibição em TV/monitor
- Atualização automática

### 7. Módulo Authentication (`/authentication/`)

**Responsabilidades:**
- Login e logout
- Controle de acesso por perfil
- Gestão de usuários

---

## 🔄 Fluxo de Trabalho

### Fluxo Completo de um Pedido

```
1. CAIXA
   ├─ Cliente chega ao balcão
   ├─ Operador adiciona itens ao carrinho
   │  ├─ Produtos normais: clique direto
   │  └─ Combos: seleção de itens por slot
   ├─ Preenche dados do cliente
   ├─ Seleciona forma de pagamento
   └─ Finaliza pedido
      ├─ Gera QR Code
      ├─ Abate estoque
      └─ Status: PENDENTE

2. COZINHA
   ├─ Pedido aparece automaticamente
   ├─ Cozinheiro visualiza itens
   ├─ Inicia preparo → Status: PREPARANDO
   ├─ Finaliza preparo → Status: PRONTO
   └─ Cronômetro registra tempo

3. CLIENTE
   ├─ Escaneia QR Code
   ├─ Acompanha status em tempo real
   └─ Recebe notificação quando pronto

4. ENTREGA
   ├─ Caixa entrega pedido
   └─ Status: ENTREGUE
```

### Sistema de Combos

```
1. CRIAÇÃO DO COMBO
   ├─ Criar produto base (categoria Combo)
   ├─ Configurar slots (ex: Lanche, Batata, Bebida)
   └─ Adicionar itens em cada slot
      ├─ Produto
      ├─ Quantidade de abate
      └─ Estoque disponível

2. VENDA DO COMBO
   ├─ Cliente seleciona combo
   ├─ Sistema abre modal de seleção
   ├─ Cliente escolhe 1 item por slot
   ├─ Sistema valida estoque
   └─ Adiciona ao carrinho com escolhas

3. FINALIZAÇÃO
   ├─ Pedido criado com item combo
   ├─ Registra escolhas (PedidoComboEscolha)
   ├─ Abate estoque dos itens escolhidos
   └─ Combo não tem limite de estoque
```

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Django 6.0.2**: Framework web Python
- **Python 3.14**: Linguagem de programação
- **SQLite**: Banco de dados
- **Pillow**: Processamento de imagens
- **qrcode**: Geração de QR Codes

### Frontend
- **HTML5**: Estrutura
- **CSS3**: Estilização (variáveis CSS, flexbox, grid)
- **JavaScript ES6+**: Interatividade
- **Fetch API**: Requisições assíncronas

### Bibliotecas JavaScript
- **QRCode.js**: Geração de QR Codes no frontend

---

## 📁 Estrutura de Arquivos

```
cantina_system/
├── acompanhamento/          # Módulo de acompanhamento
│   ├── views.py
│   ├── urls.py
│   └── templates/
├── authentication/          # Módulo de autenticação
│   ├── models.py           # Modelo Usuario
│   ├── views.py
│   └── urls.py
├── autoatendimento/        # Módulo de autoatendimento
├── caixa/                  # Módulo principal do caixa
│   ├── models.py           # Modelos: Pedido, Produto, Combo, etc
│   ├── views.py            # Views e APIs
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
├── cantina_system/         # Configurações do projeto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── cliente/                # Módulo do cliente
├── cozinha/                # Módulo da cozinha
├── painel_status/          # Módulo do painel público
├── static/                 # Arquivos estáticos
│   ├── css/
│   │   ├── style.css
│   │   └── pedidos-ativos.css
│   ├── js/
│   │   ├── main.js
│   │   └── caixa.js
│   └── images/
├── templates/              # Templates HTML
│   ├── base.html
│   ├── caixa/
│   ├── cozinha/
│   ├── cliente/
│   └── acompanhamento/
├── media/                  # Uploads (fotos de produtos)
├── venv/                   # Ambiente virtual Python
├── db.sqlite3             # Banco de dados
├── manage.py              # CLI do Django
├── requirements.txt       # Dependências Python
└── *.md                   # Documentação
```

---

## 👨‍💻 Guia de Desenvolvimento

### Configuração do Ambiente

```bash
# 1. Clonar repositório
git clone https://github.com/ibmdaf/Cantina.git
cd Cantina

# 2. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# ou
venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Aplicar migrações
python manage.py migrate

# 5. Criar superusuário
python manage.py createsuperuser

# 6. Iniciar servidor
python manage.py runserver
```

### Convenções de Código

**Python (Backend):**
- PEP 8 style guide
- Docstrings em todas as funções
- Type hints quando possível
- Nomes descritivos em português

**JavaScript (Frontend):**
- camelCase para variáveis e funções
- Comentários explicativos
- Async/await para operações assíncronas
- Console.log para debug (remover em produção)

**CSS:**
- Variáveis CSS para cores e espaçamentos
- BEM naming convention quando aplicável
- Mobile-first approach

### Adicionando Novas Funcionalidades

1. **Criar modelo** (se necessário) em `models.py`
2. **Criar migração**: `python manage.py makemigrations`
3. **Aplicar migração**: `python manage.py migrate`
4. **Criar view** em `views.py`
5. **Adicionar URL** em `urls.py`
6. **Criar template** em `templates/`
7. **Adicionar CSS/JS** em `static/`
8. **Testar funcionalidade**
9. **Documentar mudanças** em `CHANGELOG.md`
10. **Commit e push** para GitHub

### Debugging

**Backend:**
```python
import logging
logger = logging.getLogger(__name__)
logger.error(f'Debug: {variavel}')
```

**Frontend:**
```javascript
console.log('Debug:', variavel);
console.table(array);
```

### Testes

```bash
# Rodar todos os testes
python manage.py test

# Testar app específico
python manage.py test caixa

# Testar com coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 📊 Modelos de Dados Principais

### Pedido
- `numero_pedido`: Número sequencial único
- `cliente_nome`: Nome do cliente
- `tipo`: balcao/delivery
- `status`: pendente/preparando/pronto/entregue/cancelado
- `forma_pagamento`: dinheiro/debito/credito/pix
- `total`: Valor total
- `qr_code`: UUID para acompanhamento

### Produto
- `nome`: Nome do produto
- `preco`: Preço unitário
- `quantidade_estoque`: Estoque disponível
- `categoria`: FK para Categoria
- `ativo`: Boolean
- `is_combo()`: Método que verifica se é combo

### Combo
- `produto`: OneToOne com Produto
- `slots`: ManyToMany com ComboSlot

### ComboSlot
- `nome`: Nome do slot (ex: "Lanche")
- `emoji`: Emoji do slot
- `ordem`: Ordem de exibição
- `itens`: ManyToMany com Produto via ComboSlotItem

### ComboSlotItem
- `slot`: FK para ComboSlot
- `produto`: FK para Produto
- `quantidade_abate`: Quantidade a abater do estoque

### PedidoComboEscolha
- `item_pedido`: FK para ItemPedido
- `slot`: FK para ComboSlot
- `produto_escolhido`: FK para Produto
- `quantidade_abatida`: Quantidade abatida

---

## 🔐 Segurança

- **CSRF Protection**: Tokens em todos os formulários
- **Login Required**: Decorators em views protegidas
- **Permissões por Perfil**: Controle de acesso
- **SQL Injection**: ORM do Django previne
- **XSS**: Template engine escapa HTML automaticamente

---

## 📈 Performance

- **Lazy Loading**: Produtos carregados sob demanda
- **Prefetch Related**: Otimização de queries
- **Cache**: LocalStorage para carrinho temporário
- **Debounce**: Busca com delay para reduzir requisições
- **Polling Inteligente**: Apenas quando necessário

---

## 🚀 Deploy

Ver arquivo `DEPLOY.md` para instruções completas de deploy em produção.

---

## 📝 Licença

Ver arquivo `LICENSE.md` para detalhes da licença.

---

## 👥 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📞 Suporte

Para dúvidas e suporte, consulte:
- `INDICE.md`: Índice de toda documentação
- `INICIO_RAPIDO.md`: Guia de início rápido
- `GUIA_VISUAL.md`: Guia visual com screenshots
- Issues no GitHub: https://github.com/ibmdaf/Cantina/issues

---

**Última atualização:** Fevereiro 2026
**Versão do Sistema:** 2.0.0
