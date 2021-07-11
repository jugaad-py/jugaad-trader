*************
Jugaad Trader
*************

Alternate python library for Zerodha Kite connect API.

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

You may find this other jugaad (Jugaad-Data_) interesting, its a simple library to fetch data from NSE.

.. _Jugaad-Data: https://marketsetup.in/documentation/jugaad-data/


Articles and examples using Jugaad-Trader
*****************************************


`How to Log into your Zerodha account using Python`__

.. _article1: https://marketsetup.in/posts/zerodha-login/

__ article1_

A simple article which explains the basics on which this library is built
