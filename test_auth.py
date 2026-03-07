import os
from dotenv import load_dotenv
from py_clob_client.client import ClobClient

load_dotenv()
private_key = os.getenv("PK")
funder = os.getenv("FUNDER")

print(f"PK loaded: {private_key[:6]}...{private_key[-4:] if private_key else 'MISSING'}")
print(f"FUNDER loaded: {funder if funder else 'MISSING'}")

host = "https://clob.polymarket.com"

print("\n--- Testing signature_type=0 ---")
try:
    client = ClobClient(host, key=private_key, chain_id=137, signature_type=0)
    creds = client.create_or_derive_api_creds()
    print(f"✅ SUCCESS: {creds}")
except Exception as e:
    print(f"❌ FAILED: {e}")

print("\n--- Testing signature_type=1 ---")
try:
    client = ClobClient(host, key=private_key, chain_id=137, signature_type=1, funder=funder)
    creds = client.create_or_derive_api_creds()
    print(f"✅ SUCCESS: {creds}")
except Exception as e:
    print(f"❌ FAILED: {e}")

print("\n--- Testing signature_type=2 ---")
try:
    client = ClobClient(host, key=private_key, chain_id=137, signature_type=2, funder=funder)
    creds = client.create_or_derive_api_creds()
    print(f"✅ SUCCESS: {creds}")
except Exception as e:
    print(f"❌ FAILED: {e}")