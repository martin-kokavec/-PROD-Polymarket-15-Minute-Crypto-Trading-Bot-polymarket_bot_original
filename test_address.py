from eth_account import Account
import os
from dotenv import load_dotenv

load_dotenv()
pk = os.getenv("PK")
account = Account.from_key(pk)
print(f"Address derived from your PK: {account.address}")