# Documentação Front-End - Tela de Caixa/Pedidos

## Visão Geral

A tela de Caixa é a interface principal para operadores registrarem e gerenciarem pedidos. Possui layout responsivo com três frames principais que funcionam de forma independente.

---

## Estrutura de Layout

### 1. Header (Barra Superior)
- **Posição**: Fixa no topo (`position: fixed`)
- **Altura**: 45px
- **Componentes**:
  - Logo da empresa (esquerda)
  - Menu de navegação com abas
  - Nome do usuário
  - Botão fullscreen (⛶)
  - Botão Sair

**Características**:
- Nunca rola com o conteúdo
- Z-index: 1000 (sempre visível)
- Background: #1A1A1A

---

### 2. Container Principal
Layout em Flexbox com 3 frames independentes:

```
┌─────────────────────────────────────────────────────────┐
│  [Cardápio]  │  [Novo Pedido]  │  [Pedidos Ativos]     │
│   (flex: 1)  │    (347px)      │      (280px)          │
└─────────────────────────────────────────────────────────┘
```

**Dimensões**:
- Altura: `calc(100vh - 45px)` (viewport menos header)
- Overflow: hidden (sem scroll no container)
- Cada frame tem scroll independente

---

## Frame 1: Cardápio (Esquerda)

### Estrutura
```html
<div class="cardapio-section">
  ├── Header (título + contador)
  ├── Campo de busca
  └── Grid de produtos (com scroll)
</div>
```

### Características
- **Largura**: Flex 1 (ocupa espaço restante)
- **Scroll**: Vertical independente
- **Grid**: `repeat(auto-fill, minmax(220px, 1fr))`
- **Gap**: 0.8rem entre cards

### Cards de Produto
**Dimensões**:
- Largura mínima: 220px
- Altura: Automática (baseada no conteúdo)
- Padding: 1rem
- Border-radius: 10px

