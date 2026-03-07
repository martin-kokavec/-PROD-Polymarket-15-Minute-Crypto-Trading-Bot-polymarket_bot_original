import os
from dotenv import load_dotenv
from py_clob_client.client import ClobClient

load_dotenv()
private_key = os.getenv("PK")
funder = os.getenv("FUNDER")

host = "https://clob.polymarket.com"

print("Setting up allowance for trading key...")
try:
    client = ClobClient(host, key=private_key, chain_id=137, signature_type=0)
    client.set_api_creds(client.create_or_derive_api_creds())
    
    # Approve USDC allowance
    resp = client.update_local_nonce()
    print(f"Nonce updated: {resp}")
    
    approval = client.approve_usdc()
    print(f"✅ USDC approval response: {approval}")

except Exception as e:
    print(f"❌ Failed: {e}")