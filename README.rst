*************
Jugaad Trader
*************

Unofficial Upstox & Zerodha Client library


Documentation
#############


`<https://marketsetup.in/documentation/jugaad-trader/>`_


Installation
############
::

    $ pip install jugaad-trader

Quick start for Zerodha
***********************

Library provides a CLI to manage your session/credentials. It is not recommended to use the credentials directly in the code.

**Step 1** - Start session using your zerodha credentials
::

    $ jtrader zerodha startsession
    User ID >: Zerodha User Id
    Password >: 
    Pin >: 
    Logged in successfully


**Step 2** - Start using it in the code

.. code-block:: python

    from jugaad_trader import Zerodha
    kite = Zerodha()
    kite.set_access_token()
    print(kite.profile())

For more details please visit `<https://marketsetup.in/documentation/jugaad-trader/>`_









