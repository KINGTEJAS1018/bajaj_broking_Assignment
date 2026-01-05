# API Documentation

Complete API reference for the Bajaj Broking Trading Platform.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Most endpoints require authentication using an API key in the request header:

```
x-api-key: demo-key
```

### Available API Keys

| API Key | User ID | Description |
|---------|---------|-------------|
| `demo-key` | `demo-user` | Default demo user |
| `alice-key` | `alice` | Demo user Alice |
| `bob-key` | `bob` | Demo user Bob |

---

## Endpoints

### Instruments

#### Get All Instruments

Retrieve a list of all available trading instruments.

**Endpoint:** `GET /instruments`

**Authentication:** Not required

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/instruments"
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
  },
  {
    "symbol": "INFY",
    "exchange": "NSE",
    "instrument_type": "EQ",
    "last_traded_price": 1500.50
  }
]
```

**Status Codes:**
- `200 OK`: Success

---

#### Get Instrument by Symbol

Retrieve details for a specific instrument.

**Endpoint:** `GET /instruments/{symbol}`

**Authentication:** Not required

**Path Parameters:**
- `symbol` (string, required): Instrument symbol (case-insensitive)

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/instruments/RELIANCE"
```

**Response:**
```json
{
  "symbol": "RELIANCE",
  "exchange": "NSE",
  "instrument_type": "EQ",
  "last_traded_price": 2500.00
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Instrument not found

---

### Orders

#### Place Order

Place a new trading order (MARKET or LIMIT).

**Endpoint:** `POST /orders`

**Authentication:** Required

**Request Body:**
```json
{
  "symbol": "RELIANCE",
  "order_type": "BUY",
  "order_style": "MARKET",
  "quantity": 10,
  "price": null
}
```

**Fields:**
- `symbol` (string, required): Instrument symbol
- `order_type` (enum, required): `"BUY"` or `"SELL"`
- `order_style` (enum, required): `"MARKET"` or `"LIMIT"`
- `quantity` (integer, required): Order quantity (must be > 0)
- `price` (float, optional): Required for LIMIT orders, ignored for MARKET orders

**Request Examples:**

**MARKET BUY Order:**
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

**LIMIT SELL Order:**
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

**Status Codes:**
- `200 OK`: Order placed successfully
- `400 Bad Request`: Invalid request (e.g., missing price for LIMIT order)
- `401 Unauthorized`: Invalid or missing API key
- `404 Not Found`: Instrument not found
- `422 Unprocessable Entity`: Validation error

**Order States:**
- `PLACED`: Order is pending execution
- `EXECUTED`: Order has been executed
- `CANCELLED`: Order has been cancelled

---

#### Get Order Details

Retrieve details for a specific order.

**Endpoint:** `GET /orders/{order_id}`

**Authentication:** Required (must own the order)

**Path Parameters:**
- `order_id` (string, required): Order UUID

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/orders/123e4567-e89b-12d3-a456-426614174000" \
  -H "x-api-key: demo-key"
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

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Invalid or missing API key
- `403 Forbidden`: Order belongs to different user
- `404 Not Found`: Order not found

---

#### Cancel Order

Cancel a pending order.

**Endpoint:** `POST /orders/{order_id}/cancel`

**Authentication:** Required (must own the order)

**Path Parameters:**
- `order_id` (string, required): Order UUID

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/orders/123e4567-e89b-12d3-a456-426614174000/cancel" \
  -H "x-api-key: demo-key"
```

**Response:**
```json
{
  "order_id": "123e4567-e89b-12d3-a456-426614174000",
  "symbol": "RELIANCE",
  "order_type": "BUY",
  "order_style": "LIMIT",
  "quantity": 10,
  "price": 2400.00,
  "state": "CANCELLED",
  "created_at": "2024-01-15T10:30:00.000000",
  "executed_at": null
}
```

**Status Codes:**
- `200 OK`: Order cancelled successfully
- `400 Bad Request`: Order cannot be cancelled (already executed or cancelled)
- `401 Unauthorized`: Invalid or missing API key
- `403 Forbidden`: Order belongs to different user
- `404 Not Found`: Order not found

---

### Portfolio

#### Get Portfolio

Retrieve portfolio holdings for the authenticated user.

**Endpoint:** `GET /portfolio`

**Authentication:** Required

