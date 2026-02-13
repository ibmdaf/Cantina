# Implementation Plan: Redesign de Telas Mobile e TV

## Overview

This implementation plan breaks down the redesign of three critical interfaces into discrete coding tasks. The approach follows a component-by-component strategy, implementing each interface (Kitchen Mobile, Customer Tracking, TV Panel) with its backend endpoints, frontend templates, and tests. Each major component includes property-based tests to validate correctness properties from the design document.

## Tasks

- [ ] 1. Set up URL routing and base structure
  - Create new URL patterns for `/cozinha/`, `/acompanhamento/<uuid>/`, and `/painel-status/`
  - Create placeholder views that return simple responses
  - Verify routes are accessible
  - _Requirements: 4.3.1, 4.3.2, 4.3.3_

- [ ] 2. Implement Kitchen Mobile Dashboard backend
  - [ ] 2.1 Create `cozinha_mobile_dashboard` view
    - Query active orders (status in ['pendente', 'preparando', 'pronto'])
    - Order by `criado_em` ascending
    - Use `select_related` and `prefetch_related` for optimization
    - Return context with orders list
    - _Requirements: 3.1.1, 3.1.7, 4.1.1_
  
  - [ ] 2.2 Create `avancar_status_pedido` API endpoint
    - Accept POST requests with pedido_id
    - Implement status progression logic: pendente → preparando → pronto → entregue
    - Validate user's empresa matches order's empresa
    - Return JSON with success status and new status
    - Handle error cases (invalid ID, already delivered, unauthorized)
    - _Requirements: 3.1.6, 4.1.4_
  
  - [ ]* 2.3 Write property test for order chronological ordering
    - **Property 1: Order List Chronological Ordering**
    - **Validates: Requirements 3.1.1**
  
  - [ ]* 2.4 Write property test for status progression
    - **Property 2: Status Progression Correctness**
    - **Validates: Requirements 3.1.6, 4.1.4**
  
  - [ ]* 2.5 Write property test for delivered orders exclusion
    - **Property 4: Delivered Orders Exclusion**
    - **Validates: Requirements 3.1.7, 3.3.9**
  
  - [ ]* 2.6 Write unit tests for kitchen dashboard
    - Test empty order list
    - Test unauthorized access
    - Test status advancement error cases
    - _Requirements: 3.1.6, 4.1.4_

- [ ] 3. Implement Kitchen Mobile Dashboard frontend
  - [ ] 3.1 Create `mobile_dashboard.html` template
    - Implement mobile-first responsive layout
    - Create order card structure with all required fields
    - Add timer placeholder elements with data attributes
    - Add "Avançar Status" button for each card
    - Apply color palette from design
    - _Requirements: 3.1.2, 3.1.3, 3.1.8_
  
  - [ ] 3.2 Implement timer JavaScript logic
    - Calculate elapsed time from `criado_em` timestamp
    - Update timer display every second
    - Apply color classes based on elapsed time (green: 0-14min, yellow: 15-29min, red: 30+min)
    - Handle edge cases (future timestamps, null values)
    - _Requirements: 3.1.4, 4.2.5_
  
  - [ ] 3.3 Implement status advancement JavaScript
    - Add click handler for "Avançar Status" buttons
    - Send POST request to advancement endpoint
    - Update UI on success (remove card or update status)
    - Show error message on failure
    - _Requirements: 3.1.6_
  
  - [ ]* 3.4 Write property test for timer color classification
    - **Property 3: Timer Color Classification**
    - **Validates: Requirements 3.1.4, 4.2.5**
  
  - [ ]* 3.5 Write property test for order card information completeness
    - **Property 5: Order Card Information Completeness**
    - **Validates: Requirements 3.1.2, 3.2.2, 3.3.2**
  
  - [ ]* 3.6 Write property test for button presence
    - **Property 12: Kitchen Dashboard Button Presence**
    - **Validates: Requirements 3.1.3**
  
  - [ ]* 3.7 Write unit tests for kitchen frontend
    - Test timer calculation with specific timestamps
    - Test button click handling
    - Test error message display
    - _Requirements: 3.1.4, 3.1.6_

