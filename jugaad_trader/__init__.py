import os
# Moved to top to avoid circuilar imports (CLI_NAME will be required by zerodha.py and upstox.py for loading config)
CLI_NAME = "jtrader"

if not os.environ.get("SETUP"):
    from .zerodha import Zerodha
    from .upstox import Upstox

__version__ = "0.2alpha"