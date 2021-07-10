import unittest
import os
import configparser

import click
from jugaad_trader import Zerodha

config = configparser.ConfigParser()
try:
    home_folder = os.path.expanduser('~')
    config.read(os.path.join(home_folder, '.config', 'jtrader', '.zcred'))
    config['CREDENTIALS']
except:
    Exception("Credentials not found")


class TestZerodhaLogin(unittest.TestCase):
    creds = config['CREDENTIALS']
    z = Zerodha(creds['user_id'],
                creds['password'],
                creds['twofa'])
    
    def seq1_login_step1_valid_creds(self):
        self.step1_result = self.z.login_step1()
        self.assertEqual(self.step1_result['status'], 'success')
    
    def seq2_login_step2_invalid_creds(self):
        self.z.twofa = "3423122" # random str
        j = self.z.login_step2(self.step1_result)
        self.assertEqual(j['status'], 'error')
        # switch back to original
        self.z.twofa = self.creds['twofa']

    def seq3_login_step2_valid_creds(self):
        j = self.z.login_step2(self.step1_result)
        self.assertEqual(j['status'], 'success')
        self.assertIn('enctoken', self.z.r.cookies)

    def seq4_login_valid_creds(self):
        j = self.z.login()
        self.assertEqual(j['status'], 'success')
    
    def seq5_login_invalid_pass(self):
        self.z.password = "somerandompassword"
        with self.assertRaises(Exception):
            self.z.login()
        self.z.password = self.creds['password']
    
    def seq6_login_invalid_2fa(self):
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
        self.z.login()
        l = self.z.ltp(408065)
        self.assertIn('408065', l)

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

