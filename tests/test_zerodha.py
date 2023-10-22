import unittest
import os
import configparser
import pickle
import datetime

import click
import pyotp
from jugaad_trader import Zerodha
from jugaad_trader.util import CLI_NAME
from loguru import logger

app_dir = click.get_app_dir(CLI_NAME)
config = configparser.ConfigParser()
try:
    home_folder = os.path.expanduser('~')
    config.read(os.path.join(home_folder, '.config', 'jtrader', '.zcred'))
    config['CREDENTIALS']
except:
    Exception("Credentials not found")


class TestZerodhaLogin(unittest.TestCase):
    creds = config['CREDENTIALS']
    otp_gen = pyotp.TOTP(creds['twofa'])
    

    z = Zerodha(creds['user_id'],
                creds['password'],
                otp_gen.now())
    
    def seq1_login_step1_valid_creds(self):
        self.step1_result = self.z.login_step1()
        self.assertEqual(self.step1_result['status'], 'success')
    


    def seq2_login_step2_valid_creds(self):
        logger.info(self.step1_result)
        j = self.z.login_step2(self.step1_result)
        logger.info(j)
        self.assertEqual(j['status'], 'success')
        self.assertIn('enctoken', self.z.r.cookies)

    def seq3_login_valid_creds(self):
        j = self.z.login()
        self.assertEqual(j['status'], 'success')
    
    def seq4_login_invalid_pass(self):
        self.z.password = "somerandompassword"
        with self.assertRaises(Exception):
            self.z.login()
        self.z.password = self.creds['password']
    
    def seq5_login_invalid_2fa(self):
        self.z.twofa = "939344"
        with self.assertRaises(Exception):
            self.z.login()
        self.z.password = self.creds['twofa']



    def _steps(self):
        for name in dir(self): # dir() result is implicitly sorted
            if name.startswith("seq"):
                yield name, getattr(self, name)

    def test_steps(self):
        click.echo("test-sequence(", nl=False)
        for i, (_, step) in enumerate(self._steps()):
            try:
                step()
                click.echo("{}".format(i+1), nl=False)
            except Exception as e:
                self.fail("{} failed ({}: {})".format(step, type(e), e))
        click.echo(")", nl=False)
    
    def test_login_step1_invalid_creds(self):
        z = Zerodha("randomcreds", "randomstring123324", "2231212")
        step1_result = z.login_step1()
        self.assertEqual(step1_result['status'], 'error')
        z.close()
    
    def test_ltp(self):
        self.z.twofa = self.otp_gen.now()
        self.z.login()
        l = self.z.ltp(408065)
        self.assertIn('408065', l)
    
    def test_history(self):
        self.z.twofa = self.otp_gen.now()
        self.z.login()
        token = '128083204'
        from_date = (datetime.datetime.now() - datetime.timedelta(days=20)).date()
        to_date = datetime.datetime.now().date()
        logger.info(f"{token}, {from_date} {to_date}")
        data  = self.z.historical_data(token, from_date, to_date, interval='day')

        assert len(data) > 5
        
    def tearDown(self):
        self.z.close()



def test_instrument():
    z = Zerodha("randomcreds", "randomstring123324", "2231212")
    instr = z.instruments()
    assert len(instr) > 100
    instr = z.instruments("NSE")
    assert len(instr) > 100
    
if __name__=="__main__":
    
    unittest.main()

