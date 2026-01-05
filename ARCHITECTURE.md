# System Architecture

Complete architecture documentation for the Bajaj Broking Trading Platform.

---

## Table of Contents

- [Overview](#overview)
- [System Architecture Diagram](#system-architecture-diagram)
- [Component Architecture](#component-architecture)
- [Data Flow](#data-flow)
- [Order Execution Flow](#order-execution-flow)
- [Technology Stack](#technology-stack)
- [Design Patterns](#design-patterns)
- [Scalability Considerations](#scalability-considerations)

---

## Overview

The Bajaj Broking Trading Platform is a full-stack application consisting of:

1. **Backend API**: FastAPI-based REST API with WebSocket support
2. **Frontend**: React single-page application
3. **Order Matching Engine**: Background service for limit order matching
4. **Real-time Communication**: WebSocket broadcasting for trade events
5. **Data Storage**: In-memory data structures (for demonstration)

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                │
│                                                                     │
│  ┌──────────────────┐         ┌──────────────────┐                │
│  │  React Frontend  │         │  Python SDK      │                │
│  │  (Browser)       │         │  (CLI/Apps)      │                │
│  └────────┬─────────┘         └────────┬─────────┘                │
│           │                              │                           │
│           │ HTTP/WebSocket              │ HTTP                     │
└───────────┼──────────────────────────────┼───────────────────────────┘
            │                              │
            │                              │
┌───────────▼──────────────────────────────▼───────────────────────────┐
│                      API GATEWAY LAYER                                │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                    FastAPI Application                         │ │
│  │  ┌────────────────────────────────────────────────────────┐  │ │
│  │  │  CORS Middleware                                        │  │ │
│  │  │  Error Handlers                                        │  │ │
│  │  │  Authentication Middleware                             │  │ │
│  │  └────────────────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────────────┘ │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────┐
│                        API ROUTER LAYER                              │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │ Instruments  │  │   Orders     │  │  Portfolio   │            │
│  │   Router     │  │   Router     │  │   Router     │            │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘            │
│         │                 │                 │                      │
│  ┌──────▼─────────────────▼─────────────────▼──────┐            │
│  │              Trades Router                        │            │
│  └───────────────────────────────────────────────────┘            │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │              WebSocket Router (/ws)                            │ │
│  └──────────────────────────────────────────────────────────────┘ │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────┐
│                       SERVICE LAYER                                 │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │           Execution Engine                                    │ │
│  │  • Market order execution                                    │ │
│  │  • Limit order validation                                    │ │
│  │  • Trade creation                                            │ │
│  │  • Portfolio updates                                         │ │
│  │  • Thread-safe operations (asyncio.Lock)                    │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │           Limit Order Matcher (Background Task)                │ │
│  │  • Runs every 2 seconds                                      │ │
│  │  • Checks pending limit orders                                │ │
│  │  • Attempts execution if price conditions met                 │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │           WebSocket Broadcaster                               │ │
│  │  • Manages WebSocket connections                             │ │
│  │  • Broadcasts trade events                                    │ │
│  │  • Handles connection cleanup                                │ │
│  └──────────────────────────────────────────────────────────────┘ │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────┐
│                        DATA LAYER                                     │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │              In-Memory Store                                  │ │
│  │                                                              │ │
│  │  • INSTRUMENTS: List[Instrument]                           │ │
│  │  • ORDERS: Dict[order_id, Order]                           │ │
│  │  • TRADES: List[Trade]                                     │ │
│  │  • PORTFOLIO: Dict[user_id, Dict[symbol, Holding]]        │ │
│  └──────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### Backend Components

#### 1. API Layer (`app/api/`)

**Responsibilities:**
- Handle HTTP requests
- Validate input using Pydantic models
- Authenticate requests
- Route to appropriate services
- Format responses

**Components:**
- `instruments.py`: Instrument listing and details
- `orders.py`: Order placement, cancellation, querying
- `portfolio.py`: Portfolio retrieval
- `trades.py`: Trade history
- `ws.py`: WebSocket endpoint

#### 2. Service Layer (`app/services/`)

**Execution Engine (`execution_engine.py`)**
- Executes orders when conditions are met
- Handles MARKET orders (immediate execution at LTP)
- Handles LIMIT orders (execution when price condition met)
- Updates portfolio on execution
- Creates trade records
- Thread-safe operations using asyncio.Lock

**Limit Order Matcher (`limit_matcher.py`)**
- Background task running every 2 seconds
- Scans pending LIMIT orders
- Attempts execution for orders meeting price conditions
- Runs asynchronously in background

**Broadcaster (`broadcaster.py`)**
- Manages WebSocket connections
- Broadcasts trade events to all connected clients
- Handles connection cleanup

#### 3. Data Layer (`app/store/`)

**Memory Store (`memory.py`)**
- In-memory data structures
- Seeded instruments
- Order storage (Dict)
- Trade history (List)
- Portfolio per user (Dict)

#### 4. Core Utilities (`app/core/`)

**Authentication (`auth.py`)**
- API key validation
- User identification
- FastAPI dependency injection

### Frontend Components

#### 1. Components (`frontend/src/components/`)

- **Login.jsx**: Authentication interface
- **Dashboard.jsx**: Main application container with navigation
- **Orders.jsx**: Order placement and management
- **Portfolio.jsx**: Portfolio view with P&L
- **Trades.jsx**: Trade history browser
- **Instruments.jsx**: Instrument catalog

#### 2. Services (`frontend/src/services/`)

- **api.js**: API client with authentication headers

#### 3. Contexts (`frontend/src/contexts/`)

- **AuthContext.jsx**: Authentication state management

#### 4. Hooks (`frontend/src/hooks/`)

- **useWebSocket.js**: WebSocket connection management

---

## Data Flow

### Order Placement Flow

```
1. Client Request
   │
   ▼
2. API Router (orders.py)
   │  • Validate request
   │  • Authenticate user
   │
   ▼
3. Create Order Object
   │  • Generate order_id
   │  • Set state to PLACED
   │  • Store in memory
   │
   ▼
4. Execution Engine
   │  • Check order type (MARKET/LIMIT)
   │  • For MARKET: Execute immediately
   │  • For LIMIT: Check price condition
   │
   ├─► If executable:
   │     • Update order state to EXECUTED
   │     • Create trade record
   │     • Update portfolio
   │     • Broadcast via WebSocket
   │
   └─► If not executable:
         • Order remains PLACED
         • Background matcher will check later
   │
   ▼
5. Return Response
   │  • Order details with current state
```

### Limit Order Matching Flow

```
Background Matcher Loop (every 2 seconds)
   │
   ▼
1. Scan All Orders
   │  • Filter: state == PLACED AND order_style == LIMIT
   │
   ▼
2. For Each Limit Order
   │  • Check current LTP
   │  • Compare with order price
   │
   ├─► BUY LIMIT: price >= LTP → Execute
   │
   └─► SELL LIMIT: price <= LTP → Execute
   │
   ▼
3. If Executable
   │  • Call Execution Engine
   │  • Update order, create trade, update portfolio
   │  • Broadcast event
```

### WebSocket Event Flow

```
Trade Execution
   │
   ▼
1. Execution Engine Completes Trade
   │
   ▼
2. Broadcaster.broadcast()
   │  • Create event message
   │
   ▼
3. For Each Connected Client
   │  • Send JSON message
   │  • Handle errors (disconnect dead clients)
   │
   ▼
4. Client Receives Event
   │  • Update UI (portfolio, trades)
```

---

## Order Execution Flow

### MARKET Order Execution

```
MARKET BUY Order
   │
   ▼
1. Check Instrument LTP
   │  • Get last_traded_price
   │
   ▼
2. Execute Immediately
   │  • Price = LTP
   │  • Quantity = Order quantity
   │
   ▼
3. Update State
   │  • Order: PLACED → EXECUTED
   │  • Create trade record
   │  • Update portfolio (add holding)
   │
   ▼
4. Broadcast Event
```

### LIMIT Order Execution

```
LIMIT Order
   │
   ▼
1. Check Price Condition
   │
   ├─► BUY LIMIT: order.price >= LTP
   │     • Execute at order.price
   │
   └─► SELL LIMIT: order.price <= LTP
         • Execute at order.price
   │
   ▼
2. If Condition Met
   │  • Execute order
   │  • Update state, create trade, update portfolio
   │
   └─► If Condition Not Met
         • Order remains PLACED
         • Background matcher will retry
```

---

## Technology Stack

### Backend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | FastAPI | REST API framework |
| Server | Uvicorn | ASGI server |
| Validation | Pydantic | Data validation and serialization |
| Async | asyncio | Asynchronous operations |
| WebSocket | FastAPI WebSocket | Real-time communication |

### Frontend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | React 19 | UI library |
| Build Tool | Vite | Build tool and dev server |
| Routing | React Router | Client-side routing |
| HTTP Client | Fetch API | API requests |
| WebSocket | WebSocket API | Real-time updates |

---

## Design Patterns

### 1. Dependency Injection

FastAPI uses dependency injection for authentication:

```python
def get_current_user(x_api_key: str = Header(None)):
    # Authentication logic
    return user_id

@router.post("/orders")
async def place_order(..., user_id: str = Depends(get_current_user)):
    # Use authenticated user_id
```

### 2. Singleton Pattern

Broadcaster uses singleton pattern:

```python
broadcaster = Broadcaster()  # Single instance
```

### 3. Repository Pattern (Simplified)

Memory store acts as a simple repository:

```python
# Store
ORDERS: Dict[str, dict] = {}

# Usage
memory.ORDERS[order_id] = order
```

### 4. Observer Pattern

WebSocket broadcaster implements observer pattern:

```python
# Clients subscribe
broadcaster.connect(ws)

# Events broadcast to all
await broadcaster.broadcast(event)
```

---

## Scalability Considerations

### Current Limitations

1. **Single Server**: All components run on one server
2. **In-Memory Storage**: Data lost on restart
3. **No Load Balancing**: Cannot distribute load
4. **Synchronous Matching**: Limit matcher runs sequentially

### Production Improvements

1. **Database**: Replace in-memory store with PostgreSQL/MongoDB
2. **Message Queue**: Use Redis/RabbitMQ for event broadcasting
3. **Horizontal Scaling**: Multiple API instances behind load balancer
4. **Order Book**: Implement proper order book with price-time priority
5. **Caching**: Redis for frequently accessed data
6. **Microservices**: Split into separate services (matching engine, API, etc.)

### Scaling Architecture (Future)

```
                    Load Balancer
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   API Server 1      API Server 2      API Server 3
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                   Message Queue (Redis)
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
  Matching Engine    Database (Postgres)  Cache (Redis)
```

---

## Security Considerations

### Current Implementation

- API key authentication (simple, for demo)
- CORS configuration
- Input validation (Pydantic)
- Error handling

### Production Requirements

- OAuth2/JWT authentication
- HTTPS/TLS encryption
- Rate limiting
- Input sanitization
- SQL injection prevention
- XSS protection
- CSRF tokens
- API key rotation
- Audit logging

---

## Monitoring and Observability

### Current State

- Basic logging
- Error handling

### Production Requirements

- Structured logging (JSON)
- Metrics (Prometheus)
- Distributed tracing (OpenTelemetry)
- Health checks
- Alerting
- Performance monitoring

---

## Conclusion

This architecture is designed for learning and demonstration. For production use, implement the improvements outlined in the scalability and security sections.

For more details, see:
- [README.md](./README.md) - Project overview
- [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) - API reference
- [ASSUMPTIONS.md](./ASSUMPTIONS.md) - Design assumptions

