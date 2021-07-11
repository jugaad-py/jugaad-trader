import unittest

import os
import configparser

import pytest
from jugaad_trader import Zerodha, Console

config = configparser.ConfigParser()
try:
    home_folder = os.path.expanduser('~')
    config.read(os.path.join(home_folder, '.config', 'jtrader', '.zcred'))
    config['CREDENTIALS']
except:
    Exception("Credentials not found")

creds = config['CREDENTIALS']
z = Zerodha(creds['user_id'],
            creds['password'],
            creds['twofa'])

c = Console(z)
def test_console_login():
    # Should raise exception if not logged in to Zerodha
    with pytest.raises(Exception):
        c.login()
    # Should login normally
    z.login()
    assert c.login()

def dry_tester(v):
    assert v['state'] in ['PENDING', 'SUCCESS']
    assert 'result' in v

def test_dashboard():
    v = c.dashboard()
    dry_tester(v)

def test_account_values():
    v = c.account_values()
    dry_tester(v)

def test_positions():
    v = c.positions(date="2021-07-19", segment="FO")
    dry_tester(v)

def test_exposure():
    v = c.exposure(segment="FO", date="2021-07-09")
    dry_tester(v)

def test_portfolio():
    v = c.portfolio(date="2021-07-11")
    dry_tester(v)

def test_tradebook():
    v = c.tradebook(segment="EQ",
                    from_date="2021-06-11",
                    to_date="2021-07-11",
                    page=1)
    dry_tester(v)
    v = c.tradebook(segment="FO",
                    from_date="2021-06-11",
                    to_date="2021-07-11",
                    page=1)
    dry_tester(v)

def test_pnl_and_summary():
    v = c.pnl(segment="EQ",
              from_date="2021-06-11",
              to_date="2021-07-11",
              view_type="combined",
              sort_by="tradingsymbol",
              sort_desc="false",
              page="1")
    dry_tester(v)
    v = c.pnl(segment="FO",
              from_date="2021-06-11",
              to_date="2021-07-11",
              view_type="combined",
              sort_by="tradingsymbol",
              sort_desc="false",
              page="1")

    dry_tester(v)
    v = c.pnl_summary(segment="EQ",
              from_date="2021-06-11",
              to_date="2021-07-11",
              view_type="combined",
              sort_by="tradingsymbol",
              sort_desc="false",
              page="1")
    dry_tester(v)
    v = c.pnl_summary(segment="FO",
              from_date="2021-06-11",
              to_date="2021-07-11",
              view_type="combined",
              sort_by="tradingsymbol",
              sort_desc="false",
              page="1")

    dry_tester(v)


def test_tax_pnl():
    v = c.tax_pnl(fy="2020_2021",
                  from_quarter="Q1",
                  to_quarter="Q2")
    dry_tester(v)

def test_fund_balance():
    v = c.fund_balance()
    dry_tester(v)


def test_ledger():
    v = c.ledger(segment="EQ",
                 from_date="2021-07-04",
                 to_date="2021-07-11",
                 page="1")
    dry_tester(v)
