# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 10:01:40 2021

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


class Tradingview:
    
    def __init__(self):
        print("Tradingview object created.")
        current_date = datetime.today()
        current_date = current_date.strftime("%Y-%m-%d")
        
        self.getdata_path = r'C:\Users\Daniel\HighIV\opvis.csv'
        self.path_adblock=r'C:\Users\Daniel\HighIV\Adblock.crx'
        self.subfolder_tchart_path = r'C:\Users\Daniel\HighIV\{}'.format(current_date)
        self.write_tchart_path = self.subfolder_tchart_path + r'\tradingview'
        
        self.folderWriter()
    
    def getdata(self):
        try:
            
            get_data = pd.read_csv(self.getdata_path)
            get_data = pd.DataFrame(get_data)
            
            return get_data["Ticker"]
        except:
            print("Could not read file Opvis.csv. Are you sure file exists in directory?")
            
        
    
    
    
    def path_init(self):
        
        global options_ , driver , action
        
        
        
        options_= Options()
        options_.add_extension(self.path_adblock)
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options_)
        driver.set_window_size(1024, 600)
        driver.maximize_window()
        action=ActionChains(driver)
        driver.switch_to_window(driver.window_handles[0])
    
    

    def viewSignIn(self):
        
        self.trading_user = str(input("Insert Tradingview Username: "))
        self.trading_pass = str(input("Insert Tradingview Password: "))
        
        
        self.path_init()
        
        driver.get("https://www.tradingview.com/")
        
        driver.find_element_by_xpath("//button[@aria-label='Open user menu']").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[contains(text(), 'Sign in')]").click()
        time.sleep(2)
        elem = driver.find_element_by_xpath("/html/body/div[6]/div/div[2]/div/div/div/div/div/div/div[1]/div[4]/div/span")
        elem.click()
        time.sleep(2)
        elem = driver.find_element_by_xpath("//input[@name='username']")
        elem.send_keys(self.trading_user)
        
        elem = driver.find_element_by_xpath("//input[@name='password']")
        elem.send_keys(self.trading_pass)
        
        driver.find_element_by_xpath("//span[@class='tv-button__loader']").click()
        time.sleep(5)
    
    def setTChart(self):
        
        iter_ = 1
        
        
        
        
        
        self.ar_ = self.getdata()
        while iter_ < 3:
            try:    
                
                self.viewSignIn()
                
                
                
                #navigate to tradingview
                
                driver.get("https://www.tradingview.com/chart")
                
                #driver.find_element_by_xpath("//a[@data-type='chart']").click()
                
                #adding graphs each Ticker                
                for j,i in enumerate(self.ar_):  
                    print(str(j+1)+ " out of "+str(len(self.ar_)))
                
                    time.sleep(2)
                    elem =driver.find_element_by_xpath("//div[@id='header-toolbar-symbol-search']")
                    elem.click()
                    time.sleep(2)
                    elem = driver.find_element_by_xpath("//input[@placeholder='Search']")
                    elem.click()
                    elem.send_keys(Keys.BACKSPACE+Keys.BACKSPACE+Keys.BACKSPACE+Keys.BACKSPACE+i+Keys.ENTER)
             
                
             
                
             
                
                    if i==self.ar_[0]:
                        elem = driver.find_element_by_xpath("//div[@data-name='open-indicators-dialog']")
                        elem.click()
                        time.sleep(1)
                        elem = driver.find_element_by_xpath("//input[@data-role='search']")
                        for k in range(3):
                            if k ==0 :
                                string_= 'Chaikin Money Flow'
                            if k ==1 :
                                string_ = 'On Balance Volume'
                            if k==2 :
                                string_ = 'MACD'
                            elem = driver.find_element_by_xpath("//input[@data-role='search']")
                            elem.send_keys(string_)
                            time.sleep(1)
                            
                            elem = driver.find_element_by_xpath("//div[@class='main-3Ywm3-oo']")
                            elem.click()
                            time.sleep(1)
                            if i==2:
                                elem = driver.find_element_by_xpath("//span[@data-name='close']")
                                elem.click()
                        
                    
                            #for x in string_:
                            #    elem = driver.find_element_by_xpath("//input[@data-role='search']")
                            #    elem.send_keys(Keys.BACKSPACE)
                    time.sleep(3)
                    
                    
                        
                    
                    try:
                        if driver.find_element_by_xpath("//*[contains(text(),'Take your trading to the next level')]"):
                            driver.refresh()
                            elem.send_keys(Keys.ENTER)
                    except:
                        pass
                    
                    
                    
                    file_name = self.write_tchart_path + r'/{}.png'.format(i)
                    driver.save_screenshot(file_name)
                    time.sleep(3)
                iter_ = 3
            
            except Exception as EXP:
                time.sleep(2)
                driver.quit()
                print("Attempt {} failed. Retrying...".format(iter_))
                print(EXP)
                iter_ += 1
                time.sleep(5)
            
                
            
    #under construction
    def removeTChart(self):
        iter_ = 1
        while iter_ <= 2:
            
            try:
                
                self.viewSignIn()
                    
                #navigate to tradingview
                
                driver.get("https://www.tradingview.com/chart")
                
                driver.find_element_by_xpath("//td[@class='chart-markup-table pane'").click()
                
                iter_ = 3
            except Exception as e:
                time.sleep(2)
                print("Attempt {} failed. Retrying...".format(iter_))
                print(e)
                iter_ += 1
                
                
    def folderWriter(self):
        
        if os.path.isdir(self.subfolder_tchart_path):
            pass
        
            if os.path.isdir(self.write_tchart_path):
                pass
            
            else:
                os.makedirs(self.write_tchart_path)
            
        else:
            os.makedirs(self.subfolder_tchart_path)
            os.makedirs(self.write_tchart_path)
            
if __name__ == "__main__":
    tv = Tradingview()
    tv.removeTChart()