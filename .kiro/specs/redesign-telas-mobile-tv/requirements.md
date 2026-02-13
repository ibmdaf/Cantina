# Requisitos: Redesign de Telas Mobile e TV

## 1. Visão Geral
Redesenhar três telas críticas do sistema de cantina para otimizar a experiência em diferentes dispositivos e contextos de uso: cozinha (mobile), acompanhamento do cliente (mobile via QR Code) e painel de fila (TV/Monitor).

## 2. Objetivos
- Criar interface mobile-first para a tela da cozinha
- Implementar tela de acompanhamento acessível via QR Code com visualização de progresso
- Desenvolver painel de TV/Monitor para exibição pública da fila de pedidos
- Melhorar a experiência do usuário em cada contexto específico

## 3. User Stories

### 3.1 Tela Cozinha (Mobile)
**Como** funcionário da cozinha  
**Quero** visualizar pedidos em uma lista vertical simplificada  
**Para que** eu possa processar pedidos rapidamente em um dispositivo móvel

**Critérios de Aceitação:**
- [ ] 3.1.1 Lista vertical de pedidos ordenada por ordem de chegada (mais antigo primeiro)
- [ ] 3.1.2 Cada card de pedido exibe: Nome do cliente, Número do pedido (senha), Cronômetro de espera, Lista de itens, Observações
- [ ] 3.1.3 Botão grande "Avançar Status" em cada card
- [ ] 3.1.4 Cronômetro muda de cor conforme tempo: verde (0-15min), amarelo (15-30min), vermelho (30+min)
- [ ] 3.1.5 Interface otimizada para telas mobile (responsiva)
- [ ] 3.1.6 Ao clicar em "Avançar Status", o pedido muda para o próximo status (Fila → Preparando → Pronto → Entregue)
- [ ] 3.1.7 Pedidos com status "Entregue" são removidos da lista automaticamente
- [ ] 3.1.8 Layout limpo e minimalista para facilitar leitura rápida

### 3.2 Tela Acompanhamento (Mobile via QR Code)
**Como** cliente  
**Quero** acompanhar meu pedido via QR Code  
**Para que** eu saiba quando meu pedido estará pronto

**Critérios de Aceitação:**
- [ ] 3.2.1 Tela acessível via QR Code único por pedido
- [ ] 3.2.2 Exibe nome do cliente e número do pedido (senha)
- [ ] 3.2.3 Mostra status atual com frase criativa contextual
- [ ] 3.2.4 "Esteira de Progresso" visual com 4 etapas: Fila → Preparando → Pronto → Entregue
- [ ] 3.2.5 Etapa atual destacada visualmente
- [ ] 3.2.6 Atualização automática do status em tempo real (polling a cada 3 segundos)
- [ ] 3.2.7 Design mobile-first e responsivo
- [ ] 3.2.8 Frases criativas por status:
  - Fila: "Seu pedido está na fila! Logo começaremos a preparar 🍽️"
  - Preparando: "Estamos preparando seu pedido com carinho 👨‍🍳"
  - Pronto: "Seu pedido está pronto! Pode retirar no balcão ✅"
  - Entregue: "Pedido entregue! Bom apetite 🎉"

### 3.3 Tela Painel de Fila (TV/Monitor)
**Como** gerente ou cliente na loja  
**Quero** visualizar todos os pedidos em um painel grande  
**Para que** todos possam acompanhar o status dos pedidos

**Critérios de Aceitação:**
- [ ] 3.3.1 Layout em 3 colunas: "Fila" | "Em Preparo" | "Prontos"
- [ ] 3.3.2 Cada coluna exibe cards com: Nome do cliente e Número do pedido (senha)
- [ ] 3.3.3 Exibe tempo médio de preparo no topo da tela
- [ ] 3.3.4 Atualização automática em tempo real (polling a cada 2 segundos)
- [ ] 3.3.5 Design otimizado para telas grandes (TV/Monitor)
- [ ] 3.3.6 Cores distintas por coluna para fácil identificação
- [ ] 3.3.7 Fonte grande e legível à distância
- [ ] 3.3.8 Animação suave ao mover pedidos entre colunas
- [ ] 3.3.9 Pedidos "Entregues" não aparecem no painel
- [ ] 3.3.10 Limite de 10 pedidos por coluna (scroll automático se necessário)

## 4. Requisitos Técnicos

### 4.1 Backend
- [ ] 4.1.1 Endpoint para buscar pedidos da cozinha (filtrados por status)
- [ ] 4.1.2 Endpoint para buscar pedido específico via QR Code (UUID)
- [ ] 4.1.3 Endpoint para buscar todos os pedidos ativos para o painel
- [ ] 4.1.4 Endpoint para avançar status do pedido
- [ ] 4.1.5 Cálculo de tempo médio de preparo (média dos últimos 20 pedidos concluídos)

### 4.2 Frontend
- [ ] 4.2.1 Templates responsivos para mobile (cozinha e acompanhamento)
- [ ] 4.2.2 Template otimizado para telas grandes (painel TV)
- [ ] 4.2.3 JavaScript para polling e atualização em tempo real
- [ ] 4.2.4 Animações CSS para transições suaves
- [ ] 4.2.5 Cronômetros JavaScript com mudança de cor dinâmica

### 4.3 Rotas
- [ ] 4.3.1 `/cozinha/` - Dashboard da cozinha (mobile)
- [ ] 4.3.2 `/acompanhamento/<uuid>/` - Acompanhamento via QR Code
- [ ] 4.3.3 `/painel-status/` - Painel de fila para TV/Monitor

## 5. Restrições e Considerações

### 5.1 Performance
- Polling deve ser eficiente para não sobrecarregar o servidor
- Animações devem ser leves e não causar lag

### 5.2 Usabilidade
- Interfaces devem ser intuitivas e não requerer treinamento
- Fontes e cores devem ter bom contraste para legibilidade

### 5.3 Compatibilidade
- Suporte a navegadores modernos (Chrome, Firefox, Safari, Edge)
- Responsividade para diferentes tamanhos de tela

## 6. Fora do Escopo (Nesta Versão)
- Notificações push
- Som/alerta quando pedido fica pronto
- Impressão automática de comandas
- Integração com sistema de pagamento
- Histórico de pedidos antigos

## 7. Dependências
- Sistema de pedidos já implementado (modelo Pedido)
- Campo QR Code (UUID) já existe no modelo
- Sistema de autenticação funcionando

## 8. Métricas de Sucesso
- Tempo médio para processar pedido na cozinha reduzido em 30%
- 90% dos clientes conseguem acompanhar pedido via QR Code sem ajuda
- Painel de TV visível e legível a 5 metros de distância
