# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 23:05:57 2021

@author: Daniel
"""

import requests
import pandas as pd

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


#res2 returns response200
res2 = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
                   params={'symbols': ticker, 'greeks': 'false'},
                   headers={'Authorization': btoke, 'Accept': 'application/json'})


res2.json()
print(res2.status_code)
print(res2)





listy_ = ['symbol','description','strike','root_symbol','option_type','bid','ask','open_interest','volume']



#bid,ask,symbol,description,volume,open_interest,option_type,root_symbol,strike
#define expiry dates, convert dict to dataframe

nest1 = json_response['options']
nest2 = nest1['option']
x = pd.DataFrame.from_dict(nest2)

x = x[x.columns.intersection(listy_)]