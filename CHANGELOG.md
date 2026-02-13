# 📝 Changelog - Sistema Cantina

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [2.1.0] - 11/02/2026

### 🐛 Corrigido

#### Sistema de Combos - Slots com 1 Item Não Apareciam
**Problema**: Quando um slot tinha apenas 1 item e esse item estava inativo, o slot não aparecia no modal de seleção.

**Causa**: A API `obter_opcoes_combo` filtrava apenas produtos ativos usando `obter_itens_ativos()`.

**Solução**:
- Backend: Modificada view para buscar TODOS os itens (`slot.itens.all()`)
- Backend: Adicionado campo `produto_ativo` na resposta JSON
- Frontend: Produtos inativos aparecem mas não podem ser selecionados
- Frontend: Mensagem clara "Produto inativo ⚠️"
- Frontend: Feedback visual diferenciado (opacidade, cursor)

**Arquivos Alterados**:
- `caixa/views.py` - View `obter_opcoes_combo()`
- `templates/caixa/dashboard.html` - Função `renderizarSlotsSelecao()`
- `templates/caixa/dashboard.html` - Função `selecionarOpcaoCombo()`

**Impacto**: Agora todos os itens configurados aparecem no modal, independente do status.

---

### 📊 Melhorado

#### Sistema de Relatórios - Logs de Debug
**Adicionado**: Logs detalhados para facilitar troubleshooting.

**Backend**:
- Logs de empresa, filtro, período
- Logs de quantidade de pedidos encontrados
- Logs de resumo calculado
- Logs de top itens e histórico

**Frontend**:
- Logs de carregamento de relatórios
- Logs de URL da requisição
- Logs de status da resposta
- Logs de dados recebidos
- Logs de renderização

**Arquivos Alterados**:
- `caixa/views.py` - View `relatorios_dados()`
- `templates/caixa/dashboard.html` - Função `carregarRelatorios()`
- `templates/caixa/dashboard.html` - Função `renderizarHistorico()`
- `templates/caixa/dashboard.html` - Função `renderizarTopItens()`

**Impacto**: Facilita identificação de problemas no carregamento de dados.

---

#### Sistema de Relatórios - Barra de Rolagem
**Corrigido**: Barra de rolagem não funcionava corretamente.

**Mudanças**:
- Alterado `overflow-y: scroll` para `overflow-y: auto`
- Adicionado `min-height: 300px`
- Mantido `max-height: 450px`

**Arquivos Alterados**:
- `templates/caixa/dashboard.html` - CSS `.table-scroll-container-historico`

**Impacto**: Barra de rolagem aparece apenas quando necessário.

---

### 📚 Documentação

#### Nova Documentação do Sistema de Combos
**Adicionado**: Documentação completa do sistema de combos.

**Conteúdo**:
- Visão geral e características
- Arquitetura e componentes
- Modelos de dados detalhados
- Fluxo de funcionamento com diagramas
- APIs e endpoints com exemplos
- Interface do usuário
- Validações e regras de negócio
- Correções e melhorias implementadas
- Troubleshooting e boas práticas
- Referências e arquivos relacionados

**Arquivo Criado**:
- `DOCUMENTACAO_SISTEMA_COMBOS.md`

**Arquivos Atualizados**:
- `INDICE.md` - Adicionada referência à nova documentação

**Impacto**: Facilita entendimento e manutenção do sistema de combos.

---

## [2.0.0] - 10/02/2026

### ✨ Adicionado

#### Sistema Completo de Combos
**Novo**: Sistema para criar produtos compostos por múltiplas escolhas.

**Funcionalidades**:
- Criação de combos com múltiplos slots
- Cada slot pode ter uma ou mais opções
- Controle de estoque automático
- Seleção automática quando há apenas 1 opção
- Validação de disponibilidade em tempo real
- Modal de configuração (Aba Estoque)
- Modal de seleção (Aba Novo Pedido)

**Modelos Criados**:
- `Combo` - Produto combo
- `ComboSlot` - Categoria de escolha
- `ComboSlotItem` - Opção disponível
- `PedidoComboEscolha` - Registro de escolhas

