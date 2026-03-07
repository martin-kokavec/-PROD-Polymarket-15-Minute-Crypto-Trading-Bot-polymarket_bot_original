import os
import sys
import json
import time
import requests
import datetime
from dotenv import load_dotenv
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY

# Configureable parameters

BUY_IN_LAST_X_MINUTES = 5 # For example, if set to 5, buys will be attempted at minutes 10, 25, 40, 55 of each hour.
SHARES_TO_BUY = 6.0       # The number of shares to buy in a single order.
BUY_PRICE = 0.99          # The limit price for the buy order.
CHECK_INTERVAL_SECONDS = 15 # How often the bot checks for new market data.

def log_message(message):
    log_file_name = "bot.log"
    message = str(message).strip()
    if not message:
        return

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    print(log_entry + "\n")
    try:
        with open(log_file_name, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    except Exception as e:
        print(f"[{timestamp}] CRITICAL: Failed to write to log file: {e}")

def load_credentials():
    env_path = '.env'
    if not os.path.exists(env_path):
        log_message("FATAL: Environment file '.env' not found. Please create it with your PK and FUNDER.")
        sys.exit(1)

    load_dotenv()
    private_key = os.getenv("PK")
    funder_address = os.getenv("FUNDER")

    if not private_key or not funder_address:
        log_message("FATAL: Could not find PK and/or FUNDER inside the .env file.")
        log_message("Please make sure your .env file has the format:\nPK=your_private_key_here\nFUNDER=your_funder_address_here")
        sys.exit(1)

    return private_key, funder_address

def get_clob_client(private_key, funder_address):
    host = "https://clob.polymarket.com"
    client = ClobClient(host, key=private_key, chain_id=137, signature_type=1, funder=funder_address)
    client.set_api_creds(client.create_or_derive_api_creds())
    return client

def place_market_buy_order(client, token_id, size, price, direction):
    log_message(f"--- Placing Market Buy Order ---")
    log_message(f"   - Attempting to buy {size} shares of '{direction}' at up to ${price:.2f}...")

    try:
        order_args = OrderArgs(price=price, size=float(size), side=BUY, token_id=token_id)
        signed_order = client.create_order(order_args)
        log_message(f"   - ✅ Order placement response: {resp}")
        return True

    except Exception as e:
        log_message(f"   - ❌ An error occurred during buy order placement: {e}")
        return False

def get_current_polymarket_tokens():
    current_time = int(time.time())
    market_timestamp = (current_time // 900) * 900
    slug = f"btc-updown-15m-{market_timestamp}"
    log_message(f"--- 🔍 Searching for Polymarket market with slug: {slug} ---")

    try:
        url = f"https://gamma-api.polymarket.com/markets/slug/{slug}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        market = response.json()

        question = market.get('question')
        market_slug = market.get('slug')
        token_ids = json.loads(market['clobTokenIds'])
        yes_token_id = token_ids[0]
        no_token_id = token_ids[1]

        log_message(f"✅ Found Market: \"{question}\"")
        return question, market_slug, yes_token_id, no_token_id

    except (requests.exceptions.RequestException, KeyError, json.JSONDecodeError) as e:
        log_message(f"Error fetching or parsing market data for slug '{slug}': {e}")
        return None, None, None, None

def get_poly_sell_price(token_id):
    url = f"https://clob.polymarket.com/price?token_id={token_id}&side=BUY"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return float(response.json()['price'])
    except Exception:
        return None

def get_poly_orderbook_prices(token_id):
    ask_price = None
    bid_price = None

    try:
        url = f"https://clob.polymarket.com/price?token_id={token_id}&side=SELL"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        ask_price = float(response.json()['price'])
    except Exception:
        pass

    bid_price = get_poly_sell_price(token_id)

    return ask_price, bid_price

def has_traded_in_interval(last_trade_interval):
    now = datetime.datetime.now()
    current_interval = now.minute // 15
    
    if last_trade_interval == current_interval:
        return True
    return False

def main():
    log_message("🤖 --- Polymarket 15-Min BTC Auto-Trader Started --- 🤖")
    log_message(f"   - 📈 Will attempt to buy {SHARES_TO_BUY} shares in the last {BUY_IN_LAST_X_MINUTES} minutes of each interval.")

    private_key, funder_address = load_credentials()
    clob_client = get_clob_client(private_key, funder_address)

    last_trade_interval = -1

    while True:
        try:
            question, market_slug, yes_token, no_token = get_current_polymarket_tokens()
            
            if market_slug:
                log_message("--- 💹 Fetching Polymarket Prices 💹 ---")
                
                yes_ask, yes_bid = get_poly_orderbook_prices(yes_token)
                yes_ask_str = f"${yes_ask:.3f}" if yes_ask is not None else "N/A"
                yes_bid_str = f"${yes_bid:.3f}" if yes_bid is not None else "N/A"
                log_message(f"  - YES (Up):   Ask: {yes_ask_str:<8} | Bid: {yes_bid_str:<8}")

                no_ask, no_bid = get_poly_orderbook_prices(no_token)
                no_ask_str = f"${no_ask:.3f}" if no_ask is not None else "N/A"
                no_bid_str = f"${no_bid:.3f}" if no_bid is not None else "N/A"
                log_message(f"  - NO (Down):  Ask: {no_ask_str:<8} | Bid: {no_bid_str:<8}\n")

                now = datetime.datetime.now()
                minute_in_interval = now.minute % 15
                trigger_minute = 15 - BUY_IN_LAST_X_MINUTES

                if minute_in_interval >= trigger_minute and not has_traded_in_interval(last_trade_interval):
                    log_message(f"--- ✅ BUY WINDOW ACTIVE (Minute {minute_in_interval} >= {trigger_minute}) ---")

                    if yes_bid is not None and no_bid is not None:
                        if yes_bid > no_bid:
                            log_message(f"   - Highest bid is for YES (${yes_bid:.3f}). Placing buy order.")
                            trade_successful = place_market_buy_order(clob_client, yes_token, SHARES_TO_BUY, BUY_PRICE, "YES (Up)")
                        else:
                            log_message(f"   - Highest bid is for NO (${no_bid:.3f}). Placing buy order.")
                            trade_successful = place_market_buy_order(clob_client, no_token, SHARES_TO_BUY, BUY_PRICE, "NO (Down)")
                        
                        if trade_successful:
                            last_trade_interval = now.minute // 15
                            log_message(f"   - Trade placed for interval {last_trade_interval}. Waiting for next interval.")

                    else:
                        log_message("   - ❌ Cannot determine highest bid. One or both bid prices are unavailable.")
                else:
                    if last_trade_interval != now.minute // 15:
                        last_trade_interval = -1

            log_message(f"--- Cycle complete. Waiting {CHECK_INTERVAL_SECONDS} seconds. ---\n")
            time.sleep(CHECK_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            log_message("--- Price monitor shutting down manually. ---")
            sys.exit(0)
        except Exception as e:
            log_message(f"An unexpected error occurred in the main loop: {e}")
            time.sleep(30) # Wait a bit longer after a major error

if __name__ == "__main__":
    main()