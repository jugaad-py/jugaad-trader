
import asyncio
import pathlib
import ssl
import json
import uuid
import os 
import websockets
from requests import Session
import certifi
from bs4 import BeautifulSoup
import json
import configparser
import click
from jugaad_trader.util import CLI_NAME


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhost_pem = certifi.where()
ssl_context.load_verify_locations(localhost_pem)

class Upstox:
    def __init__(self, client_id="", password="", twofa=""):
        self.client_id = client_id
        self.password = password
        self.twofa = twofa
        self.loop = asyncio.get_event_loop()
        self.event_tree = {}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Host": "pro.upstox.com",
        }
        self.s = Session()
        self.s.headers.update(headers)
        self.keys = { 
                    "apiId": "e6bb46d9d4b16dae8cf5173e047fa10ca1d79ec48d3e9fb747d4eabad8ba5313",
                    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJVUFNUT1hQUk9NQUlOIiwiYXVkIjoiVVBTVE9YUFJPTUFJTnxXRUIiLCJzdWIiOiJHZXQgU29ja2V0IENvbm5lY3Rpb24iLCJpYXQiOjE1OTc2NjM1Njg1NjUsImV4cCI6MTYwNzY2MzU2ODU2NX0.JUUdWtrfacqDiqUGQNEeeehCGid8HpiF08f3jrI-a8o"
    }

    def notification_handler(self, packet):
        print("Notification: " + packet)
    
    def load_creds(self, path=None):
        if path==None:
            path = os.path.join(click.get_app_dir(CLI_NAME), ".ucred")
        config = configparser.ConfigParser()
        try:
            config.read(path)
        except FileNotFoundError:
            raise FileNotFoundError("\n\nCould not find the credentials, Please save the credentials using \n\n$ jtrader upstox savecreds")
        creds = config['CREDENTIALS']
        self.client_id = creds['user_id']
        self.password = creds['password']
        self.twofa = creds['twofa']
    
    def get_root_js(self):
        url = "https://pro.upstox.com" + self.get_js_name()
        r = self.s.get(url)
        return r.text

    def get_api_key(self, js):
        s = js.split("var s='")[1]
        s = s.split("';")[0]
        j = json.loads(s)
        
        return j
 
    def get_js_name(self):
        url = "https://pro.upstox.com"
        r = self.s.get(url)
        bs = BeautifulSoup(r.text, features="html.parser")
        script = bs.find('script')
        return script['src']

    async def connect(self):
        j = self.keys 
        wss_url = "wss://ws.upstox.com/socket.io/?apiId={apiId}&token={token}&client_id={client_id}&ReleaseType=Green&deviceId=523739463&EIO=3&transport=websocket"
        wss_url = wss_url.format(apiId=j['apiId'], token=j['token'], client_id=self.client_id)
        self.url = wss_url
        headers = [("Host", "ws.upstox.com"), ("User-Agent", 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'),
                ("Accept-Language", "en-GB,en-US;q=0.9,en;q=0.8"), ("Origin", "https://pro.upstox.com")]
        self.websocket = await websockets.connect(self.url, ssl=ssl_context, origin="https://pro.upstox.com", extra_headers=headers)
        msg = await self.recv()
        msg = await self.recv()
        return msg
    
    async def send(self, msg):
        await self.websocket.send(msg)
    
    async def recv(self):
        return await self.websocket.recv()

    async def recv_forever(self):
        while(1):
            packet = await self.websocket.recv()
            if packet == '3':
                continue
            if packet[0:2] == '42':
                try:
                    msg = self.decode_packet(packet)
                    guid = msg['guid']
                    self.event_tree[guid]['result'] = msg
                    self.event_tree[guid]['event'].set()
                    continue
                except:
                    pass
                # guid = msg['']
            self.notification_handler(packet)


    def login(self):
        self.loop.run_until_complete(self.connect())
        self.loop.create_task(self.recv_forever())
        resp = self.client_login(client_id=str(self.client_id), password=self.password)
        resp = self.client_login2fa(password=str(self.twofa))
        self.loop.create_task(self.heart_beat())
        return resp

    async def heart_beat(self):
        while(1):
            await self.send('2')
            await asyncio.sleep(5)

    def create_packet(self, method_name, guid, **kwargs):
        payload = {"method": method_name, "type": "interactive", "guid": guid }
        payload["data"] = kwargs
        packet = '42' + json.dumps(["message", payload])
        return packet

    def decode_packet(self, packet):
        return json.loads(packet[2:])[1]
       
    def __getattr__(self, name):
        async def send_recv(**kwargs):
            guid = str(uuid.uuid4())
            msg = self.create_packet(method_name=name, guid=guid,  **kwargs)
            await self.send(msg)
            self.event_tree[guid] = {"event": asyncio.Event()}
            await self.event_tree[guid]["event"].wait()
            result = self.event_tree[guid]['result']
            del self.event_tree[guid]
            return result

        def factory(**kwargs):
            x = self.loop.run_until_complete(send_recv(**kwargs))
            return x
        return factory

    def place_order(self, **kwargs):
        pass

if __name__=="__main__":

    u = Upstox()
    u.load_creds()
    r = u.login()
    print(r)
    msg = u.get_client_info()
    print(msg)
    print(u.get_order_history())

    # print(u.event_tree)
  

    u.loop.run_until_complete(asyncio.sleep(100))



