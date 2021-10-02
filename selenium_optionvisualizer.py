# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 09:24:07 2021

@author: Daniel
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import requests
import json
from datetime import *
import time
import os
import yfinance as yf


class OptionVisualizer:
    
    def __init__(self):
        global download_path
        print("OptionVisualizer object created")
        self.download_path = r'C:\Users\Daniel\server_001\HighIV_2'
        self.path_adblock=r'C:\Users\Daniel\server_001\HighIV_2\Adblock.crx'
        
        self.toke = 'H4WiYj0CVcFpz7hZeFpj9uxKJxcJ'
        self.btoke = r'Bearer {}'.format(self.toke)
        
        #self.csvcheck()
        
    def path_init(self,download_path):
        global options_ , driver , action
        
        
        self.download_path = download_path
        
        
        options_= Options()
        
        if self.download_path is not None:
            prefs = {}
            prefs["profile.default_content_settings.popups"] = 0
            prefs["download.default_directory"] = self.download_path
            options_.add_experimental_option("prefs",prefs)
        
        
        #options_.add_extension(self.path_adblock)
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options_)
        driver.set_window_size(1024, 600)
        driver.maximize_window()
        action=ActionChains(driver)
        
    def csvcheck(self):
        
        list_dir = os.listdir(self.download_path)
        for f in list_dir:
            if f == "tableExport.csv" or f == "opvis.csv":
                os.remove(self.download_path +"\\" + f)
        
        
    def csvget(self):
        
        
        self.path_init(self.download_path)
        
        driver.get("https://www.optionvisualizer.com/option-screener/highest-implied-volatility-options?o.days_before_expiration=manual|15|&o.implied_volatility=manual|60|&o.option_close=manual|0.10|&o.open_interest=manual|100|&o.volume=manual|500|&o.radio_option_type=manual|true|true&sort_by=o.implied_volatility&sort_order=desc")
        
        #days before expiration - upper range
        elem = driver.find_element_by_xpath("//input[@placeholder='Upper range']")
        elem.send_keys("45")
        
        #implied volatility - upper range
        elem = driver.find_element_by_xpath("/html/body/div/div/form/div[3]/div/div/div/div[2]/div[2]/div[1]/div/input[2]")
        elem.send_keys("150")
        
        
        #volume - lower range
        elem = driver.find_element_by_xpath("/html/body/div/div/form/div[3]/div/div/div/div[5]/div[2]/div[1]/div/input[1]")
        elem.send_keys(Keys.BACKSPACE + Keys.BACKSPACE + Keys.BACKSPACE + "100")
        #call button
        elem = driver.find_element_by_xpath("//label[@for='option_type_call']").click()
        
        elem = driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
        
        time.sleep(15)
        
        elem = driver.find_element_by_xpath("//button[@title='Export data']").click()
        
        time.sleep(2)
        
        elem = driver.find_element_by_xpath("//a[contains(text(),'CSV')]").click()
        
        time.sleep(5)
        
        driver.quit()
        
        return r'{}\\tableExport.csv'.format(self.download_path)
        
    
    def csvFormat(self):
    
        self.csv_df = pd.read_csv(r'{}\\tableExport.csv'.format(self.download_path))
        self.csv_df = pd.DataFrame(self.csv_df)
        
        self.csv_df = self.csv_df.drop_duplicates(subset='Ticker',keep='last')
        self.csv_df= self.csv_df[['Ticker','Security Name','Implied Volatility (Option)']]
        
        self.csv_df = self.csv_df.reset_index()
        del self.csv_df["index"]
        
        for i,j in enumerate(self.csv_df.index):
            try:
                
                tick_res = yf.Ticker(self.csv_df.loc[i,"Ticker"])
                sec = tick_res.info["sector"]
                cp = tick_res.info["bid"]
                self.csv_df.loc[i,"Sector"] = sec
                self.csv_df.loc[i,"Price"] = cp
                print(sec)
                print(cp)
                print(i)
            except:
                pass
        self.csv_df = self.csv_df[self.csv_df["Price"] > 10]
        
        
        self.exit_path = self.download_path + "\\" + "opvis.csv"
        self.csv_df.to_csv(self.exit_path)
        
        return self.exit_path
        # add optionality to search folder first instead of going straight to csvget. Actually scratch that lets see where it goes

    
        
 
        
    
if __name__ == "__main__":
    ov = OptionVisualizer()
    ov.csvFormat()
    
    