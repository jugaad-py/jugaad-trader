import pytest
import unittest
import os
import configparser
import re
import json
import click
from jugaad_trader import Upstox
u = Upstox()
u.load_creds()

def test_js_name():
    js_name = u.get_js_name()
    assert '/Root' == js_name[0:5]
    assert js_name.split('.')[-1] == 'js'

def test_get_root_js():
    js = u.get_root_js()
    assert "apiId" in js

def test_get_api_keys():
    js = u.get_root_js()
    j = u.get_api_key(js)
    assert "WS" in j    
    assert "apiId" in j["WS"] 

@pytest.mark.asyncio
async def test_connect():
    d = await u.connect()
    assert d == '40'

def test_functionality():
    d = u.login()
    assert d['data']['success']  
    params = {"exchange":"NSE_EQ","token":"3045","symbol":"SBIN","series":"EQ","is_amo":True,"order_complexity":"SIMPLE","order_type":"L","product":"I","duration":"DAY","transaction_type":"B","price":"180","trigger_price":"0","disclosed_quantity":"0","quantity":"1"}


def test_js_regex():
    js = """use strict";Object.defineProperty(exports,"__esModule",{value:!0});var s='{"WS_TOKEN":{"private_key":"025d8c92217c731b3c1d4dc5d34cc0df219171396ca53f0c37afae52689b805a","options":{"iss":"UPSTOXPROMAIN","aud":"UPSTOXPROMAIN|WEB","sub":"Get Socket Connection"}},"HTTP":{"/payin.upstox/":"https://payin.upstox.com/","/payin.lien/":"https://payin.upstox.com/","/rest-pro/":"https://rest-pro.upstox.com/","/amazon-south-1/":"https://s3.ap-south-1.amazonaws.com/","/api-upstox/":"https://api.upstox.com/","/profile/":"https://profile.upstox.com","/symbol-search/":"https://symbol-search.upstox.com/search","/symbol-token-search/":"https://symbol-search.upstox.com/searchByToken","/option-expiry-search/":"https://symbol-search.upstox.com/getOptionExpiries","/option-strike-search/":"https://symbol-search.upstox.com/getStrikes","/notifications/":"https://service-request-api.upstox.com/api/notifications/","/edis/":"https://edis.upstox.com/","/cdsl-form-data/":"https://edis.cdslindia.com/EDIS/VerifyDIS","/upstox-amazon/":"https://upstoxpro.s3.ap-south-1.amazonaws.com/"},"WS":{"apiId":"e6bb46d9d4b16dae8cf5173e047fa10ca1d79ec48d3e9fb747d4eabad8ba5313","url":"wss://ws.upstox.com","params":{"ReleaseType":"Blue"}},"MIXPANEL_KEY":"62597aa51842e6e2c56b97d96e4c5f8a","HOTJAR":{"HOTJAR_MODE_ID":6,"HOTJAR_KEY":1611487},"EXTERNAL_LINKS":{"MY_UPSTOX":"https://my.upstox.com/profile","REFER":"https://my.upstox.com/refer-and-earn","HELP":"https://upstox.com/announcements","TICKET":"https://upstox.freshdesk.com/support/tickets/new","ACTIVATE":"https://profile.upstox.com/"},"WS_LOGINLESS":{"apiId":"0586dcebbca0289b58e6e54fc69f63dd761fcde71905615b8d47504d13f4055e","url":"wss://loginless.upstox.com","params":{"ReleaseType":"Green"}},"WS_TOKEN_LOGINLESS":{"private_key":"42f605758cb095c4a2c1895292b2cd1a103318879d9e8b2192cf80cef520b107","options":{"iss":"UPSTOXLOGINLESS","aud":"UPSTOXLOGINLESS|WEB","sub":"Get Socket Connection"}}}';exports.default="string"==typeof s?JSON.parse(s):s;"""
    s = js.split("var s='")[1]
    assert s[2:10] == "WS_TOKEN"
    s = s.split("';")[0]
    assert s[-3:-1] == '}}'
    j = json.loads(s)
    assert "WS" in j    
    assert "apiId" in j["WS"] 


