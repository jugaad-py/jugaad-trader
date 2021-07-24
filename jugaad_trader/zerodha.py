import csv
import json
import hashlib
import logging
import datetime
import time
import operator
import json
import configparser
import os
import pickle


import requests
import click
from six.moves.urllib.parse import urljoin


from kiteconnect import KiteConnect, KiteTicker
import kiteconnect.exceptions as ex
from bs4 import BeautifulSoup

from jugaad_trader.util import CLI_NAME


log = logging.getLogger(__name__)

base_url = "https://kite.zerodha.com"
login_url = "https://kite.zerodha.com/api/login"
twofa_url = "https://kite.zerodha.com/api/twofa"
instruments_url = "https://api.kite.trade/instruments"
class Zerodha(KiteConnect):
    """
        TO DO:
        instruments - Deviation from KiteConnect
        
        
    """
    _default_root_uri = "https://kite.zerodha.com"
    def __init__(self, user_id=None, password=None, twofa=None):
    
        self.user_id = user_id
        self.password = password
        self.twofa = twofa
    
        super().__init__(api_key="")
        self.s = self.reqsession = requests.Session()
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                    }
        self.reqsession.headers.update(headers)
        self.chunkjs = {}
        self.url_patch = '/oms'
        # self._routes["user.profile"] = "/user/profile/full"

    def set_access_token(self):
        self.load_session()

    def load_session(self, path=None):
        
        if path==None:
            path = os.path.join(click.get_app_dir(CLI_NAME), ".zsession")
        try:
            with open(path, "rb") as fp:
                self.reqsession = pickle.load(fp)
        except FileNotFoundError:
            raise FileNotFoundError("\n\nCould not find the session, Please start a session using \n\n$ jtrader zerodha startsession")
        self.enc_token = self.reqsession.cookies['enctoken']
        self.user_id = self.reqsession.cookies['user_id']

    def load_creds(self, path=None):
        if path==None:
            path = os.path.join(click.get_app_dir(CLI_NAME), ".zcred")
        config = configparser.ConfigParser()
        try:
            config.read(path)
        except FileNotFoundError:
            raise FileNotFoundError("\n\nCould not find the credentials, Please save the credentials using \n\n$ jtrader zerodha savecreds")
        creds = config['CREDENTIALS']
        self.user_id = creds['user_id']
        self.password = creds['password']
        self.twofa = creds['twofa']

    def _user_agent(self):
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
    
    def login_step1(self):
        self.r = self.reqsession.get(base_url)
        self.r = self.reqsession.post(login_url, data={"user_id": self.user_id, "password":self.password})
        j = json.loads(self.r.text)
        return j

    def login_step2(self, j):
        data = {"user_id": self.user_id, "request_id": j['data']["request_id"], "twofa_value": self.twofa }
        self.r = self.s.post(twofa_url, data=data)
        j = json.loads(self.r.text)
        return j


    def login(self):
        j = self.login_step1()
        if j['status'] == 'error':
            raise Exception(j['message'])
        
        j = self.login_step2(j)
        if j['status'] == 'error':
            raise Exception(j['message'])
        self.enc_token = self.r.cookies['enctoken']
        return j

    def custom_headers(self):
        h = {}
        h['authorization'] = "enctoken {}".format(self.enc_token)
        h['referer'] = 'https://kite.zerodha.com/dashboard'
        h['x-kite-version'] = '2.9.2'
        h['sec-fetch-site'] = 'same-origin'
        h['sec-fetch-mode'] = 'cors'
        h['sec-fetch-dest'] = 'empty'
        h['x-kite-userid'] = self.user_id
        return h
    
    def _request(self, route, method, url_args=None, params=None,
                 is_json=False, query_params=None):
        if url_args:
            uri = self._routes[route].format(**url_args)
        else:
            uri = self._routes[route] 

        url = urljoin(self.root, self.url_patch + uri)
        
        # prepare url query params
        if method in ["GET", "DELETE"]:
            query_params = params


        # Custom headers
        headers = self.custom_headers()

        if self.debug:
            log.debug("Request: {method} {url} {params} {headers}".format(method=method, url=url, params=params, headers=headers))

        try:
            r = self.reqsession.request(method,
                                        url,
                                        json=params if (method in ["POST", "PUT"] and is_json) else None,
                                        data=params if (method in ["POST", "PUT"] and not is_json) else None,
                                        params=query_params,
                                        headers=headers,
                                        verify=not self.disable_ssl,
                                        allow_redirects=True,
                                        timeout=self.timeout,
                                        proxies=self.proxies)
            self.r = r
        except Exception as e:
            raise e

        if self.debug:
            log.debug("Response: {code} {content}".format(code=r.status_code, content=r.content))

        # Validate the content type.
        if "json" in r.headers["content-type"]:
            try:
                data = json.loads(r.content.decode("utf8"))
            except ValueError:
                raise ex.DataException("Couldn't parse the JSON response received from the server: {content}".format(
                    content=r.content))

            # api error
            if data.get("status") == "error" or data.get("error_type"):
                # Call session hook if its registered and TokenException is raised
                if self.session_expiry_hook and r.status_code == 403 and data["error_type"] == "TokenException":
                    self.session_expiry_hook()

                # native Kite errors
                exp = getattr(ex, data.get("error_type"), ex.GeneralException)
                raise exp(data["message"], code=r.status_code)

            return data["data"]
        elif "csv" in r.headers["content-type"]:
            return r.content
        else:
            raise ex.DataException("Unknown Content-Type ({content_type}) with response: ({content})".format(
                content_type=r.headers["content-type"],
                content=r.content))
    
    def get_chunk_js(self):
        self.r = self.reqsession.get(urljoin(base_url, '/dashboard'))
        html = self.r.text
        bs = BeautifulSoup(html)
        for tag in bs.find_all("link"):
            src = tag.attrs.get("href", "")
            if "chunk" in src:
                break
        url = urljoin(base_url, tag.attrs.get("href"))
        self.r = self.reqsession.get(url)
        return self.r.text
    
    def chunk_to_json(self, js):
        start = js.find('{"months"')
        end = js.find("\')}}])")
        jtxt = js[start:end].replace('\\','')
        self.chunkjs = json.loads(jtxt)
        return self.chunkjs
    
    def instruments(self, exchange=None):
        if exchange:
            self.r = self.reqsession.get(instruments_url + "/{}".format(exchange))
        else:
            self.r = self.reqsession.get(instruments_url)
        return self._parse_instruments(self.r.text)
        
    def close(self):
        self.reqsession.close()
   
    
    def ticker(self, api_key='kitefront', enctoken=None, userid=None):
        if enctoken is not None:
            self.enctoken = self.r.cookies['enc_token']
        if userid is not None:
            self.user_id = self.user_id
        if self.user_id is None:
            raise Exception("\nCould not find the session, Please start a session using \n\n$ jtrader zerodha startsession")
        return KiteTicker(api_key=api_key, access_token=self.enc_token+'&user_id='+self.user_id, root='wss://ws.zerodha.com')
                            