**Views Criadas**:
- `configurar_combo()` - Criar/editar combo
- `obter_opcoes_combo()` - Buscar opções
- `adicionar_combo_pedido()` - Adicionar ao carrinho
- `listar_produtos_para_combo()` - Listar produtos

**Migrations**:
- `0004_combo_comboslot_comboslotitem_pedidocomboescolha.py`
- `0005_remove_comboslotitem_unique_constraint.py`

---

#### Categoria Especial "Combo"
**Novo**: Categoria do sistema não editável para combos.

**Funcionalidades**:
- Campo `is_sistema` no modelo Categoria
- Categoria "Combo" (🎁) criada automaticamente
- Não pode ser editada ou excluída
- Vinculada automaticamente a todos os combos
- Estilo visual diferenciado (fundo azul claro)

**Migrations**:
- `0007_categoria_is_sistema.py`
- `0008_criar_categoria_combo.py`

**Script Criado**:
- `criar_categoria_combo.py` - Manutenção manual

---

#### Sistema de Gerenciamento de Categorias
**Novo**: Interface para criar e gerenciar categorias.

**Funcionalidades**:
- Botão "📂 Categorias" na aba Estoque
- Modal responsivo com 2 colunas
- Campo emoji com seletor visual (52 emojis)
- Criação, edição e exclusão de categorias
- Validações: duplicatas e categorias em uso
- Integração automática em todos os campos

**Views Criadas**:
- `listar_categorias()` - Listar categorias
- `criar_categoria()` - Criar categoria
- `editar_categoria()` - Editar categoria
- `excluir_categoria()` - Excluir categoria

**Migration**:
- `0006_categoria_emoji.py`

---

#### Tela de Acompanhamento Mobile
**Novo**: Tela para clientes acompanharem pedidos.

**Funcionalidades**:
- Design mobile-friendly com tema escuro
- Polling a cada 3 segundos
- Esteira de progresso visual
- Hierarquia invertida (nome em destaque)
- Alerta quando pedido fica pronto:
  - Tela pisca verde
  - Som de beep
  - Vibração do celular

**Arquivos**:
- `templates/acompanhamento/acompanhar.html`
- `acompanhamento/views.py`

---

#### Tela da Cozinha Redesenhada
**Novo**: Tela mobile-first para gestão de pedidos.

**Funcionalidades**:
- Sem menu superior (foco total)
- Cards mobile-first
- Esteira de status com barra colorida
- Cronômetro inteligente (muda cor após 10min e 15min)
- Botão único para avançar status
- Atualização em tempo real (polling 3s)
- API JSON para pedidos

**Arquivos**:
- `templates/cozinha/dashboard.html`
- `cozinha/views.py`
- `cozinha/urls.py`

---

#### Sistema de Exclusão de Pedidos
**Novo**: Exclusão segura com validação.

**Funcionalidades**:
- Modal de confirmação
- Campo de texto que exige digitar "EXCLUIR"
- Botão desabilitado até validação
- Devolve itens ao estoque (normais e combos)
- Remove valores do relatório

**View Criada**:
- `excluir_pedido()` - Excluir pedido

---

#### Controle de Acesso por Tipo de Usuário
**Novo**: Restrições baseadas em perfil.

**Regras**:
- **Administrador**: Acesso total
- **Gerente**: Tudo exceto Admin Django
- **Operador de Caixa**: Sem Admin Django, Configurações e Usuários
- **Cozinha**: Apenas tela da cozinha

**Funcionalidades**:
- Redirecionamento automático
- Abas ocultas conforme perfil
- Modal de edição de usuário
- Botão "🚪 Sair" na tela da cozinha

**Views Atualizadas**:
- `caixa_dashboard()` - Controle de acesso
- `obter_usuario()` - Buscar dados do usuário
- `editar_usuario()` - Editar usuário

---

### 🎨 Melhorado

#### Padronização de Modais
**Melhorado**: Todos os modais seguem o mesmo padrão.

**Mudanças**:
- Fecham ao clicar fora (sem salvar)
- Cabeçalhos padronizados
- Responsividade: 90vw desktop, 95vw mobile
- Cores roxas removidas
- Função `fecharModalSeForaDoConteudo()` atualizada

