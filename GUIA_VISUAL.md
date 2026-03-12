# 📸 Guia Visual do Sistema

## 🎨 Paleta de Cores

```
┌─────────────────────────────────────────┐
│  Primária: #FF6B35 (Laranja)           │
│  ████████████████████████████████████   │
│                                         │
│  Secundária: #000000 (Preto)           │
│  ████████████████████████████████████   │
│                                         │
│  Accent: #FFFFFF (Branco)              │
│  ████████████████████████████████████   │
└─────────────────────────────────────────┘
```

---

## 🖥️ Tela 1: Login

```
┌─────────────────────────────────────────────────┐
│                                                 │
│              🍽️ Cantina                        │
│         Sistema de Gestão                       │
│                                                 │
│  ┌───────────────────────────────────────┐    │
│  │ Usuário                               │    │
│  │ [____________________________]        │    │
│  │                                       │    │
│  │ Senha                                 │    │
│  │ [____________________________]        │    │
│  │                                       │    │
│  │     [ Entrar ]                        │    │
│  └───────────────────────────────────────┘    │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Características:**
- Fundo gradiente preto
- Card branco centralizado
- Logo laranja
- Campos de entrada estilizados
- Botão laranja com hover effect

---

## 💰 Tela 2: Caixa (Operador)

```
┌─────────────────────────────────────────────────────────────────┐
│ 🍽️ Cantina System    |    João (Caixa) | Cantina Delícias | Sair│
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  💰 Caixa - Novo Pedido                                        │
│                                                                 │
│  ┌──────────────────────┐  ┌──────────────────────────────┐  │
│  │ PRODUTOS             │  │ PEDIDO ATUAL                  │  │
│  │                      │  │                               │  │
│  │ [Categoria ▼]        │  │ Tipo: [Balcão ▼]             │  │
│  │                      │  │ Cliente: [____________]       │  │
│  │ ┌────────────────┐  │  │ Mesa: [____]                  │  │
│  │ │ X-Burger       │  │  │                               │  │
│  │ │ Hambúrguer...  │  │  │ Itens:                        │  │
│  │ │ R$ 15.90       │  │  │ ┌──────────────────────────┐ │  │
│  │ └────────────────┘  │  │ │ 2x X-Burger    [-][+][🗑️]│ │  │
│  │                      │  │ │ R$ 15.90 x 2              │ │  │
│  │ ┌────────────────┐  │  │ └──────────────────────────┘ │  │
│  │ │ X-Bacon        │  │  │                               │  │
│  │ │ Hambúrguer...  │  │  │ ┌──────────────────────────┐ │  │
│  │ │ R$ 18.90       │  │  │ │ 1x Coca-Cola   [-][+][🗑️]│ │  │
│  │ └────────────────┘  │  │ │ R$ 5.00 x 1               │ │  │
│  │                      │  │ └──────────────────────────┘ │  │
│  │ ┌────────────────┐  │  │                               │  │
│  │ │ Coca-Cola      │  │  │ ─────────────────────────────│  │
│  │ │ Refrigerante   │  │  │ Total: R$ 36.80              │  │
│  │ │ R$ 5.00        │  │  │                               │  │
│  │ └────────────────┘  │  │ [ Finalizar Pedido ]         │  │
│  └──────────────────────┘  └──────────────────────────────┘  │
│                                                                 │
│  Pedidos Recentes                                              │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ #0001 | Balcão | João | [Preparando] | R$ 36.80 | 14:30│  │
│  │ #0002 | Mesa 5 | Maria| [Pendente]   | R$ 45.00 | 14:35│  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Características:**
- Layout em 2 colunas
- Grid de produtos clicáveis
- Carrinho interativo
- Cálculo automático de total
- Lista de pedidos recentes

---

## 👨‍🍳 Tela 3: Cozinha

