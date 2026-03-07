import os
from dotenv import load_dotenv
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY

load_dotenv()
private_key = os.getenv("PK")
funder = os.getenv("FUNDER")

host = "https://clob.polymarket.com"

# Try all 3 signature types for order signing
for sig_type in [0, 1, 2]:
    print(f"\n--- Testing order signing with signature_type={sig_type} ---")
    try:
        if sig_type == 0:
            client = ClobClient(host, key=private_key, chain_id=137, signature_type=0)
        else:
            client = ClobClient(host, key=private_key, chain_id=137, signature_type=sig_type, funder=funder)
        
        client.set_api_creds(client.create_or_derive_api_creds())

        # Use a real token ID from a live market — BTC 15min YES token
        test_token_id = "21742633143463906290569050155826241533067272736897614950488156847949938836455"
        order_args = OrderArgs(price=0.99, size=1.0, side=BUY, token_id=test_token_id)
        signed_order = client.create_order(order_args)
        resp = client.post_order(signed_order, OrderType.GTC)
        print(f"✅ SUCCESS: {resp}")
    except Exception as e:
        print(f"❌ FAILED: {e}")