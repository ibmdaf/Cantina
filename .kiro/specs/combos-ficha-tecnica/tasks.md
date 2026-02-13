# Implementation Plan: Sistema de Combos com Ficha Técnica

## Overview

Este plano implementa um sistema completo de combos configuráveis com ficha técnica para o sistema de cantina Django. A implementação seguirá uma abordagem incremental, começando pelos modelos de dados, depois serviços de negócio, views de backend, e finalmente componentes frontend. Cada etapa inclui testes para validação imediata.

## Tasks

- [ ] 1. Criar modelos de dados para combos
  - [ ] 1.1 Criar modelo Combo com relacionamento OneToOne com Produto
    - Adicionar campos: produto (FK), ativo (bool), criado_em, atualizado_em
    - Implementar método validar_integridade()
    - Implementar método obter_slots_ordenados()
    - _Requirements: 1.1, 1.2_
  
  - [ ]* 1.2 Escrever testes de propriedade para modelo Combo
    - **Property 1: Criação de Combo com Atributos Válidos**
    - **Validates: Requirements 1.1, 1.2**
  
  - [ ] 1.3 Criar modelo ComboSlot
    - Adicionar campos: combo (FK), nome, ordem, criado_em
    - Configurar Meta com ordering e unique_together
    - Implementar método obter_itens_ativos()
    - _Requirements: 1.3, 1.4, 1.5_
  
  - [ ]* 1.4 Escrever testes de propriedade para ComboSlot
    - **Property 2: Adição de Múltiplos Slots**
    - **Property 3: Validação de Nome de Slot Obrigatório**
    - **Validates: Requirements 1.3, 1.4, 1.5, 7.3**
  
  - [ ] 1.5 Criar modelo ComboSlotItem
    - Adicionar campos: slot (FK), produto (FK com PROTECT), quantidade_abate (Decimal)
    - Configurar unique_together para slot + produto
    - Implementar método validar_estoque_disponivel()
    - _Requirements: 2.1, 2.2, 2.3_
  
  - [ ]* 1.6 Escrever testes de propriedade para ComboSlotItem
    - **Property 4: Vinculação de Múltiplos Produtos a Slot**
    - **Property 5: Validação de Quantidade de Abate Positiva**
    - **Validates: Requirements 2.1, 2.2, 2.3**
  
  - [ ] 1.7 Criar modelo PedidoComboEscolha
    - Adicionar campos: item_pedido (FK), slot (FK com PROTECT), produto_escolhido (FK com PROTECT), quantidade_abatida
    - Configurar unique_together para item_pedido + slot
    - _Requirements: 5.1, 5.2, 5.3_
  
  - [ ]* 1.8 Escrever testes de propriedade para PedidoComboEscolha
    - **Property 12: Armazenamento Completo de Escolhas**
    - **Property 13: Integridade Referencial de Escolhas**
    - **Validates: Requirements 5.3, 5.4**

- [ ] 2. Criar migrations e registrar modelos no admin
  - [ ] 2.1 Gerar e aplicar migrations para novos modelos
    - Executar makemigrations e migrate
    - Verificar que tabelas foram criadas corretamente
    - _Requirements: 1.1, 1.3, 2.1, 5.1_
  
  - [ ] 2.2 Registrar modelos no Django Admin
    - Criar admin.py com ModelAdmin para Combo, ComboSlot, ComboSlotItem
    - Configurar inlines para visualização hierárquica
    - _Requirements: 3.1_

- [ ] 3. Implementar serviços de negócio
  - [ ] 3.1 Criar ComboService com métodos de gerenciamento
    - Implementar criar_combo(produto_id, slots_data)
    - Implementar atualizar_combo(combo_id, slots_data)
    - Implementar validar_combo_para_venda(combo_id)
    - Implementar obter_opcoes_slots(combo_id)
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 7.5_
  
  - [ ]* 3.2 Escrever testes unitários para ComboService
    - Testar criação de combo com múltiplos slots
    - Testar validação de combo sem slots (deve falhar)
    - Testar atualização de configuração existente
    - _Requirements: 1.1, 1.2, 1.3, 7.4_
  
  - [ ] 3.3 Criar EstoqueService com métodos de controle de estoque
    - Implementar abater_estoque_combo(escolhas)
    - Implementar validar_estoque_disponivel(escolhas)
    - Implementar reverter_abate_combo(escolhas)
    - _Requirements: 6.1, 6.2, 6.3, 6.4_
  
  - [ ]* 3.4 Escrever testes de propriedade para EstoqueService
    - **Property 15: Abate de Estoque com Quantidade Correta**
    - **Property 16: Validação de Estoque Insuficiente**
    - **Property 17: Atualização Imediata de Estoque**
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.4**