```
┌─────────────────────────────────────────────────────────────────┐
│ 🍽️ Cantina System    |    Pedro (Cozinha) | Cantina Delícias   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  👨‍🍳 Cozinha - Gestão de Pedidos                              │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                    │
│  │⏳PENDENTES│  │🔥PREPARANDO│  │✅PRONTOS │                    │
│  │   (3)     │  │    (2)    │  │   (1)   │                    │
│  └──────────┘  └──────────┘  └──────────┘                    │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                    │
│  │#0001      │  │#0003      │  │#0005      │                    │
│  │Balcão     │  │Mesa 3     │  │Mesa 7     │                    │
│  │14:30      │  │14:25      │  │14:20      │                    │
│  │           │  │           │  │           │                    │
│  │Itens:     │  │Itens:     │  │Itens:     │                    │
│  │2x X-Burger│  │1x Lasanha │  │1x P.Feito │                    │
│  │1x Coca    │  │1x Suco    │  │           │                    │
│  │           │  │           │  │           │                    │
│  │[Iniciar]  │  │[Pronto]   │  │[Entregue] │                    │
│  └──────────┘  └──────────┘  └──────────┘                    │
│                                                                 │
│  ┌──────────┐  ┌──────────┐                                   │
│  │#0002      │  │#0004      │                                   │
│  │Mesa 5     │  │Delivery   │                                   │
│  │14:35      │  │14:28      │                                   │
│  │           │  │           │                                   │
│  │Itens:     │  │Itens:     │                                   │
│  │1x X-Bacon │  │2x Hot Dog │                                   │
│  │1x Pudim   │  │2x Coca    │                                   │
│  │           │  │           │                                   │
│  │[Iniciar]  │  │[Pronto]   │                                   │
│  └──────────┘  └──────────┘                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Características:**
- Layout Kanban (3 colunas)
- Cards coloridos por status
- Botões de ação em cada card
- Auto-refresh a cada 30s
- Visualização clara dos itens

---

## 📱 Tela 4: Acompanhamento (Cliente via QR Code)

```
┌─────────────────────────────────────┐
│                                     │
│           🍽️                        │
│      Pedido #0001                   │
│    Cantina Delícias                 │
│                                     │
│  ┌───────────────────────────────┐ │
│  │                               │ │
│  │  ●─────────────────────       │ │
│  │  📝 Pedido Recebido           │ │
│  │  Seu pedido foi registrado    │ │
│  │  │                            │ │
│  │  ●─────────────────────       │ │
│  │  👨‍🍳 Em Preparo (ATUAL)       │ │
│  │  Estamos preparando...        │ │
│  │  │                            │ │
│  │  ○─────────────────────       │ │
│  │  ✅ Pronto                    │ │
│  │  Seu pedido está pronto!      │ │
│  │  │                            │ │
│  │  ○─────────────────────       │ │
│  │  🎉 Entregue                  │ │
│  │  Bom apetite!                 │ │
│  │                               │ │
│  └───────────────────────────────┘ │
│                                     │
│  Itens do Pedido:                   │
│  ┌───────────────────────────────┐ │
│  │ 2x X-Burger      R$ 31.80     │ │
│  │ 1x Coca-Cola     R$  5.00     │ │
│  │ ─────────────────────────────│ │
│  │ Total:           R$ 36.80     │ │
│  └───────────────────────────────┘ │
│                                     │
│         Mesa: 5                     │
│                                     │
└─────────────────────────────────────┘
```

**Características:**
- Timeline visual do status
- Animação no status atual
- Lista de itens
- Total do pedido
- Auto-refresh a cada 15s
- Design mobile-first

---

## 📊 Tela 5: Painel de Status

```
┌─────────────────────────────────────────────────────────────────┐
│ 🍽️ Cantina System    |    Ana (Gerente) | Cantina Delícias     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📊 Painel de Status Geral                                     │
│                                                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │   45     │ │ R$ 1.250 │ │    8     │ │    5     │        │
│  │ Pedidos  │ │  Vendas  │ │Pendentes │ │ Preparo  │        │
│  │   Hoje   │ │   Hoje   │ │          │ │          │        │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
│                                                                 │
│  Pedidos Ativos                                                │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ Nº    │ Tipo   │ Mesa │ Status      │ Total  │ Tempo   │  │
│  ├─────────────────────────────────────────────────────────┤  │
│  │ #0001 │ Balcão │  -   │[Preparando] │ R$36.80│ 14:30   │  │
│  │ #0002 │ Mesa   │  5   │[Pendente]   │ R$45.00│ 14:35   │  │
│  │ #0003 │ Mesa   │  3   │[Preparando] │ R$38.00│ 14:25   │  │
│  │ #0004 │Delivery│  -   │[Preparando] │ R$25.80│ 14:28   │  │
│  │ #0005 │ Mesa   │  7   │[Pronto]     │ R$25.00│ 14:20   │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Características:**
- Cards de estatísticas coloridos
- Tabela de pedidos ativos
- Status badges coloridos
- Auto-refresh a cada 10s
- Visão geral do dia

