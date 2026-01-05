# Bajaj Broking Frontend

React frontend for the Bajaj Broking Trading Platform.

## Features

- **Authentication**: Login with API keys (demo-key, alice-key, bob-key)
- **Order Management**: Place and cancel orders (MARKET and LIMIT)
- **Portfolio View**: View holdings, P&L, and portfolio metrics
- **Trade History**: View executed trades
- **Instruments**: Browse available trading instruments
- **Real-time Updates**: WebSocket connection for live trade updates

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- Backend API running on `http://localhost:8000`

### Installation

```bash
npm install
```

### Development

Start the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Build

Build for production:

```bash
npm run build
```

## Usage

1. Start the backend API server (see main README)
2. Start the frontend: `npm run dev`
3. Open `http://localhost:5173` in your browser
4. Login with one of the demo API keys:
   - `demo-key` (demo-user)
   - `alice-key` (alice)
   - `bob-key` (bob)

## Project Structure

```
frontend/
├── src/
│   ├── components/      # React components
│   │   ├── Login.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Orders.jsx
│   │   ├── Portfolio.jsx
│   │   ├── Trades.jsx
│   │   └── Instruments.jsx
│   ├── contexts/        # React contexts
│   │   └── AuthContext.jsx
│   ├── hooks/           # Custom hooks
│   │   └── useWebSocket.js
│   ├── services/        # API services
│   │   └── api.js
│   ├── App.jsx          # Main app component
│   └── main.jsx         # Entry point
├── package.json
└── vite.config.js
```

## API Configuration

The API base URL is configured in `src/services/api.js`. By default, it points to `http://localhost:8000/api/v1`.

To change the API URL, update the `API_BASE_URL` constant in `src/services/api.js`.

## Features in Detail

### Authentication
- API key-based authentication
- Session persistence using localStorage
- Automatic redirect to login if not authenticated

### Order Placement
- Support for MARKET and LIMIT orders
- BUY and SELL order types
- Real-time order status updates
- Order cancellation for pending orders

### Portfolio
- Real-time portfolio value calculation
- P&L tracking per holding and overall
- Auto-refresh every 5 seconds

### Trades
- Complete trade history
- Trade details including price, quantity, and timestamp
- Auto-refresh every 5 seconds

### WebSocket
- Real-time connection status indicator
- Automatic reconnection handling
- Ping/pong to keep connection alive
