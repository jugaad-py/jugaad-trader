# Introduction

Jugad trader is an unofficial client for Zerodha and Upstox trading account. You can programatically log in to your Zerodha and Upstox account using your credentials and automate some of your tasks.

PLEASE USE THIS LIBRARY AT YOUR OWN RISK, THERE ARE NO GURANTEES ASSOCIATED WITH THIS LIBRARY. PLEASE USE OFFICIAL API SUBSCRIPTION FOR ALL SERIOUS USAGE.

## Table of content
1. [Installation](#installation)
2. [Getting Started with Upstox](#getting-started-with-upstox)
3. [Getting Started with Zerodha](#getting-started-with-zerodha)
4. [Source Code](#source-code)
## Installation

```
pip install jugaad-trader
```

## Getting Started with Upstox

```Python
from jugaad_trader import Upstox
user_id = "USERID"
password = "PASSWORD"
twofa = "TWOFA"
u = Upstox(user_id, password, twofa)

# Login
u.login()

# Get profile information
profile = u.get_client_info()

# More documentation to follow
```


## Getting Started with Zerodha

```Python
from jugaad_trader import Zerodha
user_id = "USERID"
password = "PASSWORD"
twofa = "TWOFA"
z = Zerodha(user_id, password, twofa)

# Log into account
status = z.login()
print(status)

# Get profile
profile = z.full_profile()
print(profile)

# Get margin
margins = z.margins()
print(margins)

# Get holdings
holdings = z.holdings()
print(holdings)

# Get today's positions
positions = z.positions()
print(positions)

# Get today's orders
orders = z.orders()
print(orders)

# Finally placing an order
order_resp = z.place_order(variety=z.VARIETY_REGULAR,
			tradingsymbol="INFY",
			exchange=z.EXCHANGE_NSE,
			transaction_type=z.TRANSACTION_TYPE_BUY,
			quantity=1,
			order_type=z.ORDER_TYPE_MARKET,
			product=z.PRODUCT_CNC)
print(order_resp)

```

## Contributing to Jugaad Trader

I am planning to conduct a small session for walk thru of how I reverse-engineered the trading portals. The intention here is to pass on the knowledge so that I can get contributions from community.

Below form is for capturing your interest in attending the session, email-id is required to share the meeting invite with you.

I'll await to collect at-least 10+ responses to conduct the session.

[Google form link](https://docs.google.com/forms/d/e/1FAIpQLSdrFaFhCNU1Pw0zwcERckmV2shAjrX54R-FajAkL75HeNoR0A/viewform?usp=sf_link)

## Source code

[https://github.com/jugaad-py/jugaad-trader.git](https://github.com/jugaad-py/jugaad-trader.git)
