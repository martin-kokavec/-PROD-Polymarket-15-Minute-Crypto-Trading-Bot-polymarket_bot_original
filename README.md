# Polymarket 15-Minute BTC Trading Bot 

![Python](https://img.shields.io/badge/python-3.x-blue.svg)

A simple and automated trading bot designed to trade on Polymarket's 15-minute BTC/USD prediction markets. The bot monitors the market in real-time, identifies the side with the highest bid price, and automatically places a buy order within a configurable time window before the market resolves.

## Features

- **Automated Trading**: Automatically places buy orders on the most likely outcome based on current bid prices.
- **Time-Based Execution**: Configurable to only trade within the last few minutes of each 15-minute market interval.
- **Real-Time Monitoring**: Continuously fetches and displays the latest Ask and Bid prices for both sides of the market.
- **Customizable**: Easily adjust key parameters like trade timing, share quantity, and buy price.
- **Secure**: Keeps your private key and funder address safe and separate from the main script using a `.env` file.
- **Logging**: All actions, price checks, and trade attempts are logged to `bot.log` for easy monitoring and debugging.

## Prerequisites

- Python 3.7+
- A Polymarket account (Email or Wallet-based)
- A funded trading address with USDC

## ⚙️ Setup and Installation

Follow these steps to get the bot up and running.

### 1. Clone the Repository

```bash
git clone https://github.com/Polando008/Polymarket-15-Minute-Crypto-Trading-Bot
cd Polymarket-15-Minute-Crypto-Trading-Bot
```

### 2. Install Dependencies

Install the required Python libraries using pip:

```bash
pip install requests python-dotenv py-clob-client
```

### 3. Create and Configure the Environment File

This is the most important step for securing your account credentials.

1.  In the project directory, find the **`.env.example`** file.
2.  Create a copy of this file and name it **`.env`**.
3.  Open the new `.env` file and add your Polymarket **Private Key** and **Funder Address**.

Your `.env` file should look like this:

```dotenv
# This is your private key. It should start with 0x.
# IMPORTANT: Keep this file secure and do not share it with anyone.
PK=0xyour_private_key_here

# This is your Polymarket funder address.
FUNDER=0xyour_funder_address_here
```


## 🔧 Bot Configuration

You can customize the bot's trading strategy by editing the parameters at the top of the `15min.py` file:

- `BUY_IN_LAST_X_MINUTES`: Sets the time window for placing a trade. For example, a value of `5` will trigger a buy attempt at minutes `10`, `25`, `40`, and `55` of each hour.
- `SHARES_TO_BUY`: The number of shares to purchase in each trade.
- `BUY_PRICE`: The limit price for the buy order. Setting this to `0.99` effectively makes it a market order, ensuring it fills at the best available price.
- `CHECK_INTERVAL_SECONDS`: How often the bot fetches new market data.

## ▶️ Running the Bot

Once everything is configured, start the bot by running:

```bash
15min.py
```

The bot will start logging its activity to the console and to the `bot.log` file.

## 📞 Contact Me

If you need setup, upgrades, or a custom bot, contact me through this link.

![Contact](https://fiverr-res.cloudinary.com/images/q_auto,f_auto/gigs/458516297/original/ddd7e230838d11152ebe129f9e61f6fbf6fe3fb3/build-auto-polymarket-trading-bot.png)

https://www.fiverr.com/daviddorkiw/build-auto-polymarket-trading-bot

## 📜 Disclaimer

This software is for educational purposes only. Automated trading involves significant risk, and you are solely responsible for any financial losses. The creators of this bot are not liable for your trading decisions. Use at your own risk.