- [ ] 4. Checkpoint - Validar camada de dados e serviços
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implementar views de backend para configuração de combos
  - [ ] 5.1 Criar view configurar_combo (GET e POST)
    - GET: retornar configuração atual do combo em JSON
    - POST: validar e salvar nova configuração usando ComboService
    - Adicionar decorators @login_required e @require_http_methods
    - _Requirements: 3.2, 3.3, 3.5, 3.6, 3.7_
  
  - [ ]* 5.2 Escrever testes de integração para configurar_combo
    - Testar GET retorna estrutura correta
    - Testar POST com dados válidos persiste corretamente
    - Testar POST com dados inválidos retorna erro 400
    - _Requirements: 3.2, 3.3, 3.5, 3.6, 3.7_
  
  - [ ] 5.3 Criar view obter_opcoes_combo (POST)
    - Retornar estrutura JSON com slots e itens disponíveis
    - Filtrar apenas produtos ativos com estoque disponível
    - _Requirements: 2.6, 4.2, 4.4, 6.5_
  
  - [ ]* 5.4 Escrever testes de propriedade para obter_opcoes_combo
    - **Property 6: Filtragem de Produtos Ativos**
    - **Property 18: Validação Preventiva de Estoque no Modal**
    - **Validates: Requirements 2.6, 6.5**

- [ ] 6. Implementar views de backend para venda de combos
  - [ ] 6.1 Criar view adicionar_combo_pedido (POST)
    - Validar que todos os slots foram preenchidos
    - Validar estoque disponível usando EstoqueService
    - Criar ItemPedido e PedidoComboEscolha
    - Abater estoque dos produtos escolhidos
    - Retornar JSON com sucesso e detalhes do item
    - _Requirements: 4.5, 4.6, 4.7, 5.1, 5.2, 6.1, 6.2_
  
  - [ ]* 6.2 Escrever testes de propriedade para adicionar_combo_pedido
    - **Property 10: Validação de Seleção Completa**
    - **Property 11: Adição de Combo ao Pedido com Escolhas**
    - **Validates: Requirements 4.5, 4.6, 4.7, 5.1, 5.2**
  
  - [ ]* 6.3 Escrever teste de integração para fluxo completo de venda
    - Testar fluxo: configurar combo → obter opções → adicionar ao pedido → verificar estoque abatido
    - _Requirements: 4.7, 5.1, 5.2, 6.1, 6.2_

- [ ] 7. Adicionar URLs para novas views
  - [ ] 7.1 Criar urls.py ou atualizar existente com rotas de combo
    - Adicionar rota para configurar_combo
    - Adicionar rota para obter_opcoes_combo
    - Adicionar rota para adicionar_combo_pedido
    - _Requirements: 3.2, 4.1, 4.7_

- [ ] 8. Checkpoint - Validar backend completo
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. Implementar componente Modal de Configuração (frontend)
  - [ ] 9.1 Criar arquivo config-combo-modal.js com classe ComboConfigModal
    - Implementar constructor(comboId)
    - Implementar método carregar() para buscar dados via API
    - Implementar método renderizar() para gerar HTML do modal
    - _Requirements: 3.3, 3.4_
  
  - [ ] 9.2 Implementar métodos de manipulação de slots
    - Implementar adicionarSlot()
    - Implementar removerSlot(slotIndex)
    - Implementar reordenarSlots()
    - _Requirements: 3.5, 3.6, 10.5_
  
  - [ ] 9.3 Implementar métodos de manipulação de itens componentes
    - Implementar adicionarItemSlot(slotIndex, produtoId, quantidadeAbate)
    - Implementar removerItemSlot(slotIndex, itemIndex)
    - Adicionar validação de quantidade_abate > 0
    - _Requirements: 2.1, 2.3, 2.4, 2.5_
  
  - [ ] 9.4 Implementar método salvar() com validações
    - Validar que todos os slots têm nome
    - Validar que combo tem pelo menos 1 slot
    - Enviar dados para backend via POST
    - Exibir mensagens de sucesso/erro
    - _Requirements: 1.4, 7.3, 7.4_
  
  - [ ]* 9.5 Escrever testes frontend para ComboConfigModal
    - Testar renderização de slots
    - Testar adição e remoção de slots
    - Testar validações antes de salvar
    - _Requirements: 3.4, 3.5, 3.6_

- [ ] 10. Implementar componente Modal de Seleção (frontend)
  - [ ] 10.1 Criar arquivo selecao-combo-modal.js com classe ComboSelectionModal
    - Implementar constructor(comboId)
    - Implementar método carregar() para buscar opções via API
    - Implementar método renderizar() para gerar campos de seleção dinâmicos
    - _Requirements: 4.1, 4.2, 4.3_
  
  - [ ] 10.2 Implementar lógica de seleção e validação
    - Implementar selecionarItem(slotId, produtoId)
    - Implementar validarSelecao() para verificar se todos os slots foram preenchidos
    - Exibir mensagens de erro para seleção incompleta
    - _Requirements: 4.5, 4.6_
  
  - [ ] 10.3 Implementar método confirmar() para adicionar combo ao pedido
    - Validar seleção completa
    - Enviar escolhas para backend via POST
    - Adicionar combo ao carrinho com detalhes das escolhas
    - Fechar modal e atualizar interface
    - _Requirements: 4.7_
  
  - [ ]* 10.4 Escrever testes de propriedade para ComboSelectionModal
    - **Property 8: Renderização Dinâmica de Slots no Modal de Seleção**
    - **Property 9: Exibição de Todos os Itens Componentes**
    - **Validates: Requirements 4.2, 4.3, 4.4**

