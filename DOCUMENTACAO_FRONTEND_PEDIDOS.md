# Documentação Frontend - Tela de Pedidos (Caixa)

## ⚠️ IMPORTANTE: NÃO ALTERAR O LAYOUT VISUAL

Esta documentação serve como referência para manter o layout atual durante alterações de funcionalidade.

---

## 📐 Estrutura de Layout

### Layout Geral
- **Tipo**: Flexbox horizontal
- **Altura**: `calc(100vh - 45px)` (viewport menos header)
- **Overflow**: `hidden` (sem scroll no container principal)
- **Gap**: `0` (sem espaçamento entre frames)

### Três Frames Principais

#### 1. Frame Cardápio (Esquerda)
- **Largura**: `flex: 1` (expansível)
- **Scroll**: Independente vertical
- **Padding direito**: `0.3rem`

#### 2. Frame Novo Pedido (Centro)
- **Largura**: `347px` (fixa)
- **Min/Max Width**: `347px`
- **Scroll**: Apenas na lista de itens internamente
- **Background**: `var(--bg-card)` (#202020)
- **Border**: `1px solid var(--border-color)`
- **Border-radius**: `10px`
- **Padding**: `1rem`

#### 3. Frame Pedidos Ativos (Direita)
- **Largura**: `280px` (fixa)
- **Min/Max Width**: `280px`
- **Scroll**: Independente vertical
- **Background**: `var(--bg-header)` (#1A1A1A)
- **Border-left**: `1px solid var(--border-color)`

---

## 🎨 Paleta de Cores

```css
--bg-primary: #0B0B0B      /* Fundo principal */
--bg-header: #1A1A1A       /* Header e sidebar */
--bg-card: #202020         /* Cards e formulários */
--border-color: #2E2E2E    /* Bordas */
--text-primary: #FFFFFF    /* Texto principal */
--text-secondary: #BDBDBD  /* Texto secundário */
--btn-primary: #F4A23A     /* Botão primário (laranja) */
--btn-hover: #D98A1F       /* Hover do botão */
--btn-text: #111111        /* Texto do botão */
```

---

## 📦 Frame 1: Cardápio

### Header do Cardápio
```css
.cardapio-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    flex-shrink: 0;
}
```

**Título**: 
- Texto: "🍽️ Cardápio"
- Font-size: `1.1rem`
- Font-weight: `normal`
- Color: `var(--text-primary)`

**Contador de itens**:
- Background: `var(--bg-card)`
- Color: `var(--text-secondary)`
- Padding: `0.3rem 0.8rem`
- Border-radius: `16px`
- Font-size: `0.8rem`
- Border: `1px solid var(--border-color)`

### Campo de Busca
```css
.busca-produto {
    margin-bottom: 0.8rem;
    flex-shrink: 0;
}

.busca-produto .form-control {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    padding: 0.7rem 0.9rem;
    font-size: 0.9rem;
}
```

### Grid de Produtos
```css
.produtos-cardapio-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 0.8rem;
    flex: 1;
    overflow: visible;
    grid-auto-rows: min-content;
}
```

### Cards de Produto
```css
.produto-card-cardapio {
    background: var(--bg-card);
    border: 2px solid var(--border-color);
    border-radius: 10px;
    padding: 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    position: relative;
    height: auto; /* Altura automática baseada no conteúdo */
}

.produto-card-cardapio:hover {
    border-color: var(--btn-primary);
    background: #252525;
    transform: translateY(-2px);
}
```

**Estrutura do Card**:
- **Título**: 
  - Font-size: `1rem`
  - Font-weight: `600`
  - Line-height: `1.4`
  - Color: `var(--text-primary)`
  - Word-wrap: `break-word`
  
- **Código**: 
  - Font-size: `0.75rem`
  - Font-weight: `500`
  - Color: `#6c757d` (cinza)
  
- **Preço**: 
  - Font-size: `1.2rem`
  - Font-weight: `bold`
  - Color: `var(--btn-primary)` (laranja)
  - Margin-top: `0.3rem`

- **Badge de Estoque** (quando presente):
  - Position: `absolute`
  - Top/Right: `0.8rem`
  - Background: `rgba(40, 167, 69, 0.2)`
  - Color: `#28a745` (verde)
  - Padding: `0.25rem 0.6rem`
  - Border-radius: `12px`
  - Font-size: `0.75rem`

### Scrollbar do Cardápio
```css
.cardapio-section::-webkit-scrollbar {
    width: 4px;
}

.cardapio-section::-webkit-scrollbar-track {
    background: transparent;
}

.cardapio-section::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 2px;
}

.cardapio-section::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.2);
}
```

---

## 📝 Frame 2: Novo Pedido

### Header do Formulário
```css
.form-header h3 {
    color: var(--text-primary);
    font-size: 1.1rem;
    margin: 0;
    font-weight: 600;
    flex-shrink: 0;
}
```

### Campos do Formulário

**Labels**:
```css
.form-label {
    color: var(--text-primary);
    font-weight: normal; /* SEM NEGRITO */
    font-size: 0.8rem;
}
```

**Inputs e Selects**:
```css
.form-control {
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    padding: 0.6rem 0.7rem;
    border-radius: 6px;
    font-size: 0.85rem;
}

.form-control:focus {
    border-color: var(--btn-primary);
    outline: none;
}
```

**Layout de Campos em Linha**:
```css
.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.6rem;
    flex-shrink: 0;
}
```

**Textarea de Observações**:
- Rows: `1` (uma linha inicial)
- Resize: `vertical` (usuário pode expandir)
- Min-height: `60px`

### Seção de Itens do Carrinho

```css
.itens-section {
    border: 1px solid var(--border-color);
    border-radius: 6px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    flex: 1; /* Expande para preencher espaço disponível */
    min-height: 0;
}

.itens-header {
    background: var(--bg-primary);
    padding: 0.5rem 0.7rem;
    border-bottom: 1px solid var(--border-color);
    color: var(--text-primary);
    font-weight: 500;
    font-size: 0.85rem;
    flex-shrink: 0;
}

.lista-itens-pedido {
    overflow-y: auto;
    padding: 0.6rem;
    background: var(--bg-primary);
    flex: 1;
    min-height: 0;
}
```

**Scrollbar da Lista de Itens**:
```css
.lista-itens-pedido::-webkit-scrollbar {
    width: 4px;
}

.lista-itens-pedido::-webkit-scrollbar-track {
    background: transparent;
}

.lista-itens-pedido::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 2px;
}

.lista-itens-pedido::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.2);
}
```

### Carrinho Vazio
```css
.carrinho-vazio {
    text-align: center;
    padding: 3rem 1rem;
    color: var(--text-secondary);
}

.carrinho-vazio-icon {
    font-size: 3rem;
    margin-bottom: 0.5rem;
    opacity: 0.5;
}

.carrinho-vazio p {
    margin: 0.5rem 0;
    font-weight: 400;
    color: var(--text-secondary);
    font-size: 0.95rem;
}

.carrinho-vazio small {
    color: var(--text-secondary);
    opacity: 0.7;
    font-size: 0.85rem;
}
```

### Item do Carrinho
```css
.item-carrinho {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 0.5rem;
    padding: 0.5rem;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    margin-bottom: 0.4rem;
}

.item-info {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
    min-width: 0;
}

.item-nome {
    color: var(--text-primary);
    font-weight: 600;
    font-size: 0.85rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.item-detalhes {
    color: var(--text-secondary);
    font-size: 0.75rem;
    white-space: nowrap;
}

.item-acoes {
    display: flex;
    align-items: center;
    gap: 0.3rem;
    flex-shrink: 0;
}
```

**Botões de Quantidade**:
```css
.btn-qty {
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    width: 26px;
    height: 26px;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
    font-size: 0.9rem;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.btn-qty:hover {
    background: var(--btn-primary);
    border-color: var(--btn-primary);
    color: var(--btn-text);
}

.item-quantidade {
    color: var(--text-primary);
    font-weight: bold;
    min-width: 24px;
    text-align: center;
    font-size: 0.85rem;
}
```

**Botão Remover**:
```css
.btn-remove {
    background: transparent;
    border: 1px solid var(--border-color);
    color: #dc3545;
    width: 26px;
    height: 26px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.btn-remove:hover {
    background: #dc3545;
    border-color: #dc3545;
    color: white;
}
```

### Total e Botão Finalizar (FIXOS NA PARTE INFERIOR)

```css
.total-pedido-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.4rem 0.6rem;
    background: transparent;
    border: none;
    border-radius: 4px;
    flex-shrink: 0;
    margin-top: 0.4rem;
}

.total-label {
    font-size: 1.1rem;
    color: var(--btn-primary);
    font-weight: normal;
}

.total-valor {
    font-size: 1.1rem;
    color: var(--btn-primary);
    font-weight: normal;
}

.btn-finalizar-pedido-full {
    width: 100%;
    padding: 0.7rem;
    background: var(--btn-primary);
    color: var(--btn-text);
    border: none;
    border-radius: 6px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    flex-shrink: 0;
    margin-top: 0.4rem;
}

.btn-finalizar-pedido-full:hover {
    background: var(--btn-hover);
    transform: translateY(-1px);
}

.btn-finalizar-pedido-full:disabled {
    background: var(--border-color);
    color: var(--text-secondary);
    cursor: not-allowed;
    transform: none;
}
```

---

## 🔥 Frame 3: Pedidos Ativos

### Título da Sidebar
```css
.sidebar-titulo {
    background: var(--bg-primary);
    padding: 0.6rem;
    border-bottom: 2px solid var(--border-color);
    display: flex;
    align-items: center;
    gap: 0.6rem;
    position: sticky;
    top: 0;
    z-index: 10;
}

.titulo-icon {
    font-size: 1.1rem;
}

.titulo-texto {
    color: var(--text-primary);
    font-size: 1.1rem;
    font-weight: normal;
}

.titulo-contador {
    color: var(--text-secondary);
    font-size: 0.9rem;
    font-weight: normal;
    margin-left: 0.3rem;
}
```

### Lista de Pedidos
```css
.pedidos-lista {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
}
```

### Card de Pedido
```css
.pedido-card-simples {
    background: #2a2a2a;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 0.5rem;
}
```

### Cabeçalho do Pedido
```css
.pedido-cabecalho {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.65rem;
}

.pedido-nome-cliente {
    color: var(--text-primary);
    font-size: 1.05rem;
    font-weight: bold;
}
```

### Cronômetro
```css
.pedido-cronometro {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    color: var(--btn-primary);
    font-size: 1.05rem;
    font-weight: normal;
}

.cronometro-icon {
    font-size: 1.15rem;
}

.cronometro-tempo {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    letter-spacing: 0.05em;
    font-weight: normal;
}
```

**Cores do Cronômetro** (baseado no tempo):
- Menos de 15 min: `var(--btn-primary)` (laranja)
- 15-30 min: `#ffc107` (amarelo)
- Mais de 30 min: `#dc3545` (vermelho)

### Meta Informações
```css
.pedido-meta-info {
    color: var(--text-secondary);
    font-size: 0.8rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.45rem;
}

.pedido-meta-separador {
    color: var(--text-secondary);
}
```

### Lista de Itens do Pedido
```css
.pedido-itens-lista {
    margin-bottom: 0.65rem;
}

.pedido-item-linha {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    color: var(--text-secondary);
    font-size: 0.8rem;
    margin-bottom: 0.4rem;
    line-height: 1.35;
}

.item-descricao {
    flex: 1;
    color: var(--text-primary);
    font-weight: normal;
}

.item-valor {
    color: var(--text-primary);
    font-weight: normal;
    white-space: nowrap;
    margin-left: 0.9rem;
}
```

### Linha do Total
```css
.pedido-total-linha {
    border-top: 1px solid var(--border-color);
    padding-top: 0.4rem;
    margin-top: 0.25rem;
}

.pedido-total-linha .item-descricao {
    color: var(--btn-primary);
}

.item-valor-total {
    color: var(--btn-primary);
    font-weight: normal;
    white-space: nowrap;
    margin-left: 0.9rem;
    font-size: 0.8rem;
}
```

### Observações (DISCRETAS)
```css
.pedido-observacoes {
    padding: 0.4rem 0;
    margin-bottom: 0.5rem;
    font-size: 0.8rem;
    line-height: 1.35;
    border-top: 1px solid var(--border-color);
    padding-top: 0.5rem;
}

.obs-label {
    color: var(--btn-primary);
    font-weight: normal;
}

.obs-texto {
    color: var(--text-secondary);
    word-wrap: break-word;
}
```

### Linha de Ações
```css
.pedido-acoes-linha {
    display: grid;
    grid-template-columns: 1fr auto auto auto;
    gap: 0.35rem;
    align-items: center;
}
```

### Select de Status
```css
.pedido-status-select-inline {
    background: #6c757d;
    color: white;
    border: none;
    padding: 0.35rem 0.55rem;
    border-radius: 5px;
    font-size: 0.7rem;
    font-weight: normal;
    cursor: pointer;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='9' height='9' viewBox='0 0 12 12'%3E%3Cpath fill='white' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 0.45rem center;
    background-size: 7.5px;
    padding-right: 1.65rem;
}

.pedido-status-select-inline:hover {
    background-color: #5a6268;
}

.pedido-status-select-inline:focus {
    outline: 2px solid var(--btn-primary);
    outline-offset: 2px;
}
```

**Cores por Status**:
- `pendente`: `#6c757d` (cinza)
- `preparando`: `#17a2b8` (azul)
- `pronto`: `#28a745` (verde)
- `entregue`: `#007bff` (azul claro)

### Botões de Ação
```css
.btn-acao-quadrado {
    width: 24px;
    height: 24px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.btn-qr {
    background: var(--btn-primary);
    color: var(--btn-text);
}

.btn-qr:hover {
    background: var(--btn-hover);
}

.btn-editar {
    background: #007bff;
    color: white;
}

.btn-editar:hover {
    background: #0056b3;
}

.btn-cancelar {
    background: #dc3545;
    color: white;
}

.btn-cancelar:hover {
    background: #c82333;
}

.btn-icon-grande {
    font-size: 0.78rem;
}
```

### Scrollbar dos Pedidos Ativos
```css
.pedidos-ativos-sidebar::-webkit-scrollbar {
    width: 4px;
}

.pedidos-ativos-sidebar::-webkit-scrollbar-track {
    background: transparent;
}

.pedidos-ativos-sidebar::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 2px;
}

.pedidos-ativos-sidebar::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.2);
}
```

---

## 🎯 Header (Fixo)

```css
.header {
    background: #1A1A1A;
    color: var(--text-light);
    padding: 0.3rem 1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.5);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    height: 45px;
}
```

### Botão Fullscreen
```css
.btn-fullscreen {
    padding: 0.3rem 0.5rem;
    min-width: 40px;
    font-size: 1rem;
    cursor: pointer;
}
```

---

## 📱 Responsividade

### Scrollbars Discretas (Padrão Global)
- **Width**: `4px`
- **Track**: `transparent`
- **Thumb**: `rgba(255, 255, 255, 0.1)`
- **Thumb Hover**: `rgba(255, 255, 255, 0.2)`
- **Border-radius**: `2px`

---

## ⚡ Comportamentos Importantes

### Scroll Independente
- Cada frame tem seu próprio scroll
- Body e container principal: `overflow: hidden`
- Menu superior: `position: fixed` (nunca rola)

### Total e Botão Finalizar
- **SEMPRE VISÍVEIS** na parte inferior do frame "Novo Pedido"
- Não rolam com a lista de itens
- `flex-shrink: 0` para não encolher

### Cards de Produto
- **Altura automática** baseada no conteúdo
- `grid-auto-rows: min-content` para evitar espaços vazios
- Nomes longos quebram em múltiplas linhas

### Cronômetros
- Atualizam a cada segundo
- Mudam de cor baseado no tempo decorrido
- Formato: `MM:SS` ou `HH:MM:SS`

---

## 📂 Arquivos Relacionados

- **Template**: `templates/caixa/dashboard.html`
- **CSS Global**: `static/css/style.css`
- **CSS Sidebar**: `static/css/pedidos-ativos.css`
- **JavaScript**: `static/js/caixa.js`
- **JavaScript Global**: `static/js/main.js`
- **Base Template**: `templates/base.html`

---

## 🔒 Regras de Preservação

### NÃO ALTERAR:
1. Larguras dos frames (flex:1, 347px, 280px)
2. Cores da paleta
3. Tamanhos de fonte
4. Espaçamentos (padding, margin, gap)
5. Border-radius
6. Comportamento de scroll
7. Posição fixa do Total e Botão Finalizar
8. Altura automática dos cards de produto
9. Estilo discreto das observações
10. Scrollbars de 4px transparentes

### PODE ALTERAR:
- Funcionalidades JavaScript
- Lógica de backend
- Conteúdo dinâmico
- Validações
- Requisições AJAX
- Eventos de clique/submit

---

**Data de Criação**: 10/02/2026  
**Versão**: 1.0  
**Status**: Layout Finalizado - Pronto para Alterações de Funcionalidade