- [ ] 4. Checkpoint - Test kitchen dashboard end-to-end
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement Customer Tracking backend
  - [ ] 5.1 Create `acompanhar_pedido_mobile` view
    - Accept QR code UUID parameter
    - Query order by qr_code field
    - Return 404 with friendly message if not found
    - Return context with order and qr_code
    - _Requirements: 3.2.1, 4.1.2_
  
  - [ ] 5.2 Create `status_pedido_polling` API endpoint
    - Accept QR code UUID parameter
    - Return JSON with order status, number, customer name, and creative phrase
    - Implement status-to-phrase mapping dictionary
    - Return 404 if QR code not found
    - _Requirements: 3.2.3, 3.2.8_
  
  - [ ]* 5.3 Write property test for QR code UUID lookup
    - **Property 6: QR Code UUID Lookup**
    - **Validates: Requirements 3.2.1, 4.1.2**
  
  - [ ]* 5.4 Write property test for status phrase mapping
    - **Property 7: Status Phrase Mapping Completeness**
    - **Validates: Requirements 3.2.3**
  
  - [ ]* 5.5 Write unit tests for tracking backend
    - Test invalid UUID returns 404
    - Test exact phrases match requirements (3.2.8)
    - Test JSON response structure
    - _Requirements: 3.2.1, 3.2.3, 3.2.8_

- [ ] 6. Implement Customer Tracking frontend
  - [ ] 6.1 Create `mobile_tracking.html` template
    - Implement mobile-first responsive layout
    - Display order number prominently
    - Display customer name
    - Add status phrase container
    - Create 4-step progress bar structure
    - Apply color palette from design
    - _Requirements: 3.2.2, 3.2.4, 3.2.7_
  
  - [ ] 6.2 Implement progress bar JavaScript
    - Function to update active steps based on current status
    - Apply 'active' class to current and previous steps
    - Remove 'active' class from future steps
    - _Requirements: 3.2.5_
  
  - [ ] 6.3 Implement polling JavaScript
    - Poll status endpoint every 3 seconds
    - Update status phrase on response
    - Update progress bar on status change
    - Implement error handling with retry logic
    - _Requirements: 3.2.6, 4.2.3_
  
  - [ ]* 6.4 Write property test for progress bar step activation
    - **Property 8: Progress Bar Step Activation**
    - **Validates: Requirements 3.2.5**
  
  - [ ]* 6.5 Write property test for progress bar structure
    - **Property 13: Progress Bar Structure Completeness**
    - **Validates: Requirements 3.2.4**
  
  - [ ]* 6.6 Write unit tests for tracking frontend
    - Test polling interval is 3 seconds
    - Test progress bar updates correctly
    - Test error handling displays warning
    - _Requirements: 3.2.6_

- [ ] 7. Checkpoint - Test customer tracking end-to-end
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 8. Implement TV Panel Dashboard backend
  - [ ] 8.1 Create `painel_tv_dashboard` view
    - Accept optional empresa_id query parameter
    - Default to first empresa if not provided
    - Return context with empresa
    - _Requirements: 3.3.1_
  
  - [ ] 8.2 Create `painel_pedidos_api` endpoint
    - Query orders grouped by status (pendente, preparando, pronto)
    - Limit each group to 10 orders maximum
    - Order each group by criado_em ascending
    - Calculate average preparation time from last 20 completed orders
    - Return JSON with fila, preparando, prontos arrays and tempo_medio
    - Exclude 'entregue' orders from results
    - _Requirements: 3.3.2, 3.3.9, 3.3.10, 4.1.3, 4.1.5_
  
  - [ ]* 8.3 Write property test for column limit
    - **Property 9: TV Panel Column Limit**
    - **Validates: Requirements 3.3.10**
  
  - [ ]* 8.4 Write property test for average time calculation
    - **Property 10: Average Preparation Time Calculation**
    - **Validates: Requirements 4.1.5**
  
  - [ ]* 8.5 Write property test for panel API response structure
    - **Property 11: Panel API Response Structure**
    - **Validates: Requirements 4.1.3**
  
  - [ ]* 8.6 Write unit tests for panel backend
    - Test with exactly 10 orders per column
    - Test with 11 orders (verify limit)
    - Test average time with 0 completed orders
    - Test empresa_id parameter handling
    - _Requirements: 3.3.10, 4.1.5_

