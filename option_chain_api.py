# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 23:05:57 2021

@author: Daniel
"""

import requests
import pandas as pd
from yahoofinancials import YahooFinancials as yf

ticker = 'SPY'
toke = 'H4WiYj0CVcFpz7hZeFpj9uxKJxcJ'
btoke = r'Bearer {}'.format(toke)
expiry = '2021-09-17'

res = requests.get('https://sandbox.tradier.com/v1/markets/options/chains',
                   params={'symbol':ticker,'expiration': expiry , 'greeks': 'false'},
                   headers={'Authorization': btoke,'Accept': 'application/json'})

json_response = res.json()

print(res.status_code)
print(json_response)


#ideally best not to call from 2 api's but tradier not working
yf1 = yf(ticker)
ticker_price = yf1.get_current_price()











#bid,ask,symbol,description,volume,open_interest,option_type,root_symbol,strike
#define expiry dates, convert dict to dataframe

listy_ = ['symbol','description','strike','root_symbol','option_type','bid','ask','open_interest','volume']

nest1 = json_response['options']
nest2 = nest1['option']
x = pd.DataFrame.from_dict(nest2)
x = x[x.columns.intersection(listy_)]