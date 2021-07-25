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

How to contribute
*****************

Refer this document how to contribute -  `<https://github.com/jugaad-py/jugaad-trader/blob/master/contributing.md>`_

Articles and examples using Jugaad-Trader
*****************************************


`How to Log into your Zerodha account using Python`__
---------------------------------------------------

.. _article1: https://marketsetup.in/posts/zerodha-login/

__ article1_

A simple article which explains the basics on which this library is built


`Download data from Zerodha using python script`__
---------------------------------------------------

.. _article2: https://marketsetup.in/posts/download-stock-data-zerodha/

__ article2_

This is a simple script based on jugaad-trader library to download minute interval data for any instrument (stock, futures, options and indices).

`How to trade with python in Zerodha`__
---------------------------------------------------

.. _article3: https://marketsetup.in/posts/how-to-trade-with-python-in-zerodha/

__ article3_

Article shows how you can use Jugaad-Trader to place orders automatically

