# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import requests
import json
from datetime import *
import datetime
import time
import os

#!pip install django
class OptionSearch:
    
    def __init__(self):
        
        
        print("im in.")

    #Loginto Barchart account and download CSV
    def BarchartImport(self):
        iter_=1
        current_date = str(input("Insert Date in MM-DD-YYYY format: "))
        bar_user = str(input("Barchart Username: "))
        bar_pass = str(input("Barchart Password: "))
        while iter_ < 6:
            try:
                
                path_adblock=r'C:\Users\Daniel\Downloads\Adblock.crx'
                options_= Options()
                options_.add_extension(path_adblock)
                driver = webdriver.Chrome(ChromeDriverManager().install(),options=options_)
                driver.set_window_size(1024, 600)
                driver.maximize_window()
                action=ActionChains(driver)
                
                driver.get("https://www.barchart.com/login")
                elem=driver.find_element_by_xpath("//input[@placeholder='Login with email']")
                elem.send_keys(bar_user)
                time.sleep(2)
                elem=driver.find_element_by_xpath("//input[@placeholder='Password']")
                elem.send_keys(bar_pass)
                time.sleep(2)
                
                elem=driver.find_element_by_xpath("//button[@class='bc-button login-button']").click()
                driver.get("https://www.barchart.com/options/highest-implied-volatility/stocks")
                driver.get("https://www.barchart.com/options/highest-implied-volatility/stocks")
                driver.find_element_by_css_selector("a.toolbar-button.download").click()
                time.sleep(4)
                try:
                    elem = driver.find_element_by_xpath("//*[contains(text(), 'Download Anyway' )]").click()
                except NoSuchElementException:
                    print(r'CSV seems to contain < 1000 lines. This is iteration attempt {}.'.format(iter_))
                time.sleep(4)
                path_test = r'C:\Users\Daniel\Downloads\highest-implied-volatility-stocks-options-{}.csv'.format(current_date)
                if os.path.isfile(path_test) == True:
                    continue
                else:
                    raise Exception
                driver.quit()
                iter_ = 6
                print("Successful download.")
            except:
                driver.quit()
                print("Retrying Attempt {} failed.".format(iter_))
                iter_+=1
                continue
            

    def OptionImport(self):
        #read Barchart CSV and assign Ticker names
        try:
            global csv3
            global csvimport2
            global ar_
            optiondate = str(input("Insert Date in MM-DD-YYYY format: "))
            df=pd.read_csv(r"C:\Users\Daniel\Downloads\highest-implied-volatility-stocks-options-{}.csv".format(optiondate))
            df.head()
            df=df.drop_duplicates(subset=['Symbol'],keep = 'last')
            csvimport = pd.DataFrame(df)
            csvimport=csvimport.reset_index()
            del csvimport['index']
            csvimport = csvimport.drop([len(csvimport['Symbol'])-1])
            csvimport = csvimport[csvimport['Price']>=10]

            df2=pd.read_csv(r'C:\Users\Daniel\Downloads\companylist.csv')
            csvimport2=pd.DataFrame(df2)
            csvimport2=df2.drop_duplicates(subset='Name',keep='last')
            csvimport2=csvimport2[csvimport2['Exchange'].isin(['AMEX','NYSE','NQNM'])]
            csv3=pd.merge(csvimport,csvimport2[['Symbol','Name']],how='left',left_on=['Symbol'],right_on=['Symbol'])
            ar_ = csv3['Symbol']
            print("Import successful.")
        except:
            print("Could not find file. Are you sure file name and date exist?")
            
 



    def TChart(self):
        #adblocker install
        iter_ = 1
        while iter_ < 6:
            try:    
                
                path_adblock=r'C:\Users\Daniel\Downloads\Adblock.crx'
                options_= Options()
                options_.add_extension(path_adblock)
                driver = webdriver.Chrome(ChromeDriverManager().install(),options=options_)
                driver.set_window_size(1024, 600)
                driver.maximize_window()
                action=ActionChains(driver)
                action.move_by_offset(200, 100)
                driver.implicitly_wait(1)
            
                #navigate to tradingview
                
                driver.get("https://www.tradingview.com/")
                
                driver.find_element_by_xpath("//a[@data-type='chart']").click()
                print("good copy.")
                #inserting ticker names
                #ar_ = csv3['Symbol']
                for i in ar_:    
                    elem =driver.find_element_by_xpath("//input[@class='input-3lfOzLDc']")
                    elem.click()
                    driver.implicitly_wait(2)
                    elem.send_keys(Keys.DELETE+i+Keys.ENTER)
             
                    if i==ar_[0]:
                        elem = driver.find_element_by_xpath("//div[@data-name='open-indicators-dialog']")
                        elem.click()
                        elem = driver.find_element_by_xpath("//input[@data-role='search']")
                        for i in range(3):
                            if i ==0 :
                                string_= 'Chaikin Money Flow'
                            if i ==1 :
                                string_ = 'On Balance Volume'
                            if i==2 :
                                string_ = 'MACD'
                            elem = driver.find_element_by_xpath("//input[@data-role='search']")
                            elem.send_keys(string_)
                            driver.implicitly_wait(1)
                            if i!=2:
                                elem = driver.find_element_by_xpath("//div[@class='main-34wD0nIh']")
                                elem.click()
                            else:
                                elem = driver.find_element_by_xpath("/html/body/div[8]/div/div/div[1]/div/div[3]/div[2]/div/div/div[2]")
                                elem.click()
                        
                    
                            for x in string_:
                                elem = driver.find_element_by_xpath("//input[@data-role='search']")
                                elem.send_keys(Keys.BACKSPACE)
                    time.sleep(3)
                    dash_ ='\\'
                    file_name = r"C:{}Pythonsaves{}{}.png".format(dash_,dash_,i)
                    driver.save_screenshot(file_name)
                    time.sleep(3)
                
                
            except:
                time.sleep(2)
                driver.quit()
                print("Attempt {} failed. Retrying...".format(iter_))
                iter_ += 1
                time.sleep(5)
                
                if iter_ == 5:
                    print("Final attempt failed. Exiting.")
                
                else:
                    continue
                iter_ +=1
                

    def GetEarnings(self):
        #Finviz scrape earnings
        driver = webdriver.Chrome(ChromeDriverManager().install())
        
        print(csv3)
        count_ = 0
        for j,i in enumerate(ar_):
            url_ = r"https://finviz.com/quote.ashx?t={}&ty=c&ta=1&p=d".format(i)
            driver.get(url_)
            edate =driver.find_element_by_xpath("/html/body/table[3]/tbody/tr[1]/td/table/tbody/tr[7]/td/table/tbody/tr[11]/td[6]").text
            print(edate)
            beta = driver.find_element_by_xpath("/html/body/table[3]/tbody/tr[1]/td/table/tbody/tr[7]/td/table/tbody/tr[7]/td[12]").text
            csv3.loc[count_,'Earnings Date'] = edate
            csv3.loc[count_,'Beta'] = beta
            print(csv3['Earnings Date'])
            count_ = count_+1
            if j==5:
                break
        return csv3
    
    def AmerConnect(self):
        #Connecting to TDAmeritradeAPI
        api_key=str(input("Enter TD Ameritrade API Key: "))
        #0 Starts on Monday
        
        cond_= datetime.datetime.today().weekday()
        if cond_ < 4:
            beg_date = datetime.datetime.today()#.strftime("%Y-%m-%d")
            beg_date += datetime.timedelta(days=(4-cond_))
            end_date = beg_date
            end_date += datetime.timedelta(days=31)
            beg_date.strftime("%Y-%m-%d")
            end_date.strftime("%Y-%m-%d")
            
        else:
            beg_date = datetime.datetime.today().strftime("%Y-%m-%d")
            end_date += datetime.timedelta(days=31)
            end_date.strftime("%Y-%m-%d")
            
        baseurl = "https://api.tdameritrade.com/v1/marketdata/chains"
        par_=['Company','description','bid','ask','volatility','openInterest','strikePrice','daysToExpiration']
        self.tdamer=pd.DataFrame(data=None,index=par_)
        for counter,l in enumerate(ar_):
            print(counter)
            sendparam = {'apikey':api_key,
                         'symbol':l, 'contractType': 'PUT', 'optionType':'S','range':'OTM','fromDate':beg_date,'toDate':end_date}
            content_ = requests.get(url = baseurl, params = sendparam)
            dat = content_.json()
            
            
            for i in dat['putExpDateMap']:
                for j in dat['putExpDateMap'][i]:
                    
                    data_ = dat['putExpDateMap'][i][j][0]
                    self.ser_=pd.Series(data=data_)
                    self.ser_=self.ser_.append(pd.Series(l,index=['Company']))
                    for k in self.ser_.index:
                        if k not in par_:
                            self.ser_= self.ser_.drop(k)
                        else:
                            continue
                    self.tdamer = self.tdamer.append(self.ser_,ignore_index=True,sort=True)
            if (counter%50==0 and counter!=0):
                time.sleep(60)
            else:
                continue
        
        
    
        
            
    
    




