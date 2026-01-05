# sdk/demo.py

from trading_sdk import TradingSDK

# use demo API key to authenticate
sdk = TradingSDK("http://127.0.0.1:8000", api_key="demo-key")

print("\n📌 Instruments:")
print(sdk.get_instruments())

print("\n📌 Place MARKET BUY Order:")
order = sdk.place_order(
    symbol="RELIANCE",
    order_type="BUY",
    order_style="MARKET",
    quantity=2
)
print(order)

order_id = order["order_id"]

print("\n📌 Fetch Order by ID:")
print(sdk.get_order(order_id))

print("\n📌 Trades:")
print(sdk.get_trades())

print("\n📌 Portfolio:")
print(sdk.get_portfolio())
