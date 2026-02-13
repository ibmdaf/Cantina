# Design Document: Redesign de Telas Mobile e TV

## Overview

This design implements three specialized interfaces for the cantina order management system, each optimized for specific devices and use cases:

1. **Tela Cozinha (Mobile)**: A mobile-first vertical list interface for kitchen staff to process orders efficiently
2. **Tela Acompanhamento (Mobile via QR Code)**: A customer-facing order tracking interface accessible via QR code
3. **Tela Painel de Fila (TV/Monitor)**: A large-screen dashboard displaying all active orders in a three-column layout

The design leverages the existing Django backend with SQLite database and the Pedido model that already includes QR code UUID fields. The solution emphasizes real-time updates through polling, responsive design, and visual clarity appropriate to each context.

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Django Backend                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Views      │  │   Models     │  │   URLs       │     │
│  │              │  │              │  │              │     │
│  │ - cozinha    │  │ - Pedido     │  │ - /cozinha/  │     │
│  │ - acomp.     │  │ - ItemPedido │  │ - /acomp/    │     │
│  │ - painel     │  │ - Produto    │  │ - /painel/   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/JSON
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  Tela Cozinha │   │ Tela Acomp.   │   │ Painel TV     │
│   (Mobile)    │   │ (Mobile/QR)   │   │ (Monitor)     │
│               │   │               │   │               │
│ - List View   │   │ - Progress    │   │ - 3 Columns   │
│ - Timer       │   │ - Polling     │   │ - Real-time   │
│ - Status Btn  │   │ - Status      │   │ - Auto-scroll │
└───────────────┘   └───────────────┘   └───────────────┘
```

### Technology Stack

- **Backend**: Django 4.x with SQLite
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Real-time Updates**: HTTP Polling (no WebSockets required)
- **Styling**: Custom CSS with mobile-first approach
- **Color Palette**: 
  - Background: #0B0B0B
  - Header: #1A1A1A
  - Cards: #202020
  - Borders: #2E2E2E
  - Text Primary: #FFFFFF
  - Text Secondary: #BDBDBD
  - Buttons: #F4A23A

### Data Flow

1. **Order Creation**: Orders are created through existing autoatendimento/caixa systems
2. **Status Updates**: Kitchen staff advances order status through mobile interface
3. **Real-time Sync**: All interfaces poll backend at regular intervals (2-3 seconds)
4. **Status Progression**: Fila → Preparando → Pronto → Entregue

## Components and Interfaces

### 1. Tela Cozinha (Mobile Interface)

#### Purpose
Provide kitchen staff with a streamlined mobile interface to view and process orders sequentially.

#### URL Route
```
/cozinha/
```

#### View Component
```python
@login_required
def cozinha_mobile_dashboard(request):
    """
    Returns mobile-optimized kitchen dashboard with active orders
    """
    empresa = request.user.empresa
    
    # Get orders that are not yet delivered
    pedidos_ativos = Pedido.objects.filter(
        empresa=empresa,
        status__in=['pendente', 'preparando', 'pronto']
    ).order_by('criado_em').select_related('empresa').prefetch_related('itens__produto')
    
    context = {
        'pedidos': pedidos_ativos,
    }
    return render(request, 'cozinha/mobile_dashboard.html', context)
