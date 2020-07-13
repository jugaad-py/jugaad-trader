import unittest
import os
import configparser

import click
from jugaad_trader import Zerodha

config = configparser.ConfigParser()
try:
    home_folder = os.path.expanduser('~')
    config.read(os.path.join(home_folder, '.zcreds'))
except:
    Exception("Credentials not found")

class TestZerodhaInit(unittest.TestCase):

    def test_init(self):
        self.assertEqual(1,2)

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
        self.assertEqual(self.step1_result['status'], 'success')
        self.assertIn('enctoken', self.z.r.cookies)

    def seq4_login_valid_creds(self):
        j = self.z.login()
        self.assertEqual(self.step1_result['status'], 'success')
    
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
        for i, (name, step) in enumerate(self._steps()):
            try:
                step()
                click.echo(".")
            except Exception as e:
                self.fail("{} failed ({}: {})".format(step, type(e), e))
        click.echo('Completed {} sub-tests'.format(i))
    
    def test_login_step1_invalid_creds(self):
        z = Zerodha("randomcreds", "randomstring123324", "2231212")
        step1_result = z.login_step1()
        self.assertEqual(step1_result['status'], 'error')
        z.close()
    
    def test_init_without_creds(self):
        z = Zerodha()
        self.assertEqual(z.user_id, self.z.user_id)
    
    def tearDown(self):
        self.z.close()

if __name__=="__main__":


    unittest.main()