---

## 🖥️ Tela 6: Totem de Autoatendimento

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│              🍽️ Cantina Delícias                               │
│                 Faça seu pedido                                 │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Todas as Categorias ▼]                                       │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                    │
│  │ [FOTO]   │  │ [FOTO]   │  │ [FOTO]   │                    │
│  │          │  │          │  │          │                    │
│  │ X-Burger │  │ X-Bacon  │  │ X-Salada │                    │
│  │          │  │          │  │          │                    │
│  │Hambúrguer│  │Hambúrguer│  │Hambúrguer│                    │
│  │com queijo│  │com bacon │  │completo  │                    │
│  │          │  │          │  │          │                    │
│  │ R$ 15.90 │  │ R$ 18.90 │  │ R$ 16.90 │                    │
│  └──────────┘  └──────────┘  └──────────┘                    │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                    │
│  │ [FOTO]   │  │ [FOTO]   │  │ [FOTO]   │                    │
│  │          │  │          │  │          │                    │
│  │ Coca-Cola│  │  Suco    │  │  Água    │                    │
│  │          │  │          │  │          │                    │
│  │Refrigerante│ │Natural   │  │ Mineral  │                    │
│  │  350ml   │  │  500ml   │  │  500ml   │                    │
│  │          │  │          │  │          │                    │
│  │ R$  5.00 │  │ R$  8.00 │  │ R$  3.00 │                    │
│  └──────────┘  └──────────┘  └──────────┘                    │
│                                                                 │
│                                    ┌──────────────────┐        │
│                                    │  🛒  3 itens     │        │
│                                    └──────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

**Características:**
- Grid de produtos com fotos
- Filtro por categoria
- Carrinho flutuante
- Design touch-friendly
- Cores vibrantes

---

## 📖 Tela 7: Cardápio (Visão Cliente)

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                        🍽️                                       │
│                 Cantina Delícias                                │
│                  Nosso Cardápio                                 │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ═══════════════════════════════════════════════════════════   │
│  LANCHES                                                        │
│  ═══════════════════════════════════════════════════════════   │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ [FOTO] │ X-Burger                                      │   │
│  │        │ Hambúrguer com queijo, alface e tomate       │   │
│  │        │                              R$ 15.90         │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ [FOTO] │ X-Bacon                                       │   │
│  │        │ Hambúrguer com bacon e molho especial        │   │
│  │        │                              R$ 18.90         │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ═══════════════════════════════════════════════════════════   │
│  BEBIDAS                                                        │
│  ═══════════════════════════════════════════════════════════   │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ [FOTO] │ Coca-Cola 350ml                               │   │
│  │        │ Refrigerante lata                             │   │
│  │        │                              R$  5.00         │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  Cantina Delícias - (11) 98765-4321                            │
│  Rua das Flores, 123 - Centro                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Características:**
- Layout limpo e elegante
- Organizado por categorias
- Fotos dos produtos
- Informações da empresa no rodapé
- Responsivo

---

## 🎨 Elementos de Design

### Botões

```
┌──────────────────┐
│  [ Primário ]    │  ← Laranja (#FF6B35)
│  [ Secundário ]  │  ← Preto (#000000)
│  [ Sucesso ]     │  ← Verde (#28a745)
│  [ Perigo ]      │  ← Vermelho (#dc3545)
└──────────────────┘
```

### Status Badges

```
┌──────────────────────────┐
│ [Pendente]   ← Amarelo   │
│ [Preparando] ← Azul      │
│ [Pronto]     ← Verde     │
│ [Entregue]   ← Ciano     │
│ [Cancelado]  ← Vermelho  │
└──────────────────────────┘
```

### Cards

```
┌─────────────────────────┐
│                         │
│  Título do Card         │
│  ─────────────────────  │
│                         │
│  Conteúdo aqui...       │
│                         │
│  [ Ação ]               │
│                         │
└─────────────────────────┘
```