- [ ] 9. Implement TV Panel Dashboard frontend
  - [ ] 9.1 Create `tv_dashboard.html` template
    - Implement 3-column layout (Fila, Em Preparo, Prontos)
    - Add header with tempo médio display
    - Create column containers with distinct CSS classes
    - Apply large fonts for distance readability
    - Apply color palette with distinct colors per column
    - _Requirements: 3.3.1, 3.3.3, 3.3.6, 3.3.7_
  
  - [ ] 9.2 Implement panel update JavaScript
    - Function to update each column with order cards
    - Create card HTML with order number and customer name
    - Implement smooth opacity transition on updates
    - _Requirements: 3.3.2, 3.3.8_
  
  - [ ] 9.3 Implement polling JavaScript
    - Poll panel API every 2 seconds
    - Update all three columns on response
    - Update tempo médio display
    - Implement error handling with retry logic
    - _Requirements: 3.3.4, 4.2.3_
  
  - [ ]* 9.4 Write unit tests for panel frontend
    - Test 3-column structure exists
    - Test tempo médio element exists
    - Test distinct column CSS classes
    - Test polling interval is 2 seconds
    - _Requirements: 3.3.1, 3.3.3, 3.3.6, 3.3.4_

- [ ] 10. Checkpoint - Test TV panel end-to-end
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Create comprehensive CSS styling
  - [ ] 11.1 Create `cozinha_mobile.css`
    - Mobile-first responsive styles
    - Card layout with proper spacing
    - Timer color classes (green, yellow, red)
    - Button styling with #F4A23A color
    - Dark theme with specified color palette
    - _Requirements: 3.1.4, 3.1.5, 3.1.8_
  
  - [ ] 11.2 Create `tracking_mobile.css`
    - Mobile-first responsive styles
    - Progress bar styling with 4 steps
    - Active step highlighting
    - Status phrase styling
    - Dark theme with specified color palette
    - _Requirements: 3.2.4, 3.2.5, 3.2.7_
  
  - [ ] 11.3 Create `painel_tv.css`
    - Large screen optimized layout
    - 3-column grid with equal widths
    - Large fonts for distance readability
    - Distinct colors per column
    - Smooth transition animations
    - Dark theme with specified color palette
    - _Requirements: 3.3.5, 3.3.6, 3.3.7, 3.3.8_

- [ ] 12. Integration and final wiring
  - [ ] 12.1 Update main URLs configuration
    - Include all three app URL patterns
    - Verify no URL conflicts
    - _Requirements: 4.3.1, 4.3.2, 4.3.3_
  
  - [ ] 12.2 Add navigation links
    - Add link to kitchen dashboard from main menu
    - Add link to TV panel from main menu
    - Ensure QR codes on receipts link to tracking page
    - _Requirements: 3.2.1_
  
  - [ ]* 12.3 Write integration tests
    - Test complete flow: create order → view in kitchen → advance status → check tracking → verify panel
    - Test polling updates across all interfaces
    - Test concurrent access with multiple users
    - _Requirements: 3.1.6, 3.2.6, 3.3.4_

- [ ] 13. Final checkpoint - Complete system validation
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at major milestones
- Property tests validate universal correctness properties with minimum 100 iterations
- Unit tests validate specific examples, edge cases, and error conditions
- All polling intervals must match requirements: 3 seconds for tracking, 2 seconds for panel
- Color palette must be consistently applied across all interfaces
- Mobile-first approach ensures responsive design works on all devices