```

#### API Endpoint for Status Update
```python
@login_required
def avancar_status_pedido(request, pedido_id):
    """
    Advances order to next status in the workflow
    """
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id, empresa=request.user.empresa)
        
        # Status progression logic
        status_flow = {
            'pendente': 'preparando',
            'preparando': 'pronto',
            'pronto': 'entregue'
        }
        
        if pedido.status in status_flow:
            pedido.status = status_flow[pedido.status]
            pedido.save()
            
            return JsonResponse({
                'success': True,
                'novo_status': pedido.status,
                'status_display': pedido.get_status_display()
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
```

#### Frontend Structure
```html
<!-- mobile_dashboard.html -->
<div class="cozinha-mobile-container">
    <header class="mobile-header">
        <h1>Pedidos Ativos</h1>
        <span class="pedidos-count">{{ pedidos.count }}</span>
    </header>
    
    <div class="pedidos-list">
        {% for pedido in pedidos %}
        <div class="pedido-card" data-pedido-id="{{ pedido.id }}">
            <div class="pedido-header">
                <span class="numero-pedido">#{{ pedido.numero_pedido }}</span>
                <span class="timer" data-criado="{{ pedido.criado_em|date:'c' }}">00:00</span>
            </div>
            
            <div class="cliente-info">
                <strong>{{ pedido.cliente_nome|default:"Cliente" }}</strong>
            </div>
            
            <div class="itens-lista">
                {% for item in pedido.itens.all %}
                <div class="item">
                    <span class="quantidade">{{ item.quantidade }}x</span>
                    <span class="produto">{{ item.produto.nome }}</span>
                </div>
                {% if item.observacoes %}
                <div class="observacao">{{ item.observacoes }}</div>
                {% endif %}
                {% endfor %}
            </div>
            
            {% if pedido.observacoes %}
            <div class="pedido-observacoes">
                <strong>Obs:</strong> {{ pedido.observacoes }}
            </div>
            {% endif %}
            
            <button class="btn-avancar-status" data-pedido-id="{{ pedido.id }}">
                Avançar Status
            </button>
        </div>
        {% endfor %}
    </div>
</div>
```

#### Timer Logic
```javascript
// Timer updates every second
function initializeTimers() {
    const timers = document.querySelectorAll('.timer');
    
    setInterval(() => {
        timers.forEach(timer => {
            const criadoEm = new Date(timer.dataset.criado);
            const agora = new Date();
            const diffMs = agora - criadoEm;
            const diffMins = Math.floor(diffMs / 60000);
            const diffSecs = Math.floor((diffMs % 60000) / 1000);
            
            timer.textContent = `${String(diffMins).padStart(2, '0')}:${String(diffSecs).padStart(2, '0')}`;
            
            // Color coding
            if (diffMins >= 30) {
                timer.className = 'timer timer-red';
            } else if (diffMins >= 15) {
                timer.className = 'timer timer-yellow';
            } else {
                timer.className = 'timer timer-green';
            }
        });
    }, 1000);
}
```

### 2. Tela Acompanhamento (Customer Tracking Interface)

#### Purpose
Allow customers to track their order status in real-time using a QR code.

#### URL Route
```
/acompanhamento/<uuid:qr_code>/
```

#### View Component
```python
def acompanhar_pedido_mobile(request, qr_code):
    """
    Customer-facing order tracking page
    """
    pedido = get_object_or_404(Pedido, qr_code=qr_code)
    
    context = {
        'pedido': pedido,
        'qr_code': qr_code,
    }
    return render(request, 'acompanhamento/mobile_tracking.html', context)
```

#### API Endpoint for Polling
```python
def status_pedido_polling(request, qr_code):
    """
    Returns current order status for polling
    """
    pedido = get_object_or_404(Pedido, qr_code=qr_code)
    
    # Status phrases
    frases_status = {
        'pendente': 'Seu pedido está na fila! Logo começaremos a preparar 🍽️',
        'preparando': 'Estamos preparando seu pedido com carinho 👨‍🍳',
        'pronto': 'Seu pedido está pronto! Pode retirar no balcão ✅',
        'entregue': 'Pedido entregue! Bom apetite 🎉'
    }
    
    return JsonResponse({
        'status': pedido.status,
        'numero_pedido': pedido.numero_pedido,
        'cliente_nome': pedido.cliente_nome,
        'frase': frases_status.get(pedido.status, ''),
        'atualizado_em': pedido.atualizado_em.isoformat()
    })
```

#### Frontend Structure
```html
<!-- mobile_tracking.html -->
<div class="tracking-container">
    <header class="tracking-header">
        <h1>Acompanhe seu Pedido</h1>
    </header>
    
    <div class="pedido-info">
        <div class="numero-grande">#<span id="numero-pedido">{{ pedido.numero_pedido }}</span></div>
        <div class="cliente-nome">{{ pedido.cliente_nome|default:"Cliente" }}</div>
    </div>
    
    <div class="status-frase" id="status-frase">
        <!-- Updated via JavaScript -->
    </div>
    
    <div class="progress-bar">
        <div class="progress-step" data-status="pendente">
            <div class="step-circle"></div>
            <div class="step-label">Fila</div>
        </div>
        <div class="progress-line"></div>
        <div class="progress-step" data-status="preparando">
            <div class="step-circle"></div>
            <div class="step-label">Preparando</div>
        </div>
        <div class="progress-line"></div>
        <div class="progress-step" data-status="pronto">
            <div class="step-circle"></div>
            <div class="step-label">Pronto</div>
        </div>
        <div class="progress-line"></div>
        <div class="progress-step" data-status="entregue">
            <div class="step-circle"></div>
            <div class="step-label">Entregue</div>
        </div>
    </div>
</div>
```

#### Polling Logic
```javascript
// Poll every 3 seconds
const qrCode = '{{ qr_code }}';

function atualizarStatus() {
    fetch(`/api/acompanhamento/${qrCode}/status/`)
        .then(response => response.json())
        .then(data => {
            // Update status phrase
            document.getElementById('status-frase').textContent = data.frase;
            
            // Update progress bar
            atualizarProgressBar(data.status);
        })
        .catch(error => console.error('Erro ao atualizar status:', error));
}

function atualizarProgressBar(statusAtual) {
    const steps = document.querySelectorAll('.progress-step');
    const statusOrder = ['pendente', 'preparando', 'pronto', 'entregue'];
    const currentIndex = statusOrder.indexOf(statusAtual);
    
    steps.forEach((step, index) => {
        if (index <= currentIndex) {
            step.classList.add('active');
        } else {
            step.classList.remove('active');
        }
    });
}

// Start polling
setInterval(atualizarStatus, 3000);
atualizarStatus(); // Initial call
```

### 3. Tela Painel de Fila (TV/Monitor Dashboard)

#### Purpose
Display all active orders on a large screen for public viewing in the establishment.

#### URL Route
```
/painel-status/
```

#### View Component
```python
def painel_tv_dashboard(request):
    """
    TV/Monitor dashboard showing all active orders
    """
    # Get empresa from query param or default to first empresa
    empresa_id = request.GET.get('empresa_id')
    if empresa_id:
        empresa = get_object_or_404(Empresa, id=empresa_id)
    else:
        empresa = Empresa.objects.first()
    
    context = {
        'empresa': empresa,
    }
    return render(request, 'painel/tv_dashboard.html', context)
```

#### API Endpoint for Polling
```python
def painel_pedidos_api(request):
    """
    Returns all active orders grouped by status
    """
    empresa_id = request.GET.get('empresa_id')
    empresa = get_object_or_404(Empresa, id=empresa_id) if empresa_id else Empresa.objects.first()
    
    # Get orders by status (limit 10 per column)
    pedidos_fila = Pedido.objects.filter(
        empresa=empresa,
        status='pendente'
    ).order_by('criado_em')[:10]
    
    pedidos_preparando = Pedido.objects.filter(
        empresa=empresa,
        status='preparando'
    ).order_by('criado_em')[:10]
    
    pedidos_prontos = Pedido.objects.filter(
        empresa=empresa,
        status='pronto'
    ).order_by('criado_em')[:10]
    
    # Calculate average prep time (last 20 completed orders)
    pedidos_concluidos = Pedido.objects.filter(
        empresa=empresa,
        status='entregue'
    ).order_by('-atualizado_em')[:20]
    
    tempo_medio = 0
    if pedidos_concluidos:
        total_tempo = sum([
            (p.atualizado_em - p.criado_em).total_seconds() / 60
            for p in pedidos_concluidos
        ])
        tempo_medio = int(total_tempo / len(pedidos_concluidos))
    
    return JsonResponse({
        'fila': [{'numero': p.numero_pedido, 'cliente': p.cliente_nome or 'Cliente'} for p in pedidos_fila],
        'preparando': [{'numero': p.numero_pedido, 'cliente': p.cliente_nome or 'Cliente'} for p in pedidos_preparando],
        'prontos': [{'numero': p.numero_pedido, 'cliente': p.cliente_nome or 'Cliente'} for p in pedidos_prontos],
        'tempo_medio': tempo_medio
    })
```

#### Frontend Structure
```html
<!-- tv_dashboard.html -->
<div class="painel-tv-container">
    <header class="painel-header">
        <h1>Painel de Pedidos</h1>
        <div class="tempo-medio">
            Tempo Médio: <span id="tempo-medio">--</span> min
        </div>
    </header>
    
    <div class="colunas-container">
        <div class="coluna coluna-fila">
            <div class="coluna-header">Fila</div>
            <div class="coluna-content" id="coluna-fila">
                <!-- Populated via JavaScript -->
            </div>
        </div>
        
        <div class="coluna coluna-preparando">
            <div class="coluna-header">Em Preparo</div>
            <div class="coluna-content" id="coluna-preparando">
                <!-- Populated via JavaScript -->
            </div>
        </div>
        
        <div class="coluna coluna-prontos">
            <div class="coluna-header">Prontos</div>
            <div class="coluna-content" id="coluna-prontos">
                <!-- Populated via JavaScript -->
            </div>
        </div>
    </div>
</div>
```

#### Polling and Update Logic
```javascript
// Poll every 2 seconds
const empresaId = '{{ empresa.id }}';

function atualizarPainel() {
    fetch(`/api/painel/pedidos/?empresa_id=${empresaId}`)
        .then(response => response.json())
        .then(data => {
            atualizarColuna('fila', data.fila);
            atualizarColuna('preparando', data.preparando);
            atualizarColuna('prontos', data.prontos);
            
            document.getElementById('tempo-medio').textContent = data.tempo_medio;
        })
        .catch(error => console.error('Erro ao atualizar painel:', error));
}

function atualizarColuna(colunaId, pedidos) {
    const coluna = document.getElementById(`coluna-${colunaId}`);
    
    // Create HTML for pedidos
    const html = pedidos.map(p => `
        <div class="pedido-card-tv">
            <div class="numero-tv">#${p.numero}</div>
            <div class="cliente-tv">${p.cliente}</div>
        </div>
    `).join('');
    
    // Smooth transition
    if (coluna.innerHTML !== html) {
        coluna.style.opacity = '0.5';
        setTimeout(() => {
            coluna.innerHTML = html;
            coluna.style.opacity = '1';
        }, 200);
    }
}

// Start polling
setInterval(atualizarPainel, 2000);
atualizarPainel(); // Initial call
```

## Data Models

The existing Pedido model already contains all necessary fields:

```python
class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),      # Maps to "Fila"
        ('preparando', 'Preparando'),  # Maps to "Em Preparo"
        ('pronto', 'Pronto'),          # Maps to "Prontos"
        ('entregue', 'Entregue'),      # Removed from displays
        ('cancelado', 'Cancelado'),    # Not used in this feature
    ]
    
    empresa = ForeignKey(Empresa)
    numero_pedido = CharField(max_length=10, unique=True)
    qr_code = UUIDField(default=uuid.uuid4, unique=True)  # Used for tracking
    status = CharField(choices=STATUS_CHOICES)
    cliente_nome = CharField(max_length=200)
    observacoes = TextField(blank=True)
    criado_em = DateTimeField(auto_now_add=True)  # Used for timer calculation
    atualizado_em = DateTimeField(auto_now=True)  # Used for average time
    
    # Related: itens (ItemPedido)