---

## 📱 Responsividade

### Desktop (1920x1080)
- Layout em múltiplas colunas
- Grid de 3-4 produtos por linha
- Sidebar visível
- Tabelas completas

### Tablet (768x1024)
- Layout em 2 colunas
- Grid de 2-3 produtos por linha
- Menu adaptado
- Tabelas scrolláveis

### Mobile (375x667)
- Layout em 1 coluna
- Grid de 1-2 produtos por linha
- Menu hambúrguer
- Cards empilhados

---

## 🎯 Fluxo Visual

```
LOGIN
  ↓
DASHBOARD (redireciona por tipo)
  ↓
┌─────────┬──────────┬─────────┐
│  CAIXA  │ COZINHA  │ PAINEL  │
└─────────┴──────────┴─────────┘
     ↓         ↓          ↓
  PEDIDO → PREPARO → ENTREGA
     ↓
  QR CODE
     ↓
ACOMPANHAMENTO
```

---

## 💡 Dicas de UX

1. **Cores Consistentes**: Laranja para ações principais
2. **Feedback Visual**: Hover effects em todos os elementos clicáveis
3. **Loading States**: Animações durante carregamento
4. **Auto-refresh**: Atualização automática nas telas críticas
5. **Mobile-first**: Design pensado primeiro para mobile
6. **Acessibilidade**: Contraste adequado, textos legíveis
7. **Ícones**: Emojis para facilitar compreensão
8. **Espaçamento**: Breathing room entre elementos

---

## 📏 Padrões de Espaçamento em Formulários e Modais

### Sistema de Espaçamento Padronizado (8px/16px/24px)

Todos os formulários e modais do sistema seguem um padrão consistente baseado em múltiplos de 8px:

```
┌─────────────────────────────────────────┐
│                                         │
│  Título do Modal/Formulário             │  ← 24px (margin-bottom)
│                                         │
│  ↓ Espaço entre título e primeiro campo│
│                                         │
│  Label do Campo                         │  ← 8px (gap)
│  ↓ Espaço entre label e campo          │
│  [______________]                       │
│                                         │  ← 16px (gap entre campos)
│  ↓ Espaço entre campos                 │
│                                         │
│  Próximo Label                          │  ← 8px (gap)
│  ↓                                      │
│  [______________]                       │
│                                         │  ← 24px (margin-top)
│  ↓ Espaço entre seção e botões         │
│                                         │
│  [Cancelar]  [Confirmar]                │
│                                         │
└─────────────────────────────────────────┘
```

### Escala de Espaçamento

- **8px** - Micro espaçamento (label → campo)
- **16px** - Espaçamento padrão (entre campos relacionados, entre colunas, entre botões)
- **24px** - Separação de seções (título → conteúdo, conteúdo → botões, entre grupos)

### Implementação CSS

**Estrutura de Campos**:
```css
/* Container de campo com label e input */
display: flex;
flex-direction: column;
gap: 8px; /* Label → Campo */

/* Container de múltiplos campos */
display: flex;
flex-direction: column;
gap: 16px; /* Entre campos */

/* Título do modal/seção */
margin-bottom: 24px !important;

/* Botões de ação */
margin-top: 24px !important;
gap: 16px; /* Entre botões */
```

### Modais Padronizados

✅ **Modal Novo Usuário**
- Título → Primeiro campo: 24px
- Label → Campo: 8px
- Entre campos: 16px
- Campos → Botões: 24px
- Entre botões: 16px

✅ **Modal Editar Usuário**
- Título → Primeiro campo: 24px
- Label → Campo: 8px
- Entre campos: 16px
- Campos → Botões: 24px
- Entre botões: 16px

✅ **Modal Novo Produto / Editar Produto**
- Título → Primeiro campo: 24px
- Label → Campo: 8px
- Entre campos: 16px
- Entre colunas: 16px (grid gap)
- Campos → Botões: 24px
- Entre botões: 16px

✅ **Modal Categorias**
- Título seção → Primeiro campo: 16px
- Label → Campo: 8px
- Entre campos: 16px
- Campo → Botão: 8px
- Entre colunas: 16px

✅ **Modal Novo Combo / Editar Combo**
- Título seção → Primeiro campo: 16px
- Label → Campo: 8px
- Entre campos: 16px
- Campo → Info box: 8px
- Entre colunas: 16px