class Console(Zerodha):
    """
        Experimental support for Zerodha backoffice platform Coin
    """
    _default_root_uri = "https://console.zerodha.com"
    api_key = "console" # API key for Coin
    _routes = {
        "login":"/kite/login",
        "status": "/api/user/status",
        "user_profile": "/api/user_profile/status",
        "dashboard": "/api/dashboard",
        "account_values": "/api/dashboard/account_values",
        "positions": "/api/reports/positions",
        "exposure": "/api/reports/positions/exposure",
        "portfolio": "/api/reports/holdings/portfolio",
        "tradebook": "/api/reports/tradebook",
        "pnl": "/api/reports/pnl",
        "pnl_summary": "/api/reports/pnl/summary",
        "tax_pnl": "/api/reports/taxpnl",
        "fund_balance": "https://console.zerodha.com/api/funds/balance",
        "ledger": "/api/ledger",
        "interest_statement": "/api/funds/interest_statement",
        "mandate": "/api/mandate"
    }
    def __init__(self, z):
        """
            args:
                z - Instance of Zerodha class
        """
        
        super().__init__(z.user_id, z.password, z.twofa)
        self._root = self._default_root_uri

        self.url_patch = ""
        self.reqsession = z.reqsession
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                    }
        self.reqsession.headers.update(headers)
        self.console_session = "" 
        self.public_token = "" 
        self.register_functions() 
    def custom_headers(self):
        h = {}
        h['referer'] = 'https://console.zerodha.com/'
        h['x-kite-version'] = '3'
        h['sec-fetch-site'] = 'same-origin'
        h['sec-fetch-mode'] = 'cors'
        h['sec-fetch-dest'] = 'empty'
        h['user-agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"

        return h
    

    def login(self):
        """
            Get request to /login redirects to kite, if the Kite session is
            already active, You are redirected back to Console and logged in
            automatically            
        """
        url = self._root + self._routes["login"]
        self.r = self.reqsession.get(url) 
        if self.r.url == 'https://console.zerodha.com/dashboard':
            cookies = self.reqsession.cookies.get_dict('console.zerodha.com')
            self.console_session = cookies['session']
            return True
        else:
            raise Exception("Login failed or Kite session expired")
    
    def factory_functions(self, route, docstring=""):
        """
            All APIs used by console end up sendinga a get request with some
            data, hence creating a fatory function which will generate a
            function to send GET requests
        """
        def generic_function(**kwargs):
            return self._get(route, params=kwargs)
        generic_function.__doc__ = docstring
        return generic_function
    
    def register_functions(self):
        self.dashboard = self.factory_functions("dashboard")
        self.account_values = self.factory_functions("account_values")
        self.positions = self.factory_functions("positions")
        self.exposure = self.factory_functions("exposure")
        self.portfolio = self.factory_functions("portfolio")
        self.tradebook = self.factory_functions("tradebook")
        self.pnl = self.factory_functions("pnl")
        self.pnl_summary = self.factory_functions("pnl_summary")
        self.tax_pnl = self.factory_functions("tax_pnl")
        self.fund_balance = self.factory_functions("fund_balance")
        self.ledger = self.factory_functions("ledger")
        self.interest_statement = self.factory_functions("interest_statement")
        self.mandate = self.factory_functions("mandate")
   
if __name__=="__main__":
    pass