**Conteúdo**:
- Título do produto (1rem, quebra de linha automática)
- Código (#XXX) em cinza (#6c757d)
- Preço em laranja (1.2rem, bold)
- Badge de estoque (quando aplicável)

**Estados**:
- Normal: Border #2E2E2E
- Hover: Border laranja + transform translateY(-2px)

---

## Frame 2: Novo Pedido (Centro)

### Estrutura
```html
<div class="pedido-form-section">
  ├── Header (título)
  ├── Formulário (campos fixos)
  ├── Lista de itens (scroll interno)
  ├── Total (fixo)
  └── Botão Finalizar (fixo)
</div>
```

### Características
- **Largura**: 347px (fixa)
- **Scroll**: Apenas na lista de itens
- **Background**: #202020

### Campos do Formulário
1. **Nome do Cliente**
   - Input text
   - Placeholder: "Digite o nome do cliente..."

2. **Tipo** (select)
   - ⛪ Local
   - 🚗 Viagem

3. **Pagamento** (select)
   - 💵 Dinheiro
   - 💳 Débito
   - 💳 Crédito
   - 📱 PIX

4. **Observações**
   - Textarea (1 linha inicial)
   - Redimensionável pelo usuário

### Lista de Itens
**Container**:
- Flex: 1 (expande para preencher espaço)
- Min-height: 0
- Overflow-y: auto
- Scrollbar: 4px, discreta

**Item do Carrinho**:
```
┌────────────────────────────────────┐
│ Nome do Produto        │ [-] 2 [+] │
│ R$ 10,00 • Detalhes    │    [🗑️]   │
└────────────────────────────────────┘
```

**Layout**: Grid (2 colunas: info | ações)
- Padding: 0.5rem
- Gap entre botões: 0.3rem
- Botões: 26px × 26px

### Total e Finalizar
**Sempre visíveis** na parte inferior:
- Total: Fonte 1.1rem, laranja
- Botão: Width 100%, padding 0.7rem

---

## Frame 3: Pedidos Ativos (Direita)

### Estrutura
```html
<div class="pedidos-ativos-sidebar">
  ├── Título (fixo no topo)
  ├── Estatísticas (fixas no topo)
  └── Lista de pedidos (scroll)
</div>
```

### Características
- **Largura**: 280px (fixa)
- **Altura**: `calc(100vh - 45px)`
- **Scroll**: Vertical independente
- **Background**: #1A1A1A
- **Scrollbar**: 4px, discreta

### Título (Sticky)
**Posição**: Fixa no topo (sticky, z-index: 10)
```
🔥 Pedidos Ativos (6)
```
- Background: #0B0B0B
- Padding: 0.6rem
- Border-bottom: 2px solid #2E2E2E
- Fonte: 1.1rem

### Estatísticas (Sticky)
**Posição**: Fixa abaixo do título (sticky, z-index: 9)
```
⏳ 0  |  👨‍🍳 1  |  ✅ 5  |  ⏱️ 12:34
```

**Layout**: Flexbox horizontal (space-between)
- Background: #0B0B0B
- Padding: 0.5rem 0.6rem
- Border-bottom: 1px solid #2E2E2E
- Gap: 0.4rem

**Cada Estatística**:
- Display: flex
- Gap: 0.3rem
- Fonte: 0.75rem
- Ícone: 0.9rem
- Valor: Bold, cor específica

**Cores dos Valores**:
- ⏳ Pendente: #ffc107 (amarelo)
- 👨‍🍳 Preparando: #17a2b8 (azul)
- ✅ Pronto: #28a745 (verde)
- ⏱️ Tempo médio: #F4A23A (laranja)

**Atualização**:
- Polling a cada 3 segundos via `/caixa/api/pedidos-ativos/`
- Tempo médio calculado dos pedidos entregues HOJE
- Ignora pedidos com tempo > 2 horas

### Card de Pedido
**Estrutura Visual**:
```
┌─────────────────────────────────┐
│ João Silva          ⏱️ 12:34    │
│ #001 • Local • 💳 Crédito       │
│                                 │
│ 2x X-Salada         R$ 28,00    │
│ 1x Coca-Cola        R$ 5,00     │
│ ─────────────────────────────   │
│ 💰 Total:           R$ 33,00    │
│                                 │
│ 📝 Obs: Sem cebola              │
│                                 │
│ [✅ Pronto ▼] [📱] [✏️] [🗑️]   │
└─────────────────────────────────┘
```

**Dimensões**:
- Background: #2a2a2a
- Border: 1px solid #2E2E2E
- Border-radius: 8px
- Padding: 0.5rem
- Gap: 1rem entre cards

**Componentes Detalhados**:

#### 1. Cabeçalho (pedido-cabecalho)
**Layout**: Flex (space-between)
- Margin-bottom: 0.65rem

**Nome do Cliente**:
- Fonte: 1.05rem, bold
- Cor: #FFFFFF

**Cronômetro**:
- Display: flex, gap: 0.35rem
- Ícone: ⏱️ (1.15rem)
- Tempo: Fonte monospace, 1.05rem
- Formato: MM:SS ou HH:MM:SS
- Atualização: A cada segundo via JavaScript

**Cores do Cronômetro** (baseado no tempo):
- 0-10min: #BDBDBD (cinza)
- 10-15min: #F4A23A (laranja)
- 15min+: #ff4444 (vermelho)

#### 2. Meta Informações (pedido-meta-info)
**Layout**: Flex horizontal com separadores
- Fonte: 0.8rem
- Cor: #BDBDBD
- Gap: 0.45rem
- Margin-bottom: 0.8rem

**Conteúdo**:
- `#001` - Número do pedido
- `•` - Separador
- `Local` ou `Viagem` - Tipo do pedido
- `•` - Separador
- `💳 Crédito` - Forma de pagamento (dinâmica)

**Formas de Pagamento**:
- 💵 Dinheiro
- 💳 Débito
- 💳 Crédito
- 📱 PIX
- "Não informado" (se vazio)

#### 3. Lista de Itens (pedido-itens-lista)
**Layout**: Flex column
- Margin-bottom: 0.65rem

**Cada Item** (pedido-item-linha):
- Display: flex (space-between)
- Fonte: 0.8rem
- Cor: #FFFFFF (descrição), #FFFFFF (valor)
- Margin-bottom: 0.4rem
- Line-height: 1.35

**Formato**:
```
2x X-Salada                    R$ 28,00
```

**Linha do Total** (pedido-total-linha):
- Border-top: 1px solid #2E2E2E
- Padding-top: 0.4rem
- Margin-top: 0.25rem
- Cor do texto: #F4A23A (laranja)
- Fonte: 0.8rem

#### 4. Observações (pedido-observacoes)
**Exibição**: Condicional (apenas se houver observações)
- Border-top: 1px solid #2E2E2E
- Padding: 0.4rem 0
- Margin-bottom: 0.5rem
- Fonte: 0.8rem
- Line-height: 1.35

**Formato**:
- Label "📝 Obs:" em laranja (#F4A23A)
- Texto em cinza (#BDBDBD)
- Word-wrap: break-word

#### 5. Linha de Ações (pedido-acoes-linha)
**Layout**: Grid (1fr auto auto auto)
- Gap: 0.35rem
- Align-items: center

**Select de Status** (pedido-status-select-inline):
- Flex: 1 (ocupa espaço disponível)
- Padding: 0.35rem 0.55rem
- Border-radius: 5px
- Fonte: 0.7rem
- Cursor: pointer
- Padding-right: 1.65rem (espaço para seta)
- Transition: background-color 0.3s ease

**Cores por Status** (aplicadas via JavaScript):
- `pendente`: Background #ffc107 (amarelo), texto #000
- `preparando`: Background #17a2b8 (azul), texto #fff
- `pronto`: Background #28a745 (verde), texto #fff
- `entregue`: Background #6c757d (cinza), texto #fff

**Opções do Select**:
- ⏳ Fila (pendente)
- 👨‍🍳 Em preparo (preparando)
- ✅ Pronto (pronto)
- 🎉 Entregue (entregue)

**Botões de Ação** (btn-acao-quadrado):
- Dimensões: 24px × 24px
- Border: 2px solid #000 (borda preta grossa)
- Border-radius: 4px
- Display: flex (center)
- Transition: all 0.3s ease
- Hover: transform scale(1.05)

**Botão QR Code** (btn-qr):
- Background: #F4A23A (laranja)
- Ícone: 📱 (0.85rem)
- Função: `mostrarQRCode(qr_code)`

**Botão Editar** (btn-editar):
- Background: #007bff (azul)
- Ícone: ✏️ (0.85rem)
- Função: `abrirModalEditar(pedido_id)`

**Botão Excluir** (btn-cancelar):
- Background: #dc3545 (vermelho)
- Ícone: 🗑️ (0.85rem)
- Função: `abrirModalExcluirPedido(pedido_id)`

### Comportamento Dinâmico

#### Atualização em Tempo Real
**Polling**: A cada 3 segundos
- Endpoint: `/caixa/api/pedidos-ativos/`
- Atualiza: Estatísticas + Cronômetros
- NÃO recria HTML dos cards (mantém layout original do Django)

**Função**: `atualizarPedidosAtivos()`
```javascript
// Atualiza apenas:
// 1. Contador de pedidos no título
// 2. Valores das estatísticas
// 3. Cronômetros dos cards existentes
```

#### Mudança de Status
**Função**: `alterarStatusPedido(selectElement)`
- Envia POST para `/caixa/alterar-status-pedido/`
- Atualiza cor do select dinamicamente
- Se status = "entregue": Remove card após 2 segundos (fade out)

#### Inicialização
**DOMContentLoaded**:
1. `iniciarCronometros()` - Inicia contadores
2. `atualizarCoresStatus()` - Aplica cores aos selects
3. `iniciarPollingPedidos()` - Inicia atualização automática

### Classes CSS Principais

```css
.pedidos-ativos-sidebar      /* Container principal */
.sidebar-titulo               /* Título fixo */
.sidebar-stats                /* Estatísticas fixas */
.sidebar-stat                 /* Cada estatística */
.pedidos-lista                /* Container dos cards */
.pedido-card-simples          /* Card individual */
.pedido-cabecalho             /* Nome + cronômetro */
.pedido-nome-cliente          /* Nome do cliente */
.pedido-cronometro            /* Container do cronômetro */
.cronometro-icon              /* Ícone ⏱️ */
.cronometro-tempo             /* Tempo formatado */
.pedido-meta-info             /* Linha de metadados */
.pedido-meta-separador        /* Separador • */
.pedido-itens-lista           /* Lista de itens */
.pedido-item-linha            /* Cada item */
.item-descricao               /* Descrição do item */
.item-valor                   /* Valor do item */
.pedido-total-linha           /* Linha do total */
.item-valor-total             /* Valor total */
.pedido-observacoes           /* Observações */
.obs-label                    /* Label "Obs:" */
.obs-texto                    /* Texto da observação */
.pedido-acoes-linha           /* Linha de ações */
.pedido-status-select-inline  /* Select de status */
.btn-acao-quadrado            /* Botões de ação */
.btn-qr                       /* Botão QR Code */
.btn-editar                   /* Botão Editar */
.btn-cancelar                 /* Botão Excluir */
.btn-icon-grande              /* Ícone do botão */
```

### Arquivo CSS
`static/css/pedidos-ativos.css` - 300+ linhas de estilos específicos

---

## Paleta de Cores

```css
--bg-primary: #0B0B0B      /* Fundo principal */
--bg-header: #1A1A1A       /* Header e sidebar */
--bg-card: #202020         /* Cards e formulários */
--border-color: #2E2E2E    /* Bordas */
--text-primary: #FFFFFF    /* Texto principal */
--text-secondary: #BDBDBD  /* Texto secundário */
--btn-primary: #F4A23A     /* Botões e destaques */
--btn-hover: #D98A1F       /* Hover dos botões */
--btn-text: #111111        /* Texto em botões */
```

---

## Scrollbars Personalizadas

Todas as áreas com scroll usam scrollbars discretas:

```css
::-webkit-scrollbar {
    width: 4px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 2px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.2);
}
```

---

## Responsividade

### Desktop (> 1024px)
- Layout padrão com 3 colunas

### Tablet (768px - 1024px)
- Sidebar de pedidos oculta
- Layout em 2 colunas

### Mobile (< 768px)
- Layout em coluna única
- Frames empilhados verticalmente

---

## Funcionalidades JavaScript

### 1. Adicionar Produto ao Carrinho
```javascript
adicionarProduto(id, nome, preco)
```
- Adiciona item à lista
- Atualiza contador
- Atualiza total

### 2. Alterar Status do Pedido
```javascript
alterarStatusPedido(selectElement)
```
- Envia requisição AJAX
- Atualiza cor do select
- Remove card se status = "entregue"

### 3. Cronômetros
```javascript
iniciarCronometros()
```
- Atualiza a cada segundo
- Calcula tempo desde criação
- Muda cor baseado no tempo

### 4. Busca de Produtos
- Filtra por nome ou código
- Atualização em tempo real
- Case-insensitive

### 5. Fullscreen
```javascript
toggleFullscreen()
```
- Alterna modo tela cheia
- Compatível com todos navegadores
- Atualiza ícone do botão

---

## Arquivos Principais

### Templates
- `templates/base.html` - Layout base com header
- `templates/caixa/dashboard.html` - Tela principal

### CSS
- `static/css/style.css` - Estilos globais
- `static/css/pedidos-ativos.css` - Estilos da sidebar

### JavaScript
- `static/js/main.js` - Funções utilitárias
- `static/js/caixa.js` - Lógica específica da tela

---

## Boas Práticas Implementadas

1. **Scroll Independente**: Cada frame gerencia seu próprio scroll
2. **Header Fixo**: Sempre visível, não rola
3. **Altura Automática**: Cards se adaptam ao conteúdo
4. **Feedback Visual**: Hover states em todos elementos clicáveis
5. **Acessibilidade**: Tooltips e labels descritivos
6. **Performance**: CSS otimizado, transições suaves
7. **Responsividade**: Layout adapta-se a diferentes telas

---

## Melhorias Futuras Sugeridas

1. Drag & drop para reordenar itens
2. Atalhos de teclado
3. Impressão automática de pedidos
4. Notificações sonoras para novos pedidos
5. Modo escuro/claro
6. Filtros avançados na busca
7. Histórico de pedidos inline
8. Suporte a múltiplos idiomas

---

**Última atualização**: 12/02/2026
**Versão**: 2.0

**Changelog v2.0**:
- Adicionadas estatísticas em tempo real no frame de Pedidos Ativos
- Documentação completa do layout dos cards com todas as classes CSS
- Detalhamento do comportamento dinâmico (polling, cronômetros, cores)
- Especificação das cores por status do select
- Documentação dos botões de ação com bordas pretas
- Adicionada seção de comportamento dinâmico e inicialização
