# Requirements Document - Sistema de Combos com Ficha Técnica

## Introduction

Este documento especifica os requisitos para um sistema de combos configuráveis com ficha técnica para o sistema de cantina Django. O sistema permitirá criar produtos do tipo "combo" onde cada combo possui múltiplos slots de escolha, e cada slot pode conter vários produtos disponíveis para seleção. Ao vender um combo, o operador ou cliente seleciona um produto para cada slot, e o sistema abate automaticamente o estoque dos produtos componentes conforme as quantidades definidas na ficha técnica.

## Glossary

- **Combo**: Produto especial composto por múltiplos slots de escolha
- **Slot**: Posição de escolha dentro de um combo (ex: "Pastel", "Bebida", "Sobremesa")
- **Item_Componente**: Produto do estoque que pode ser escolhido em um slot específico
- **Ficha_Técnica**: Configuração que define quais produtos podem ser escolhidos em cada slot e quanto abater do estoque
- **Quantidade_Abate**: Quantidade que será descontada do estoque quando um item componente for escolhido
- **Escolha_Combo**: Registro da seleção feita pelo cliente/operador para cada slot de um combo vendido
- **Sistema_Estoque**: Sistema existente de controle de produtos e quantidades
- **PDV**: Ponto de Venda - interface de caixa para registrar pedidos
- **Modal_Seleção**: Interface modal que permite escolher os itens de cada slot do combo

## Requirements

### Requirement 1: Cadastro de Combos

**User Story:** Como administrador da cantina, eu quero cadastrar produtos do tipo combo com múltiplos slots de escolha, para que eu possa oferecer combinações de produtos aos clientes.

#### Acceptance Criteria

1. THE Sistema SHALL permitir criar um produto marcado como tipo "combo"
2. WHEN um combo é criado, THE Sistema SHALL permitir definir um nome e preço para o combo
3. THE Sistema SHALL permitir adicionar múltiplos slots a um combo
4. WHEN um slot é adicionado, THE Sistema SHALL exigir um nome descritivo para o slot
5. THE Sistema SHALL permitir definir a ordem de exibição dos slots

### Requirement 2: Configuração de Slots e Itens Componentes

**User Story:** Como administrador da cantina, eu quero configurar quais produtos do estoque podem ser escolhidos em cada slot do combo, para que eu possa controlar as opções disponíveis.

#### Acceptance Criteria

1. WHEN um slot é criado, THE Sistema SHALL permitir vincular múltiplos produtos do estoque como itens componentes
2. WHEN um item componente é vinculado a um slot, THE Sistema SHALL exigir a definição da quantidade de abate do estoque
3. THE Sistema SHALL validar que a quantidade de abate seja um número positivo maior que zero
4. THE Sistema SHALL permitir remover itens componentes de um slot
5. THE Sistema SHALL permitir adicionar novos itens componentes a slots existentes
6. THE Sistema SHALL exibir apenas produtos ativos do estoque como opções para vincular aos slots

### Requirement 3: Gestão de Combos na Interface de Estoque

**User Story:** Como operador do sistema, eu quero gerenciar combos através da aba Estoque do Caixa, para que eu possa configurar e editar combos no mesmo local onde gerencio produtos.

#### Acceptance Criteria

1. WHEN a aba Estoque é exibida, THE Sistema SHALL mostrar produtos do tipo combo com indicação visual diferenciada
2. WHEN um produto combo é selecionado, THE Sistema SHALL exibir um botão "Configurar Combo"
3. WHEN o botão "Configurar Combo" é clicado, THE Sistema SHALL abrir um modal de configuração
4. THE Modal_Configuração SHALL exibir todos os slots do combo com seus itens componentes
5. THE Modal_Configuração SHALL permitir adicionar novos slots
6. THE Modal_Configuração SHALL permitir remover slots existentes
7. THE Modal_Configuração SHALL permitir editar o nome e ordem dos slots
8. WHEN um slot não possui itens componentes vinculados, THE Sistema SHALL exibir um aviso visual

### Requirement 4: Venda de Combos no PDV

**User Story:** Como operador de caixa, eu quero adicionar combos aos pedidos e selecionar os itens de cada slot, para que eu possa registrar a venda completa do combo.

#### Acceptance Criteria

1. WHEN um produto combo é adicionado ao pedido, THE Sistema SHALL abrir um Modal_Seleção
2. THE Modal_Seleção SHALL exibir um campo de seleção para cada slot do combo
3. THE Modal_Seleção SHALL adaptar-se dinamicamente ao número de slots configurados no combo
4. WHEN um slot é exibido, THE Sistema SHALL mostrar todos os itens componentes disponíveis para escolha
5. THE Sistema SHALL validar que todos os slots tenham um item selecionado antes de confirmar
6. WHEN a seleção está incompleta e o usuário tenta confirmar, THE Sistema SHALL exibir mensagem de erro e impedir a confirmação
7. WHEN todos os slots estão preenchidos e o usuário confirma, THE Sistema SHALL adicionar o combo ao pedido com as escolhas registradas