**Modais Padronizados**:
- Modal de Produto
- Modal de Combo
- Modal de Seleção de Combo
- Modal de Categorias
- Modal de Edição de Usuário
- Modal de Exclusão de Pedido

---

#### Layout de Modais em 2 Colunas
**Melhorado**: Melhor organização visual.

**Modais Atualizados**:
- **Modal Combo**: Informações (350px) + Slots (flex)
- **Modal Categorias**: Criar (280px) + Listar (flex)
- **Responsivo**: Empilha em 1 coluna em telas < 968px
- Scroll independente nas listas
- Barras de rolagem laranja customizadas

---

#### Aba de Relatórios
**Melhorado**: Dashboard completo com filtros.

**Funcionalidades**:
- Filtros rápidos (Hoje, Ontem, Semana, Mês, Personalizado)
- Cards de resumo (Vendas, Pedidos, Ticket Médio, Itens)
- Top 5/10 itens mais vendidos
- Histórico de vendas em tabela
- Atualização em tempo real (5s)
- Botões de exportação (PDF, Excel)

**View Criada**:
- `relatorios_dados()` - API de dados

---

#### Aba de Links
**Melhorado**: Mais responsivo e otimizado.

**Mudanças**:
- Grid mais eficiente (280px mínimo)
- Cards otimizados com flexbox
- Ícones menores (2.5rem)
- Fontes otimizadas
- Mobile: 1 coluna
- Desktop grande: 3 colunas fixas

---

#### Aba de Estoque
**Melhorado**: Filtros e pesquisa.

**Funcionalidades**:
- Campo de pesquisa por nome ou código
- Filtro dropdown de categorias
- Botão "Limpar" para resetar
- Feedback visual quando não há resultados
- Coluna de categoria na tabela
- Botão "✏️ Editar" em cada linha
- Edição inteligente (abre modal correto)

---

#### Categoria Obrigatória
**Melhorado**: Validação ao cadastrar produto.

**Mudanças**:
- Campo marcado com asterisco vermelho
- Atributo `required` no select
- Validação JavaScript
- Validação backend
- Mensagem de erro clara

---

#### Fullscreen Mantido ao Trocar Abas
**Corrigido**: Fullscreen não fecha mais ao trocar de aba.

**Mudanças**:
- Adicionado `event.preventDefault()`
- Chamada direta ao `showTab()`
- History API para atualizar URL
- Suporte a navegação do navegador

---

### 🔧 Técnico

#### Integração de Categorias
**Melhorado**: Sincronização automática.

**Funcionalidades**:
- Função `popularCamposCategoria()` criada
- Popula select de categoria no modal de produto
- Popula filtro de categoria na aba estoque
- Chamada após criar/editar/excluir categoria
- Chamada no `DOMContentLoaded`
- Removidos `location.reload()` desnecessários

---

#### Correção de Erros JavaScript
**Corrigido**: Erros que quebravam funcionalidades.

**Problemas Corrigidos**:
- Linhas duplicadas em `renderizarCategorias()`
- Template strings aninhados com backticks
- Solução: Extrair expressões para variáveis

**Impacto**: Botões e cronômetros voltaram a funcionar.

---

## [1.0.0] - Data Anterior

### ✨ Versão Inicial

- Sistema de autenticação
- Gestão de pedidos
- Gestão de produtos
- Gestão de categorias
- Painel de status
- Autoatendimento
- Cardápio do cliente
- Relatórios básicos

---

## Tipos de Mudanças

- `✨ Adicionado` - Novas funcionalidades
- `🎨 Melhorado` - Melhorias em funcionalidades existentes
- `🐛 Corrigido` - Correções de bugs
- `🔧 Técnico` - Mudanças técnicas/refatoração
- `📚 Documentação` - Mudanças na documentação
- `🔒 Segurança` - Correções de segurança
- `⚠️ Depreciado` - Funcionalidades que serão removidas
- `🗑️ Removido` - Funcionalidades removidas

---

**Formato de Versionamento**: MAJOR.MINOR.PATCH

- **MAJOR**: Mudanças incompatíveis com versões anteriores
- **MINOR**: Novas funcionalidades compatíveis
- **PATCH**: Correções de bugs compatíveis

---

*Última atualização: 11/02/2026*
