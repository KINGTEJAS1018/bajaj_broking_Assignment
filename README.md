# Bajaj Broking Trading Platform

> A full-stack trading platform with order matching engine, real-time WebSocket updates, and modern React frontend. Built with FastAPI and React for demonstration of core exchange concepts including order placement, limit/market matching, executions, portfolio tracking, and real-time event broadcasting.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Frontend Usage](#frontend-usage)
- [Sample API Usage](#sample-api-usage)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [Assumptions and Design Decisions](#assumptions-and-design-decisions)
- [Production Considerations](#production-considerations)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This project implements a complete trading platform simulation with:

- **Backend API**: FastAPI-based REST API with WebSocket support
- **Order Matching Engine**: Handles MARKET and LIMIT orders with background matching
- **Real-time Updates**: WebSocket broadcasting for trade executions
- **Frontend**: Modern React application with responsive UI
- **Portfolio Management**: Automatic portfolio tracking with P&L calculations
- **Authentication**: API key-based authentication system

The system is designed for learning, testing, and small-scale demonstrations. It uses an in-memory store for rapid prototyping and deterministic testing.

---

## ✨ Features

### Backend Features
- ✅ REST API for order management (place, cancel, query)
- ✅ Order matching engine (MARKET and LIMIT orders)
- ✅ Background limit order matcher
- ✅ WebSocket real-time event broadcasting
- ✅ Portfolio tracking with automatic P&L calculation
- ✅ Trade history management
- ✅ Instrument management
- ✅ API key authentication
- ✅ CORS support for frontend integration
- ✅ Comprehensive error handling

### Frontend Features
- ✅ Modern, responsive UI design
- ✅ API key authentication with session persistence
- ✅ Order placement interface (MARKET/LIMIT, BUY/SELL)
- ✅ Real-time portfolio view with P&L tracking
- ✅ Trade history browser
- ✅ Instruments catalog
- ✅ WebSocket connection status indicator
- ✅ Auto-refresh for portfolio and trades
- ✅ Error handling and user feedback

---

## 🛠 Technology Stack

### Backend
- **Python 3.8+**
- **FastAPI**: Modern, fast web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **WebSockets**: Real-time communication

### Frontend
- **React 19**: UI library
- **Vite**: Build tool and dev server
- **React Router**: Client-side routing
- **WebSocket API**: Real-time updates

### Development Tools
- **Pytest**: Testing framework
- **Docker**: Containerization
- **Git**: Version control

---

## 🏗 System Architecture

For detailed architecture documentation, see [ARCHITECTURE.md](./ARCHITECTURE.md).

### High-Level Architecture

```
┌─────────────────┐
│   React Client  │
│   (Frontend)    │
└────────┬────────┘
         │ HTTP/WebSocket
         │
┌────────▼─────────────────────────────────────┐
│         FastAPI Backend                        │
│  ┌──────────────────────────────────────────┐ │
│  │  API Layer (REST + WebSocket)            │ │
│  │  - /orders, /portfolio, /trades, /ws     │ │
│  └──────────────┬───────────────────────────┘ │
│                 │                             │
│  ┌──────────────▼───────────────────────────┐ │
│  │  Service Layer                           │ │
│  │  - Execution Engine                      │ │
│  │  - Limit Order Matcher (Background)      │ │
│  │  - Broadcaster (WebSocket)              │ │
│  └──────────────┬───────────────────────────┘ │
│                 │                             │
│  ┌──────────────▼───────────────────────────┐ │
│  │  Data Layer (In-Memory Store)            │ │
│  │  - Orders, Trades, Portfolio, Instruments│ │
│  └──────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
bajaj-broking-api/
├── app/                          # Backend application
│   ├── __init__.py
│   ├── main.py                   # FastAPI app entry point
│   ├── api/                      # API route handlers
│   │   ├── instruments.py        # Instrument endpoints
│   │   ├── orders.py             # Order management endpoints
│   │   ├── portfolio.py          # Portfolio endpoints
│   │   ├── trades.py             # Trade history endpoints
│   │   └── ws.py                 # WebSocket endpoint
│   ├── core/                     # Core utilities
│   │   └── auth.py               # Authentication dependency
│   ├── models/                   # Pydantic models
│   │   ├── instrument.py
│   │   ├── order.py
│   │   ├── portfolio.py
│   │   └── trade.py
│   ├── services/                 # Business logic
│   │   ├── execution_engine.py   # Order execution logic
│   │   ├── limit_matcher.py      # Background limit matcher
│   │   └── broadcaster.py        # WebSocket broadcaster
│   └── store/                    # Data storage
│       └── memory.py             # In-memory data store
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── components/           # React components
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Orders.jsx
│   │   │   ├── Portfolio.jsx
│   │   │   ├── Trades.jsx
│   │   │   └── Instruments.jsx
│   │   ├── contexts/             # React contexts
│   │   │   └── AuthContext.jsx
│   │   ├── hooks/                # Custom hooks
│   │   │   └── useWebSocket.js
│   │   ├── services/             # API services
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── sdk/                          # Python SDK
│   ├── trading_sdk.py            # SDK implementation
│   └── demo.py                   # SDK usage example
├── tests/                        # Test suite
│   ├── conftest.py
│   └── test_api.py
├── Dockerfile                    # Docker configuration
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── ARCHITECTURE.md               # Architecture documentation
├── API_DOCUMENTATION.md          # Detailed API docs
├── ASSUMPTIONS.md                # Implementation assumptions
└── SETUP.md                      # Quick setup guide
```

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Node.js 16+** and **npm** ([Download](https://nodejs.org/))
- **Git** (optional, for cloning repository)
- **Docker** (optional, for containerized deployment)

---

## 🚀 Setup and Installation

### Backend Setup

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd bajaj-broking-api
   ```

2. **Create and activate virtual environment**

   **Windows (PowerShell):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   **Unix / macOS / WSL:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

---

## 🏃 Running the Application

### Development Mode

#### Start Backend Server

In the project root directory (with virtual environment activated):

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base URL**: `http://localhost:8000`
- **Interactive API Docs**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/`

#### Start Frontend Development Server

In a new terminal, navigate to the frontend directory:

```bash
cd frontend
npm run dev
```

The frontend will be available at:
- **Frontend URL**: `http://localhost:5173`

### Access the Application

1. Open your browser and navigate to `http://localhost:5173`
2. Login with one of the demo API keys:
   - `demo-key` (user: demo-user)
   - `alice-key` (user: alice)
   - `bob-key` (user: bob)

---

## 📚 API Documentation

For detailed API documentation with request/response examples, see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md).

### Quick API Reference

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/instruments` | List all instruments | No |
| GET | `/api/v1/instruments/{symbol}` | Get instrument details | No |
| POST | `/api/v1/orders` | Place a new order | Yes |
| GET | `/api/v1/orders/{order_id}` | Get order details | Yes |
| POST | `/api/v1/orders/{order_id}/cancel` | Cancel an order | Yes |
| GET | `/api/v1/portfolio` | Get user portfolio | Yes |
| GET | `/api/v1/trades` | Get trade history | Yes |
| WS | `/api/v1/ws` | WebSocket for real-time updates | No |

### Authentication

All authenticated endpoints require the `x-api-key` header:

```bash
x-api-key: demo-key
```

Available API keys:
- `demo-key` → user: `demo-user`
- `alice-key` → user: `alice`
- `bob-key` → user: `bob`

---

## 🖥 Frontend Usage

### Login

1. Navigate to the login page
2. Enter an API key or click a demo button
3. You'll be redirected to the dashboard upon successful login

### Dashboard Features

- **Orders Tab**: Place new orders (MARKET/LIMIT, BUY/SELL)
- **Portfolio Tab**: View holdings, P&L, and portfolio metrics
- **Trades Tab**: Browse trade history
- **Instruments Tab**: View available trading instruments

### WebSocket Connection

The dashboard shows real-time connection status. When connected, you'll receive live trade execution updates via WebSocket.

---

## 📝 Sample API Usage

### Using cURL

#### 1. Get Available Instruments

```bash
curl -X GET "http://localhost:8000/api/v1/instruments" \
  -H "Content-Type: application/json"
```

**Response:**
```json
[
  {
    "symbol": "RELIANCE",
    "exchange": "NSE",
    "instrument_type": "EQ",
    "last_traded_price": 2500.00
  },
  {
    "symbol": "TCS",
    "exchange": "NSE",
    "instrument_type": "EQ",
    "last_traded_price": 3800.00
  }
]
```

#### 2. Place a MARKET BUY Order

```bash
curl -X POST "http://localhost:8000/api/v1/orders" \
  -H "Content-Type: application/json" \
  -H "x-api-key: demo-key" \
  -d '{
    "symbol": "RELIANCE",
    "order_type": "BUY",
    "order_style": "MARKET",
    "quantity": 10
  }'
```

**Response:**
```json
{
  "order_id": "123e4567-e89b-12d3-a456-426614174000",
  "symbol": "RELIANCE",
  "order_type": "BUY",
  "order_style": "MARKET",
  "quantity": 10,
  "price": null,
  "state": "EXECUTED",
  "created_at": "2024-01-15T10:30:00.000000",
  "executed_at": "2024-01-15T10:30:00.100000"
}
```

#### 3. Place a LIMIT SELL Order

```bash
curl -X POST "http://localhost:8000/api/v1/orders" \
  -H "Content-Type: application/json" \
  -H "x-api-key: demo-key" \
  -d '{
    "symbol": "TCS",
    "order_type": "SELL",
    "order_style": "LIMIT",
    "quantity": 5,
    "price": 3900.00
  }'
```

#### 4. Get Order Details

```bash
curl -X GET "http://localhost:8000/api/v1/orders/{order_id}" \
  -H "x-api-key: demo-key"
```

#### 5. Cancel an Order

```bash
curl -X POST "http://localhost:8000/api/v1/orders/{order_id}/cancel" \
  -H "x-api-key: demo-key"
```

#### 6. Get Portfolio

```bash
curl -X GET "http://localhost:8000/api/v1/portfolio" \
  -H "x-api-key: demo-key"
```

**Response:**
```json
{
  "user_id": "demo-user",
  "holdings": [
    {
      "symbol": "RELIANCE",
      "quantity": 10,
      "avg_price": 2500.00,
      "current_value": 25000.00
    }
  ]
}
```

#### 7. Get Trade History

```bash
curl -X GET "http://localhost:8000/api/v1/trades" \
  -H "x-api-key: demo-key"
```

### Using Python SDK

See `sdk/demo.py` for a complete example:

```bash
cd sdk
python demo.py
```

---

## 🧪 Testing

### Run Backend Tests

```bash
# Unix / macOS / WSL
PYTHONPATH=. pytest -q

# Windows (PowerShell)
$env:PYTHONPATH='.'; pytest -q
```

### Test Coverage

The test suite includes:
- API endpoint tests
- Order execution tests
- Portfolio calculation tests
- Authentication tests

---

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t bajaj-broking:latest .
```

### Run Container

```bash
docker run -p 8000:8000 --rm bajaj-broking:latest
```

### Docker Compose (Full Stack)

For a complete setup with frontend, see the Docker Compose configuration in the repository.

---

## 💡 Assumptions and Design Decisions

For detailed assumptions and design decisions, see [ASSUMPTIONS.md](./ASSUMPTIONS.md).

### Key Assumptions

1. **In-Memory Storage**: Data is stored in memory for simplicity and speed
2. **Single Server**: System runs on a single server instance
3. **API Key Authentication**: Simple API key-based auth for demonstration
4. **Order Matching**: Simplified matching logic (MARKET executes at LTP, LIMIT at specified price)
5. **Portfolio Calculation**: Average price calculated on BUY, unchanged on SELL
6. **No Partial Fills**: Orders execute fully or not at all
7. **No Order Book**: Simplified matching without traditional order book structure

---

## 🏭 Production Considerations

This system is designed for demonstration and learning. For production use, consider:

1. **Persistent Storage**: Replace in-memory store with PostgreSQL/MongoDB
2. **Authentication**: Implement OAuth2/JWT instead of API keys
3. **Order Book**: Implement proper order book with price-time priority
4. **Partial Fills**: Support partial order execution
5. **Message Queue**: Use Redis/RabbitMQ for event broadcasting
6. **Monitoring**: Add Prometheus metrics and logging
7. **Rate Limiting**: Implement API rate limiting
8. **Security**: Add input validation, SQL injection protection, etc.
9. **Scalability**: Design for horizontal scaling
10. **Data Persistence**: Implement database migrations and backups

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is provided for educational and demonstration purposes.

---

## 📞 Support

For questions or issues:
- Open an issue in the repository
- Check the [API Documentation](./API_DOCUMENTATION.md)
- Review [Architecture Documentation](./ARCHITECTURE.md)

---

## 🎓 Learning Resources

This project demonstrates:
- FastAPI REST API development
- WebSocket real-time communication
- Order matching engine concepts
- Portfolio management
- React frontend development
- Full-stack integration

---

**Built with ❤️ for learning and demonstration**
