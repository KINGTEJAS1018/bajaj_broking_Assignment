# app/models/instrument.py
from pydantic import BaseModel

class Instrument(BaseModel):
    symbol: str
    exchange: str
    instrument_type: str
    last_traded_price: float
