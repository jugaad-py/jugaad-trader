## Free Zerodha API - jugaad-trader

Jugaad trader implements reverse engineered API for Zerodha in python (hence the name Jugaad). With this library you can programatically execute trades, retrieve your order and trade books, holdings, margins among other things.

Documentation - https://marketsetup.in/documentation/jugaad-trader/


## Installation

```
pip install jugaad-trader
```

### Quick start


### Step 1 - Log in to Zerodha account with jtrader CLI

```
$ jtrader zerodha startsession
User ID >: Zerodha User Id
Password >:
Pin >:
Logged in successfully
```

### Step 2 - Instantiate Zerodha and issue commands

```python
from jugaad_trader import Zerodha
kite = Zerodha()
 
# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()

# Get profile
profile = kite.profile()
print(profile)
```

## How to contribute

Refer this document how to contribute - https://github.com/jugaad-py/jugaad-trader/blob/master/contributing.md

## Articles and examples using Jugaad-Trader

https://marketsetup.in/tags/jugaad-trader/

