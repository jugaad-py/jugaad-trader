
import json
from requests import Session 
base_url = "https://kite.zerodha.com"
login_url = "https://kite.zerodha.com/api/login"
twofa_url = "https://kite.zerodha.com/api/twofa"
full_profile_url = "https://kite.zerodha.com/oms/user/profile/full"
margins_url = "https://kite.zerodha.com/oms/user/margins"
holdings_url = "https://kite.zerodha.com/oms/portfolio/holdings"
positions_url = "https://kite.zerodha.com/oms/portfolio/positions"
orders_url = "https://kite.zerodha.com/oms/orders"
gtt_triggers_url = "https://kite.zerodha.com/oms/gtt/triggers"

place_order_url = "https://kite.zerodha.com/oms/orders/{variety}"
order_cancel_url = "https://kite.zerodha.com/oms/orders/{variety}/{order_id}"
# Instruments - https://kite.zerodha.com/static/js/chunk-2d22c101.f181d8c9.js


class Zerodha:
    PRODUCT_MIS = "MIS"
    PRODUCT_CNC = "CNC"
    PRODUCT_NRML = "NRML"
    PRODUCT_CO = "CO"
    PRODUCT_BO = "BO"

    # Order types
    ORDER_TYPE_MARKET = "MARKET"
    ORDER_TYPE_LIMIT = "LIMIT"
    ORDER_TYPE_SLM = "SL-M"
    ORDER_TYPE_SL = "SL"

    # Varities
    VARIETY_REGULAR = "regular"
    VARIETY_BO = "bo"
    VARIETY_CO = "co"
    VARIETY_AMO = "amo"

    # Transaction type
    TRANSACTION_TYPE_BUY = "BUY"
    TRANSACTION_TYPE_SELL = "SELL"

    # Validity
    VALIDITY_DAY = "DAY"
    VALIDITY_IOC = "IOC"

    # Exchanges
    EXCHANGE_NSE = "NSE"
    EXCHANGE_BSE = "BSE"
    EXCHANGE_NFO = "NFO"
    EXCHANGE_CDS = "CDS"
    EXCHANGE_BFO = "BFO"
    EXCHANGE_MCX = "MCX"

    # Margins segments
    MARGIN_EQUITY = "equity"
    MARGIN_COMMODITY = "commodity"

    # Status constants
    STATUS_COMPLETE = "COMPLETE"
    STATUS_REJECTED = "REJECTED"
    STATUS_CANCELLED = "CANCELLED"

    # GTT order type
    GTT_TYPE_OCO = "two-leg"
    GTT_TYPE_SINGLE = "single"

    # GTT order status
    GTT_STATUS_ACTIVE = "active"
    GTT_STATUS_TRIGGERED = "triggered"
    GTT_STATUS_DISABLED = "disabled"
    GTT_STATUS_EXPIRED = "expired"
    GTT_STATUS_CANCELLED = "cancelled"
    GTT_STATUS_REJECTED = "rejected"
    GTT_STATUS_DELETED = "deleted"
    def __init__(self, user_id, password, twofa):
        self.user_id = user_id
        self.password = password
        self.twofa = twofa
        self.s = Session()
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            # "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                    }
        self.s.headers.update(headers)
    
    def login(self):
        self.r = self.s.get(base_url)
        self.r = self.s.post(login_url, data={"user_id": self.user_id, "password":self.password})
        j = json.loads(self.r.text)
        data = {"user_id": self.user_id, "request_id": j['data']["request_id"], "twofa_value": self.twofa }
        self.r = self.s.post(twofa_url, data=data)
        j = json.loads(self.r.text)
        # self.public_token = j['data']['public_token']
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
    def oms_get(self, url):
        h = self.oms_headers()
        self.r = self.s.get(url, headers=h)
        j = json.loads(self.r.text)
        return j

    def oms_post(self, url, data):
        h = self.oms_headers()
        self.r = self.s.post(url, data=data, headers=h)
        j = json.loads(self.r.text)
        return j
    
    def oms_delete(self, url):
        h = self.oms_headers()
        self.r = self.s.delete(url, headers=h)
        j = json.loads(self.r.text)
        return j

    def full_profile(self):
        return self.oms_get(url=full_profile_url)
    
    def margins(self):
        return self.oms_get(url=margins_url)


    def holdings(self):
        return self.oms_get(url=holdings_url)

    
    def positions(self):
        return self.oms_get(url=positions_url)

    
    def orders(self):
        return self.oms_get(url=orders_url)


    def gtt_triggers(self):
        return self.oms_get(url=gtt_triggers_url)
    
    def place_order(self,
                    variety,
                    exchange,
                    tradingsymbol,
                    transaction_type,
                    quantity,
                    order_type,
                    product="CNC",
                    price=0,
                    validity="DAY",
                    disclosed_quantity=0,
                    trigger_price=0,
                    squareoff=0,
                    stoploss=0,
                    trailing_stoploss=0):
            params = locals()
            del(params["self"])
            url = place_order_url.format(variety=params['variety'])
            params['user_id'] = self.user_id
            return self.oms_post(url, params)

    def cancel_order(self, variety, order_id, parent_order_id=None):
        url = order_cancel_url.format(variety=variety, order_id=order_id)
        return self.oms_delete(url)





        
    
if __name__=="__main__":
    import os
    cwd = os.getcwd()
    print(cwd)
    with open('./env/zerodha.json','r') as fp:
        creds = json.load(fp)
        user_id = creds['user_id']
        password = creds['password']
        twofa = creds['twofa']
        print(creds)
    z = Zerodha(user_id, password, twofa)
    # Log into account
    status = z.login()
    print(status)

    # Get profile
    profile = z.full_profile()
    print(profile)

    # Get margin
    margins = z.margins()
    print(margins)

    # Get holdings
    holdings = z.holdings()
    print(holdings)

    # Get today's positions
    positions = z.positions()
    print(positions)

    # Get today's orders
    orders = z.orders()
    print(orders)

    # Finally placing an order
    order_resp = z.place_order(variety=z.VARIETY_REGULAR,
                                tradingsymbol="INFY",
                                exchange=z.EXCHANGE_NSE,
                                transaction_type=z.TRANSACTION_TYPE_BUY,
                                quantity=1,
                                order_type=z.ORDER_TYPE_MARKET,
                                product=z.PRODUCT_CNC)
    print(order_resp)
