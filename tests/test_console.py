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
    assert v['state'] == 'SUCCESS'
    assert 'result' in v

def test_dashboard():
    v = c.dashboard()
    dry_tester(v)

def test_account_values():
    v = c.account_values()
    dry_tester(v)

      