✅ **Modal Excluir Pedido**
- Título → Conteúdo: 24px
- Entre elementos de conteúdo: 16px
- Label → Campo: 8px
- Conteúdo → Botões: 24px
- Entre botões: 16px

✅ **Tela Novo Pedido**
- Título → Primeiro campo: 24px
- Label → Campo: 8px
- Entre campos: 16px
- Entre grupos: 24px
- Entre colunas: 16px
- Observações → Itens: 24px
- Carrinho → Total: 24px
- Total → Botão: 16px
- Padding do card: 24px

### Objetivo do Padrão

O sistema de espaçamento foi projetado para:
1. **Criar hierarquia visual clara** - Espaços maiores separam seções, menores associam elementos
2. **Melhorar legibilidade** - Breathing room adequado entre elementos
3. **Consistência em todo o sistema** - Mesma experiência em todos os modais e formulários
4. **Facilitar manutenção** - Padrão documentado e fácil de aplicar
5. **Evitar confusão** - Fica claro qual label pertence a qual campo

### Regras de Aplicação

1. **Sempre use `!important`** quando necessário para sobrescrever estilos globais
2. **Use `margin-bottom: 0 !important`** em labels para controlar espaçamento via `gap`
3. **Prefira `gap`** ao invés de margins individuais para espaçamento entre elementos
4. **Use `flex-direction: column`** com `gap` para estruturas verticais
5. **Mantenha consistência** - não invente novos valores de espaçamento

---

## 📏 Padrões de Espaçamento em Formulários (LEGADO - Substituído pelo padrão acima)

### Medidas Padrão

```
┌─────────────────────────────────────────┐
│                                         │
│  Campo Anterior: [______________]       │
│                                         │  ← 2.2rem (GRANDE)
│  ↓ Espaço entre campo e próximo título │
│                                         │
│  Próximo Título                         │  ← 0.3rem (PEQUENO)
│  ↓ Espaço entre título e seu campo     │
│  Seu Campo: [______________]            │
│                                         │
└─────────────────────────────────────────┘
```

### Classes CSS Aplicadas

**`.form-group`** (Espaçamento vertical entre grupos)
- `margin-top: 2.2rem` - Espaço GRANDE entre campo anterior e próximo título
- `gap: 0.3rem` - Espaço PEQUENO entre título e seu campo
- `margin-bottom: 0` - Sem margem inferior
- Primeiro `.form-group` tem `margin-top: 0`

**`.form-row`** (Campos lado a lado)
- `margin-top: 2.2rem` - Consistente com `.form-group`
- `gap: 0.6rem` - Espaço entre colunas
- `.form-row .form-group` tem `margin-top: 0` (não duplicar espaço)

**`.form-label`** (Títulos dos campos)
- `margin-bottom: 0` - Controlado pelo `gap` do `.form-group`
- `font-size: 0.85rem`
- `font-weight: 500`

### Modais Específicos

**Modal de Editar Pedido** (`.modal-editar-dados`)
- `margin-top: 1.5rem` - Espaçamento reduzido para modal compacto
- Primeiro `.form-group` tem `margin-top: 0`

**Modal de Produto** (`.modal-produto-coluna-esquerda/direita`)
- `gap: 1.5rem` - Espaçamento entre grupos de campos
- `.form-group` interno com `gap: 0.3rem`
- `.form-label` com `margin-bottom: 0`

### Formulários Afetados

✅ Novo Pedido (aba Pedido)
✅ Novo Produto / Editar Produto
✅ Novo Usuário / Editar Usuário
✅ Novo Combo / Editar Combo
✅ Modal de Excluir Pedido
✅ Modal de Editar Pedido
✅ Modal de Categorias
✅ Todos os formulários que usam `.form-group` e `.form-label`

### Objetivo do Padrão

O espaçamento foi projetado para:
1. **Separar visualmente** grupos de campos (espaço grande)
2. **Associar** título ao seu campo (espaço pequeno)
3. **Melhorar legibilidade** e compreensão do formulário
4. **Evitar confusão** sobre qual título pertence a qual campo

---

**Este guia visual ajuda a entender o layout e design do sistema sem precisar executá-lo!**
