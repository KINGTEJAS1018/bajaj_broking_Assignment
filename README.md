# Bajaj Broking — Matching Engine API

>A lightweight, in-memory order matching API built with FastAPI. This project demonstrates core exchange concepts — order placement, limit/market matching, executions, portfolio tracking, and real-time event broadcasting — implemented for learning, testing, and small-scale demos.

---

## Key capabilities

- REST API for placing, cancelling and querying orders
- In-memory store for rapid prototyping and deterministic tests
- Simple matching engine handling market and limit logic
- WebSocket broadcasting for real-time trade/execution events
- Minimal Python SDK and demo for integration testing

---

## Production-ready overview

This repository contains an application that is ready for local development, CI testing, and containerized deployments. It is intentionally small and opinionated to make it easy to read, extend and test. For production usage you should replace the in-memory store with a durable datastore, add persistent logging, metrics, and secure the authentication layer.

---

## Project structure

- `app/` — Application source
  - `main.py` — FastAPI application entry
  - `api/` — REST & WebSocket route handlers
    - `instruments.py`, `orders.py`, `portfolio.py`, `trades.py`, `ws.py`
  - `core/` — Lightweight helpers (auth dependency)
  - `models/` — Pydantic domain & DTO models
  - `services/` — Business logic (execution engine, matcher, broadcaster)
  - `store/` — In-memory datastore (seeded instruments, orders, trades)
- `sdk/` — Mini client SDK and demo script (`trading_sdk.py`, `demo.py`)
- `tests/` — Pytest test-suite and fixtures
- `requirements.txt` — Python dependency pin list
- `Dockerfile` — Container image build instructions (example)

---

## Quick start (development)

Prerequisites

- Python 3.8+ installed
- `pip` available

Create and activate a virtual environment

Unix / macOS / WSL:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the API server (development):

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open interactive docs: http://127.0.0.1:8000/docs

---

## API Endpoints (summary)

- POST `/orders` — Place a new order. Accepts `OrderRequest` and returns `OrderResponse`.
- POST `/orders/{order_id}/cancel` — Cancel an order owned by the caller.
- GET `/orders/{order_id}` — Query order state.
- GET `/instruments` — List available instruments.
- GET `/trades` — Retrieve trade history.
- GET `/portfolio` — View portfolio positions/metrics.
- WebSocket `/ws` — Subscribe for real-time events (trades/executions).

Refer to the route handlers in `app/api/` for request/response details and example payloads.

---

## Usage examples

Place a market buy order (curl):

```bash
curl -s -X POST http://127.0.0.1:8000/orders \\
  -H "Content-Type: application/json" \\
  -d '{"symbol":"ABC","order_type":"MARKET","order_style":"BUY","quantity":10}'
```

Cancel an order:

```bash
curl -s -X POST http://127.0.0.1:8000/orders/<order_id>/cancel
```

Use the `sdk/demo.py` script to run an integration demo against a running server:

```bash
python sdk/demo.py
```

---

## Testing

Run unit tests with pytest. If you encounter `ModuleNotFoundError: No module named 'app'`, ensure the repository root is on `PYTHONPATH` or make `app` a package.

Quick run (temporary):

Unix / CI:
```bash
PYTHONPATH=. pytest -q
```

Windows (PowerShell):
```powershell
$env:PYTHONPATH='.'; pytest -q
```

Persistent fixes (recommended for CI / editors):

- Add empty `app/__init__.py` and `app/store/__init__.py` to make `app` a proper package.
- Alternatively, add packaging metadata and install the project in editable mode:

```bash
pip install -e .
```

---

## Configuration & environment

This project is minimal and reads configuration inline. For production hardened deployments:

- Load secrets and credentials from environment variables or a secret manager
- Configure logging (structured JSON), log aggregation, and retention
- Add observability: Prometheus metrics, request tracing (OpenTelemetry)
- Persist order/trade state to an ACID-backed datastore (Postgres), and use a durable broker for events

---

## Docker

Build image (example):

```bash
docker build -t bajaj-broking:latest .
```

Run container (example):

```bash
docker run -p 8000:8000 --rm bajaj-broking:latest
```

Note: For production, swap the in-memory store to a persistent storage layer and configure environment variables.

---

## CI/CD suggestions

- Add a GitHub Actions workflow or similar to run `pip install -r requirements.txt` and `pytest -q` on PRs.
- Add linting (flake8 or ruff) and type checks (mypy) in the pipeline.
- Build and publish a Docker image on successful merges to `main`.

---

## Security & hardening notes

- Do not expose the development server publicly. Use an ASGI server like `gunicorn` with `uvicorn` workers or a managed platform for production.
- Harden authentication — the included `core/auth.py` is a simple dependency for demos and tests only.
- Validate and sanitize inputs in public-facing endpoints.

---

## Contributing

- Fork the repository and open a PR with focused changes.
- Include tests for new behavior and run the test suite locally.
- Keep commits small and add a clear PR description.

---

## License

Add a `LICENSE` file to the repository. If you want an example, use the MIT license.

---

## Contact

For questions or issues open an issue in this repository or contact the maintainer.

---

If you'd like, I can:

- add `app/__init__.py` and `app/store/__init__.py` to make imports stable in editors/CI,
- add a minimal `pyproject.toml` to enable `pip install -e .`, or
- create a basic GitHub Actions workflow for testing and linting.

Tell me which follow-up you'd like and I'll apply it.