**Request:**
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
    },
    {
      "symbol": "TCS",
      "quantity": 5,
      "avg_price": 3800.00,
      "current_value": 19000.00
    }
  ]
}
```

**Response Fields:**
- `user_id` (string): Authenticated user ID
- `holdings` (array): List of holdings
  - `symbol` (string): Instrument symbol
  - `quantity` (integer): Number of shares held
  - `avg_price` (float): Average purchase price
  - `current_value` (float): Current market value (quantity × LTP)

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Invalid or missing API key

---

### Trades

#### Get Trade History

Retrieve executed trades for the authenticated user.

**Endpoint:** `GET /trades`

**Authentication:** Required

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/trades" \
  -H "x-api-key: demo-key"
```

**Response:**
```json
[
  {
    "trade_id": "456e7890-e89b-12d3-a456-426614174001",
    "order_id": "123e4567-e89b-12d3-a456-426614174000",
    "symbol": "RELIANCE",
    "quantity": 10,
    "price": 2500.00,
    "side": "BUY",
    "timestamp": "2024-01-15T10:30:00.100000"
  },
  {
    "trade_id": "789e0123-e89b-12d3-a456-426614174002",
    "order_id": "234e5678-e89b-12d3-a456-426614174003",
    "symbol": "TCS",
    "quantity": 5,
    "price": 3800.00,
    "side": "SELL",
    "timestamp": "2024-01-15T11:00:00.200000"
  }
]
```

**Response Fields:**
- `trade_id` (string): Unique trade identifier
- `order_id` (string): Associated order ID
- `symbol` (string): Instrument symbol
- `quantity` (integer): Trade quantity
- `price` (float): Execution price
- `side` (string): `"BUY"` or `"SELL"`
- `timestamp` (string): ISO 8601 timestamp

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Invalid or missing API key

---

### WebSocket

#### WebSocket Connection

Connect to real-time trade execution updates.

**Endpoint:** `WS /ws`

**Authentication:** Not required (but user context may be added in future)

**Connection URL:**
```
ws://localhost:8000/api/v1/ws
```

**Connection Example (JavaScript):**
```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/ws');

ws.onopen = () => {
  console.log('WebSocket connected');
  // Send periodic pings to keep connection alive
  setInterval(() => ws.send('ping'), 30000);
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Trade update:', data);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('WebSocket disconnected');
};
```

**Message Format:**
```json
{
  "type": "trade",
  "trade": {
    "trade_id": "456e7890-e89b-12d3-a456-426614174001",
    "order_id": "123e4567-e89b-12d3-a456-426614174000",
    "symbol": "RELIANCE",
    "quantity": 10,
    "price": 2500.00,
    "side": "BUY",
    "timestamp": "2024-01-15T10:30:00.100000"
  }
}
```

**Message Types:**
- `trade`: Trade execution notification

---

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message description"
}
```

### Common Error Codes

| Status Code | Description |
|-------------|-------------|
| `400 Bad Request` | Invalid request parameters |
| `401 Unauthorized` | Missing or invalid API key |
| `403 Forbidden` | Access denied (e.g., accessing another user's order) |
| `404 Not Found` | Resource not found |
| `422 Unprocessable Entity` | Validation error |
| `500 Internal Server Error` | Server error |

### Validation Errors

When validation fails (422), the response includes detailed error information:

```json
{
  "detail": [
    {
      "loc": ["body", "quantity"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production, implement rate limiting based on API key.

---

## Best Practices

1. **Always include API key** in authenticated requests
2. **Handle errors gracefully** - check status codes and error messages
3. **Use WebSocket** for real-time updates instead of polling
4. **Validate input** before sending requests
5. **Store order IDs** for later reference
6. **Check order state** before attempting cancellation

---

## Interactive API Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These interfaces allow you to:
- View all available endpoints
- See request/response schemas
- Test endpoints directly from the browser
- View example requests and responses

---

## SDK Usage

For easier integration, use the Python SDK:

```python
from sdk.trading_sdk import TradingSDK

sdk = TradingSDK("http://localhost:8000", api_key="demo-key")

# Place order
order = sdk.place_order(
    symbol="RELIANCE",
    order_type="BUY",
    order_style="MARKET",
    quantity=10
)

# Get portfolio
portfolio = sdk.get_portfolio()

# Get trades
trades = sdk.get_trades()
```

See `sdk/demo.py` for complete examples.

---

## Support

For questions or issues:
- Check the main [README.md](./README.md)
- Review [ARCHITECTURE.md](./ARCHITECTURE.md) for system design
- Open an issue in the repository

