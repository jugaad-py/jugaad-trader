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

class ZerodhaTicker(KiteTicker):
    ROOT_URI = "wss://ws.zerodha.com/"
    def __init__(self, user_id, enc_token, debug=False, 
                                            root=None, reconnect=True,
                                            reconnect_max_tries=KiteTicker.RECONNECT_MAX_TRIES,
                                            reconnect_max_delay=KiteTicker.RECONNECT_MAX_DELAY,
                                            connect_timeout=KiteTicker.CONNECT_TIMEOUT):
        super(ZerodhaTicker, self).__init__(api_key="", access_token="",
                                            debug=debug, root=root,
                                            reconnect=reconnect,
                                            reconnect_max_tries=reconnect_max_tries,
                                            reconnect_max_delay=reconnect_max_delay,
                                            connect_timeout=connect_timeout)

        uid = int(time.time())*1000
        self.socket_url = "{root}?api_key=kitefront"\
                          "&user_id={user_id}&enctoken={enc_token}&uid={uid}&user-agent=kite3-web&version=2.4.0".format(
                              root=self.ROOT_URI,
                              user_id=user_id,
                              enc_token=enc_token,
                              uid=uid)
 
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
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                    }
        self.reqsession.headers.update(headers)
        self.chunkjs = {}
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
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    
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

    def oms_headers(self):
        h = {}
        h['authorization'] = "enctoken {}".format(self.enc_token)
        h['referer'] = 'https://kite.zerodha.com/dashboard'
        h['x-kite-version'] = '2.4.0'
        h['sec-fetch-site'] = 'same-origin'
        h['sec-fetch-mode'] = 'cors'
        h['sec-fetch-dest'] = 'empty'
        h['x-kite-userid'] = self.user_id
        return h
    
    def _request(self, route, method, parameters=None):
        """Make an HTTP request."""
        params = parameters.copy() if parameters else {}

        # Form a restful URL
        uri = self._routes[route].format(**params)
        url = urljoin(self.root, '/oms' + uri)

        # Custom headers
        headers = self.oms_headers()

        if self.debug:
            log.debug("Request: {method} {url} {params} {headers}".format(method=method, url=url, params=params, headers=headers))

        try:
            r = self.reqsession.request(method,
                                        url,
                                        data=params if method in ["POST", "PUT"] else None,
                                        params=params if method in ["GET", "DELETE"] else None,
                                        headers=headers,
                                        verify=not self.disable_ssl,
                                        allow_redirects=True,
                                        timeout=self.timeout,
                                        proxies=self.proxies)
            self.r = r
        # Any requests lib related exceptions are raised here - http://docs.python-requests.org/en/master/_modules/requests/exceptions/
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
            if data.get("error_type"):
                # Call session hook if its registered and TokenException is raised
                if self.session_expiry_hook and r.status_code == 403 and data["error_type"] == "TokenException":
                    self.session_expiry_hook()

                # native Kite errors
                exp = getattr(ex, data["error_type"], ex.GeneralException)
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
            # print(src)
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
   
    
    def ticker(self):
        return ZerodhaTicker(self.user_id, self.enc_token)
                            
if __name__=="__main__":
    pass