```

### Status Mapping

The requirements use different terminology than the model:

| Requirements Term | Model Status | Display Context |
|------------------|--------------|-----------------|
| Fila | pendente | All interfaces |
| Preparando | preparando | All interfaces |
| Pronto | pronto | All interfaces |
| Entregue | entregue | Hidden from displays |

### No Schema Changes Required

The existing schema fully supports all requirements:
- QR code field exists for customer tracking
- Status field supports the workflow
- Timestamps enable timer and average calculation
- Related ItemPedido provides order details


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Order List Chronological Ordering

*For any* set of orders retrieved for the kitchen dashboard, the orders should be sorted by creation time in ascending order (oldest first).

**Validates: Requirements 3.1.1**

### Property 2: Status Progression Correctness

*For any* order with status in ['pendente', 'preparando', 'pronto'], advancing the status should transition it to the next status in the sequence: pendente → preparando → pronto → entregue.

**Validates: Requirements 3.1.6, 4.1.4**

### Property 3: Timer Color Classification

*For any* elapsed time value, the timer color class should be: 'timer-green' for 0-14 minutes, 'timer-yellow' for 15-29 minutes, and 'timer-red' for 30+ minutes.

**Validates: Requirements 3.1.4, 4.2.5**

### Property 4: Delivered Orders Exclusion

*For any* query for active orders (kitchen dashboard or TV panel), orders with status 'entregue' should not appear in the results.

**Validates: Requirements 3.1.7, 3.3.9**

### Property 5: Order Card Information Completeness

*For any* order rendered as a card (in any interface), the rendered HTML should contain the customer name (or default "Cliente"), order number, and list of items.

**Validates: Requirements 3.1.2, 3.2.2, 3.3.2**

### Property 6: QR Code UUID Lookup

*For any* valid QR code UUID that exists in the database, the tracking endpoint should return the corresponding order data with status 200.

**Validates: Requirements 3.2.1, 4.1.2**

### Property 7: Status Phrase Mapping Completeness

*For any* order status in ['pendente', 'preparando', 'pronto', 'entregue'], there should exist a corresponding creative phrase in the status phrase mapping.

**Validates: Requirements 3.2.3**

### Property 8: Progress Bar Step Activation

*For any* order with a given status, when rendering the progress bar, all steps up to and including the current status should have the 'active' class, and subsequent steps should not.

**Validates: Requirements 3.2.5**

### Property 9: TV Panel Column Limit

*For any* status column in the TV panel API response, the number of orders returned should not exceed 10.

**Validates: Requirements 3.3.10**

### Property 10: Average Preparation Time Calculation

*For any* set of completed orders, the calculated average preparation time should equal the mean of the time differences between atualizado_em and criado_em for those orders.

**Validates: Requirements 4.1.5**

### Property 11: Panel API Response Structure

*For any* request to the panel API endpoint, the response should contain exactly three arrays ('fila', 'preparando', 'prontos') and a 'tempo_medio' integer value.

**Validates: Requirements 4.1.3**

### Property 12: Kitchen Dashboard Button Presence

*For any* order card rendered in the kitchen dashboard, the HTML should contain a button element with class 'btn-avancar-status'.

**Validates: Requirements 3.1.3**

### Property 13: Progress Bar Structure Completeness

*For any* rendered tracking page, the progress bar should contain exactly 4 step elements with data-status attributes: 'pendente', 'preparando', 'pronto', 'entregue'.

**Validates: Requirements 3.2.4**

## Error Handling

### Invalid QR Code Handling

When a customer accesses the tracking page with an invalid or non-existent QR code UUID:
- Return HTTP 404 with a user-friendly error page
- Log the invalid access attempt for security monitoring
- Display message: "Pedido não encontrado. Verifique o QR Code."

### Status Advancement Errors

When attempting to advance order status:
- **Invalid Order ID**: Return 404 JSON response
- **Order Already Delivered**: Return 400 with message "Pedido já foi entregue"
- **Unauthorized Access**: Return 403 if user's empresa doesn't match order's empresa
- **Invalid Status Transition**: Return 400 if status is 'entregue' or 'cancelado'

### Polling Failures

When frontend polling encounters errors:
- **Network Error**: Retry after 5 seconds (exponential backoff)
- **Server Error (5xx)**: Display warning banner "Problemas de conexão. Tentando reconectar..."
- **Timeout**: Retry immediately once, then fall back to 5-second interval
- **Maximum Retries**: After 5 consecutive failures, display "Sem conexão. Recarregue a página."

### Database Query Errors

When querying orders:
- **Empty Result Set**: Return empty array, not error
- **Database Connection Error**: Log error, return 503 Service Unavailable
- **Query Timeout**: Log slow query, return cached data if available

### Timer Calculation Edge Cases

When calculating elapsed time:
- **Future Timestamp**: Treat as 0 minutes (clock skew protection)
- **Null criado_em**: Skip timer display, log data integrity error
- **Very Old Orders (>24h)**: Display "24:00+" instead of calculating exact time

## Testing Strategy

### Dual Testing Approach

This feature requires both unit tests and property-based tests to ensure comprehensive coverage:

- **Unit tests**: Verify specific examples, edge cases, URL routing, and error conditions
- **Property tests**: Verify universal properties across all inputs using randomized data

Both testing approaches are complementary and necessary. Unit tests catch concrete bugs in specific scenarios, while property tests verify general correctness across a wide range of inputs.

### Property-Based Testing Configuration

**Library Selection**: Use **Hypothesis** for Python/Django property-based testing

**Test Configuration**:
- Minimum 100 iterations per property test (due to randomization)
- Each property test must reference its design document property
- Tag format: `# Feature: redesign-telas-mobile-tv, Property {number}: {property_text}`