### Requirement 5: Registro de Escolhas de Combo

**User Story:** Como administrador, eu quero que o sistema registre quais itens foram escolhidos em cada combo vendido, para que eu possa ter histórico completo das vendas.

#### Acceptance Criteria

1. WHEN um combo é confirmado no pedido, THE Sistema SHALL criar um registro de ItemPedido para o combo
2. WHEN um ItemPedido de combo é criado, THE Sistema SHALL criar registros de Escolha_Combo para cada slot
3. THE Escolha_Combo SHALL armazenar o slot, o produto escolhido e a quantidade de abate
4. THE Sistema SHALL manter a integridade referencial entre ItemPedido e Escolha_Combo
5. WHEN um pedido é consultado, THE Sistema SHALL exibir o combo com os itens escolhidos em cada slot

### Requirement 6: Abate de Estoque Automático

**User Story:** Como administrador, eu quero que o estoque dos produtos componentes seja abatido automaticamente quando um combo for vendido, para que o controle de estoque seja preciso.

#### Acceptance Criteria

1. WHEN um pedido contendo combo é confirmado, THE Sistema SHALL abater o estoque de cada produto escolhido nos slots
2. THE Sistema SHALL abater a quantidade definida na ficha técnica para cada item componente
3. WHEN o estoque de um produto componente é insuficiente, THE Sistema SHALL impedir a confirmação do pedido
4. WHEN o estoque é abatido, THE Sistema SHALL atualizar imediatamente a quantidade disponível
5. THE Sistema SHALL validar disponibilidade de estoque antes de permitir a seleção de itens no Modal_Seleção

### Requirement 7: Validações de Integridade

**User Story:** Como administrador, eu quero que o sistema valide a integridade dos combos, para que não ocorram erros durante as vendas.

#### Acceptance Criteria

1. THE Sistema SHALL impedir a exclusão de produtos que estão vinculados como itens componentes de combos ativos
2. WHEN um produto vinculado a um combo é desativado, THE Sistema SHALL exibir aviso ao configurar o combo
3. THE Sistema SHALL impedir a criação de slots sem nome
4. THE Sistema SHALL impedir a criação de combos sem pelo menos um slot
5. WHEN um combo é adicionado ao pedido, THE Sistema SHALL validar que todos os slots possuem pelo menos um item componente ativo

### Requirement 8: Interface Responsiva e Consistente

**User Story:** Como usuário do sistema, eu quero que as interfaces de configuração e seleção de combos sejam responsivas e consistentes com o design atual, para que a experiência seja fluida.

#### Acceptance Criteria

1. THE Modal_Configuração SHALL ser responsivo e adaptar-se a diferentes tamanhos de tela
2. THE Modal_Seleção SHALL ser responsivo e adaptar-se a diferentes tamanhos de tela
3. THE Sistema SHALL utilizar o tema dark com cor laranja #F4A23A conforme padrão existente
4. WHEN modais são exibidos, THE Sistema SHALL desabilitar interações com o conteúdo de fundo
5. THE Sistema SHALL exibir indicadores de carregamento durante operações assíncronas
6. THE Sistema SHALL exibir mensagens de sucesso e erro de forma clara e visível

### Requirement 9: Exibição de Combos em Pedidos

**User Story:** Como operador, eu quero visualizar os detalhes dos combos nos pedidos, para que eu possa confirmar as escolhas feitas.

#### Acceptance Criteria

1. WHEN um pedido contém combos, THE Sistema SHALL exibir o nome do combo como item principal
2. THE Sistema SHALL exibir os itens escolhidos de cada slot como sub-itens do combo
3. THE Sistema SHALL exibir o nome do slot e o produto escolhido para cada seleção
4. WHEN o pedido é exibido na cozinha, THE Sistema SHALL mostrar todos os detalhes do combo
5. WHEN o pedido é impresso, THE Sistema SHALL incluir todos os detalhes do combo no comprovante

### Requirement 10: Flexibilidade de Configuração

**User Story:** Como administrador, eu quero ter flexibilidade total para criar combos com diferentes quantidades de slots, para que eu possa atender diferentes necessidades comerciais.

#### Acceptance Criteria

1. THE Sistema SHALL permitir criar combos com 2 ou mais slots
2. THE Sistema SHALL permitir criar combos com até 10 slots
3. THE Sistema SHALL permitir que cada slot tenha entre 1 e 50 itens componentes
4. THE Sistema SHALL permitir definir quantidades de abate com até 3 casas decimais
5. THE Sistema SHALL permitir reordenar slots através de drag-and-drop ou botões de ordenação
