# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 23:05:57 2021

@author: Daniel
"""

import requests
import pandas as pd
from yahoofinancials import YahooFinancials as yf
from selenium_barchart_2 import *
import datetime

def getdate():
    today = datetime.datetime.today()
    fridays = []
    for i in range(5):
        if i == 0:
            fri = (today + datetime.timedelta(4-today.weekday()))
        else:
            fri += datetime.timedelta(7)
            
        fridays.append(fri.strftime("%Y-%m-%d"))
    
    return fridays


def maincall(ticker_path):
    
    #ticker_data_selenium = OptionSearch()
    #ticker_data_selenium.BarchartImport()
    
    #ticker = ticker_data_selenium.OptionImport()
    
    ticker = pd.read_csv(ticker_path)
    ticker = pd.DataFrame(ticker)
    ticker.sort_values(by=["Ticker"],ascending=True,inplace=True)
    
    toke = 'H4WiYj0CVcFpz7hZeFpj9uxKJxcJ'
    btoke = r'Bearer {}'.format(toke)
    column_list = ['symbol','root_symbol','description','strike','bid','ask','option_type','open_interest','volume','expiration_date']
    
    

    expiry = getdate()
    
    import_chain2 = pd.DataFrame(data=None,columns=column_list)
    
    for num,tick_ in enumerate(ticker["Ticker"]):
        print((num+1) + "//" + len(ticker["Ticker"]))
        for f in expiry:
            try:
                
                
        
                res = requests.get('https://sandbox.tradier.com/v1/markets/options/chains',
                                   params={'symbol':tick_,'expiration': f , 'greeks': 'false'},
                                   headers={'Authorization': btoke,'Accept': 'application/json'})
                
                json_response = res.json()
                
                print(res.status_code)
                #print(json_response)
                
                if json_response['options'] == None:
                    raise Exception
            
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
                del import_chain2["description"]
                del import_chain2["open_interest"]
                
                
                
                
            except:
                continue
    
    print(import_chain2)
    return import_chain2
            

if __name__ == "__main__":
    path = r'C:\Users\Daniel\HighIV\opvis.csv'
    csv_exportpath = r'C:\Users\Daniel\HighIV\opchain.csv'
    return_df = maincall(path)
    return_df.to_csv(csv_exportpath)
    