**Property Test Implementation**:
- Each correctness property listed above must be implemented as a single property-based test
- Use Hypothesis strategies to generate random orders, timestamps, and status values
- Tests should be placed in `tests/test_properties.py` within each Django app

### Unit Testing Focus

Unit tests should focus on:
- **Specific Examples**: Test exact status phrases match requirements (3.2.8)
- **URL Routing**: Verify all three routes are accessible (4.3.1, 4.3.2, 4.3.3)
- **Edge Cases**: Empty order lists, single order, exactly 10 orders, 11 orders
- **Error Conditions**: Invalid UUIDs, unauthorized access, invalid status transitions
- **Integration Points**: Template rendering, JSON serialization, database queries
- **Polling Mechanism**: Verify polling functions are called at correct intervals (3.2.6, 3.3.4)
- **UI Structure**: Verify 3-column layout exists (3.3.1), tempo médio element exists (3.3.3)
- **CSS Classes**: Verify distinct column classes exist (3.3.6)

### Test Organization

```
cozinha/
  tests/
    test_views.py          # Unit tests for views
    test_properties.py     # Property-based tests
    
acompanhamento/
  tests/
    test_views.py          # Unit tests for views
    test_properties.py     # Property-based tests
    
painel/
  tests/
    test_views.py          # Unit tests for views
    test_properties.py     # Property-based tests
```

### Example Property Test Structure

```python
from hypothesis import given, strategies as st
from hypothesis.extra.django import TestCase
from caixa.models import Pedido

class TestOrderProperties(TestCase):
    
    @given(st.lists(st.datetimes()))
    def test_property_1_chronological_ordering(self, timestamps):
        """
        Feature: redesign-telas-mobile-tv, Property 1: Order List Chronological Ordering
        
        For any set of orders, they should be sorted by creation time ascending.
        """
        # Create orders with given timestamps
        # Query kitchen dashboard
        # Assert orders are sorted by criado_em
        pass
```

### Coverage Goals

- **Line Coverage**: Minimum 85% for all new view code
- **Branch Coverage**: Minimum 80% for conditional logic
- **Property Coverage**: 100% of correctness properties must have corresponding tests
- **Integration Coverage**: All three interfaces must have end-to-end tests

### Performance Testing

While not part of automated testing, manual performance validation should verify:
- Polling doesn't cause server overload with 10+ concurrent clients
- Timer updates don't cause UI lag on mobile devices
- TV panel updates smoothly with 30 active orders
- Average time calculation completes in <100ms