- [ ] 11. Integrar combos com sistema de caixa existente
  - [ ] 11.1 Modificar caixa.js para detectar produtos tipo combo
    - Atualizar função adicionarProduto() para verificar se é combo
    - Se for combo, abrir ComboSelectionModal ao invés de adicionar diretamente
    - _Requirements: 4.1_
  
  - [ ] 11.2 Criar função adicionarComboAoPedido()
    - Adicionar combo ao array itensPedido com flag is_combo=true
    - Armazenar escolhas junto com o item
    - Atualizar exibição do carrinho para mostrar detalhes do combo
    - _Requirements: 4.7, 9.1, 9.2, 9.3_
  
  - [ ] 11.3 Atualizar função atualizarListaItens() para renderizar combos
    - Exibir nome do combo como item principal
    - Exibir escolhas de cada slot como sub-itens
    - Manter formatação consistente com design existente
    - _Requirements: 9.1, 9.2, 9.3_

- [ ] 12. Atualizar interface de estoque para gerenciar combos
  - [ ] 12.1 Modificar template da aba Estoque
    - Adicionar indicação visual para produtos tipo combo
    - Adicionar botão "Configurar Combo" para produtos combo
    - _Requirements: 3.1, 3.2_
  
  - [ ] 12.2 Adicionar event listeners para botão "Configurar Combo"
    - Ao clicar, instanciar e abrir ComboConfigModal
    - Passar produto_id correto para o modal
    - _Requirements: 3.3_

- [ ] 13. Implementar exibição de combos em pedidos
  - [ ] 13.1 Atualizar template de visualização de pedidos
    - Modificar renderização de ItemPedido para detectar combos
    - Exibir estrutura hierárquica: combo → escolhas de slots
    - _Requirements: 5.5, 9.1, 9.2, 9.3_
  
  - [ ] 13.2 Atualizar view de cozinha para mostrar detalhes de combos
    - Garantir que todos os detalhes do combo aparecem na tela da cozinha
    - Manter formatação clara e legível
    - _Requirements: 9.4_
  
  - [ ] 13.3 Atualizar geração de comprovante para incluir combos
    - Adicionar lógica para imprimir combo com todas as escolhas
    - Manter formatação consistente com outros itens
    - _Requirements: 9.5_

- [ ] 14. Adicionar validações de integridade e proteções
  - [ ] 14.1 Implementar proteção contra exclusão de produtos vinculados
    - Sobrescrever método delete() do modelo Produto
    - Verificar se produto é usado em ComboSlotItem de combos ativos
    - Lançar exceção se houver vinculação
    - _Requirements: 7.1_
  
  - [ ]* 14.2 Escrever teste de propriedade para proteção de exclusão
    - **Property 19: Proteção de Produtos Vinculados**
    - **Validates: Requirements 7.1**
  
  - [ ] 14.3 Adicionar validação de combo antes de adicionar ao pedido
    - Verificar que todos os slots têm pelo menos 1 item componente ativo
    - Retornar erro descritivo se combo estiver incompleto
    - _Requirements: 7.5_
  
  - [ ]* 14.4 Escrever teste de propriedade para validação de combo
    - **Property 21: Validação de Slots com Itens Ativos**
    - **Validates: Requirements 7.5**

- [ ] 15. Aplicar estilos CSS consistentes com design existente
  - [ ] 15.1 Criar arquivo combo-modals.css
    - Estilizar Modal de Configuração com tema dark e laranja #F4A23A
    - Estilizar Modal de Seleção com tema dark e laranja #F4A23A
    - Garantir responsividade para diferentes tamanhos de tela
    - Adicionar overlay para desabilitar fundo quando modal aberto
    - _Requirements: 8.1, 8.2, 8.3, 8.4_
  
  - [ ] 15.2 Adicionar estilos para indicação visual de combos
    - Criar badge ou ícone para produtos tipo combo na lista de estoque
    - Estilizar exibição hierárquica de combos no carrinho
    - _Requirements: 3.1, 9.1, 9.2_

- [ ] 16. Checkpoint final - Testes end-to-end
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 17. Documentação e refinamentos finais
  - [ ] 17.1 Adicionar docstrings e comentários no código
    - Documentar todos os métodos dos serviços
    - Adicionar comentários explicativos em lógica complexa
    - _Requirements: All_
  
  - [ ] 17.2 Criar ou atualizar documentação de usuário
    - Documentar como criar e configurar combos
    - Documentar como vender combos no PDV
    - Incluir screenshots ou GIFs demonstrativos
    - _Requirements: All_

## Notes

- Tasks marcadas com `*` são opcionais e podem ser puladas para MVP mais rápido
- Cada task referencia requisitos específicos para rastreabilidade
- Checkpoints garantem validação incremental
- Property tests validam propriedades universais de correção
- Unit tests validam exemplos específicos e casos extremos
- A implementação segue ordem lógica: dados → lógica → apresentação
