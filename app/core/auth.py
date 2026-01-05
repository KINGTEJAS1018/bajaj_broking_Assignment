# app/core/auth.py
from fastapi import Header, HTTPException, Depends

API_KEYS = {"demo-key": "demo-user", "alice-key": "alice", "bob-key": "bob"}

def get_current_user(x_api_key: str = Header(None)):
    if x_api_key is None or x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return API_KEYS[x_api_key]
