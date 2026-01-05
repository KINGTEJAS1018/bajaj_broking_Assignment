# app/api/instruments.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.instrument import Instrument
from app.store.memory import INSTRUMENTS

router = APIRouter()

@router.get("/instruments", response_model=List[Instrument], tags=["Instruments"])
def get_instruments():
    """
    Return all available instruments (seeded in-memory).
    """
    return INSTRUMENTS

@router.get("/instruments/{symbol}", response_model=Instrument, tags=["Instruments"])
def get_instrument(symbol: str):
    """
    Return a single instrument by symbol (case-insensitive).
    """
    symbol_upper = symbol.upper()
    for inst in INSTRUMENTS:
        if inst["symbol"].upper() == symbol_upper:
            return inst
    raise HTTPException(status_code=404, detail="Instrument not found")
