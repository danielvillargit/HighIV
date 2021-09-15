# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 23:05:57 2021

@author: Daniel
"""

import requests
import pandas as pd
from yahoofinancials import YahooFinancials as yf
from selenium_barchart_2 import *

def main():
    
    ticker_data_selenium = OptionSearch()
    ticker_data_selenium.BarchartImport()
    
    ticker = ticker_data_selenium.OptionImport()
    toke = 'H4WiYj0CVcFpz7hZeFpj9uxKJxcJ'
    btoke = r'Bearer {}'.format(toke)
    column_list = ['symbol','root_symbol','description','strike','bid','ask','option_type','open_interest','volume']
    
    
    #go back and calculate the expiry for weekly and monthly options
    expiry = '2021-09-17'
    
    import_chain2 = pd.DataFrame(data=None,columns=column_list)
    
    for tick_ in ticker:
        
        res = requests.get('https://sandbox.tradier.com/v1/markets/options/chains',
                           params={'symbol':tick_,'expiration': expiry , 'greeks': 'false'},
                           headers={'Authorization': btoke,'Accept': 'application/json'})
        
        json_response = res.json()
        
        print(res.status_code)
        print(json_response)
    
    #ideally best not to call from 2 api's but tradier not working
        yf1 = yf(tick_)
        ticker_price = yf1.get_current_price()
        
        
        nest1 = json_response['options']['option']
        import_chain = pd.DataFrame.from_dict(nest1)
        import_chain = import_chain[import_chain.columns.intersection(column_list)]
        
        import_chain.sort_values(by='strike',ascending=True)
        
        import_chain["center_strike"] = abs(import_chain["strike"]-ticker_price)
        min_strike = import_chain["center_strike"].min()
        mid1 = import_chain[import_chain["center_strike"] == min_strike].strike.index[0]
        mid1 = int(mid1)
        mid2 = mid1 + 1
        import_chain2 = import_chain2.append(import_chain.loc[mid1-12:mid1])
        import_chain2 = import_chain2.append(import_chain.loc[mid2:mid2+12])
        del import_chain
        del import_chain2["center_strike"]
    
    return import_chain2

