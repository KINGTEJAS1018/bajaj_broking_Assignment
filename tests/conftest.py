# tests/conftest.py
import pytest
from app.store import memory

@pytest.fixture(autouse=True)
def reset_store():
    """
    Automatically runs before EACH test function.
    Clears the in-memory database to ensure test isolation.
    """
    memory.ORDERS.clear()
    memory.TRADES.clear()
    memory.PORTFOLIO.clear()
    # Note: We usually don't clear INSTRUMENTS as they are static seed data