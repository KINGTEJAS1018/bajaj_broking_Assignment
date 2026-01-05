# Setup Guide - Bajaj Broking Full Stack Application

This guide will help you set up and run both the backend API and frontend React application.

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ and npm installed
- pip available

## Backend Setup

1. **Navigate to the project root directory**

2. **Create and activate virtual environment**

   Windows (PowerShell):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   Unix / macOS / WSL:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/`

## Frontend Setup

1. **Navigate to the frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## Running the Application

1. **Start the backend** (in one terminal)
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the frontend** (in another terminal)
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open your browser**
   - Navigate to `http://localhost:5173`
   - Login with one of the demo API keys:
     - `demo-key` (demo-user)
     - `alice-key` (alice)
     - `bob-key` (bob)

## Features

### Backend (FastAPI)
- ✅ CORS middleware configured for React frontend
- ✅ REST API endpoints for orders, portfolio, trades, instruments
- ✅ WebSocket endpoint for real-time updates
- ✅ API key authentication

### Frontend (React)
- ✅ Modern UI with responsive design
- ✅ Authentication with API keys
- ✅ Order placement (MARKET and LIMIT orders)
- ✅ Portfolio view with P&L tracking
- ✅ Trade history
- ✅ Instruments browser
- ✅ WebSocket connection for real-time updates
- ✅ Auto-refresh for portfolio and trades

## Troubleshooting

### CORS Errors
- Ensure the backend is running on port 8000
- Check that CORS middleware is properly configured in `app/main.py`
- Verify the frontend is running on port 5173 (Vite default)

### Authentication Errors
- Make sure you're using a valid API key: `demo-key`, `alice-key`, or `bob-key`
- Check that the API key is being sent in the `x-api-key` header
- Verify the backend authentication is working by checking the API docs at `http://localhost:8000/docs`

### WebSocket Connection Issues
- Ensure the backend is running
- Check the WebSocket URL in `frontend/src/components/Dashboard.jsx`
- Verify the WebSocket endpoint is accessible at `ws://localhost:8000/api/v1/ws`

### Port Conflicts
- If port 8000 is in use, change it in the uvicorn command
- Update `API_BASE_URL` in `frontend/src/services/api.js` if you change the backend port
- If port 5173 is in use, Vite will automatically use the next available port

## Development Tips

- The backend auto-reloads on code changes (--reload flag)
- The frontend has hot module replacement (HMR) enabled
- Check browser console for frontend errors
- Check terminal for backend errors
- Use the API docs at `http://localhost:8000/docs` to test endpoints directly

## Production Deployment

For production:
1. Build the frontend: `cd frontend && npm run build`
2. Serve the built files using a static file server or integrate with the FastAPI backend
3. Update CORS origins to match your production domain
4. Use environment variables for API keys and configuration
5. Replace the in-memory store with a persistent database

