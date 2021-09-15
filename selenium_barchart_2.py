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
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import requests
import json
from datetime import *
import time
import os


class OptionSearch:
    
    def __init__(self):
        
        pd.set_option('display.max_rows',500)
        pd.set_option('display.max_columns',500)
        pd.set_option('display.width',1000)
        print("I'm in.")

    #Loginto Barchart account and download CSV
    
    def path_init(self):
        global path_adblock , options_ , driver , action
        
        
        path_adblock=r'C:\Users\Daniel\Downloads\Adblock.crx'
        options_= Options()
        options_.add_extension(path_adblock)
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options_)
        driver.set_window_size(1024, 600)
        driver.maximize_window()
        action=ActionChains(driver)
    
    def BarchartImport(self):
        iter_=1
        current_date = str(input("Insert Date in MM-DD-YYYY format: "))
        bar_user = str(input("Barchart Username: "))
        bar_pass = str(input("Barchart Password: "))
        
        while iter_ < 2:
            try:
                
                self.path_init()
                
                driver.get("https://www.barchart.com/login")
                time.sleep(1)
                driver.find_element_by_xpath('//body').send_keys(Keys.CONTROL+'w')
                elem=driver.find_element_by_xpath("//input[@placeholder='Login with email']")
                elem.send_keys(bar_user)
                time.sleep(2)
                
                elem=driver.find_element_by_xpath("//input[@placeholder='Password']")
                elem.send_keys(bar_pass)
                time.sleep(2)
                
                elem=driver.find_element_by_xpath("//button[@class='bc-button login-button']").click()
                # write code to check if successfully went through login page
                
                driver.get("https://www.barchart.com/options/highest-implied-volatility/stocks")
                driver.get("https://www.barchart.com/options/highest-implied-volatility/stocks")
                driver.find_element_by_css_selector("a.toolbar-button.download").click()
                time.sleep(4)
                
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
            except Exception as exp:
                driver.quit()
                print(exp)
                print("Retrying Attempt {} failed.".format(iter_))
                iter_+=1
                continue
            

    def OptionImport(self):
        #read Barchart CSV and assign Ticker names
        try:
            global IV_list
            global IV_list_2
            global IV_list_3
            global public_company_list
            global IV3_symbol
            global ar_
            
            optiondate = str(input("Insert Date in MM-DD-YYYY format: "))
            IV_list = pd.read_csv(r"C:\Users\Daniel\Downloads\stocks-highest-implied-volatility-{}.csv".format(optiondate))
            IV_list = IV_list.drop_duplicates(subset=['Symbol'],keep = 'last')
            
            IV_list_2 = pd.DataFrame(IV_list)
            IV_list_2 = IV_list_2.reset_index()
            
            IV_list_2 = IV_list_2.drop([ len(IV_list_2['Symbol']) - 1])
            IV_list_2 = IV_list_2[ IV_list_2['Price'] >= 10]
            del IV_list_2['index']
            
            public_company_list = pd.read_csv(r'C:\Users\Daniel\Downloads\companylist.csv')
            public_company_list = pd.DataFrame(public_company_list)
            public_company_list = public_company_list.drop_duplicates(subset='Name',keep='last')
            public_company_list = public_company_list[ public_company_list['Exchange'].isin(['AMEX','NYSE','NQNM'])]
            
            IV_list_3 = pd.merge(IV_list_2, public_company_list[['Symbol','Name']],how='left',left_on=['Symbol'],right_on=['Symbol'])
            ar_ = IV_list_3['Symbol']
            print("Import successful.")
            
            return ar_
        
        except Exception as EXP:
            print(EXP)
            print("Could not find file. Are you sure file name and date exist?")
            
        
 
    


    def TChart(self):
        
        iter_ = 1
        while iter_ < 3:
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
                
                #adding graphs each Ticker                
                for i in ar_:    
                    elem =driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div[1]")
                    elem.click()
                    time.sleep(2)
                    elem = driver.find_element_by_xpath("//input[@placeholder='Search']")
                    elem.click()
                    elem.send_keys(Keys.BACKSPACE+Keys.BACKSPACE+Keys.BACKSPACE+Keys.BACKSPACE+i+Keys.ENTER)
             
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
                    
                    file_name = r"C:\Pythonsaves\{}.png".format(i)
                    driver.save_screenshot(file_name)
                    time.sleep(3)
                
                
            except Exception as EXP:
                time.sleep(2)
                driver.quit()
                print("Attempt {} failed. Retrying...".format(iter_))
                print(EXP)
                iter_ += 1
                time.sleep(5)
            finally:
                print("Finished screenshotting Technicals")
                driver.quit()
                

    def GetEarnings(self):
        #Finviz scrape earnings
        
        self.path_init()
        
        
        for j,i in enumerate(ar_):
            try: 
                url_ = r"https://finviz.com/quote.ashx?t={}&ty=c&ta=1&p=d".format(i)
                driver.get(url_)
                edate =driver.find_element_by_xpath("/html/body/div[4]/div/table[2]/tbody/tr[11]/td[6]/b").text
                print(edate)
                
                
                beta = driver.find_element_by_xpath("/html/body/div[4]/div/table[2]/tbody/tr[7]/td[12]/b").text
                dividend = driver.find_element_by_xpath("/html/body/div[4]/div/table[2]/tbody/tr[8]/td[2]/b").text
                marketcap = driver.find_element_by_xpath("/html/body/div[4]/div/table[2]/tbody/tr[2]/td[2]/b").text
                
                IV_list_3.loc[j,'Earnings Date'] = edate
                IV_list_3.loc[j,'Beta'] = beta
                IV_list_3.loc[j,'Div'] = dividend
                IV_list_3.loc[j,'Market Cap'] = marketcap
                IV_list_3.fillna("-",inplace = True)
                print(IV_list_3['Earnings Date'])
                
            except:
                continue
            
        return IV_list_3
    
    def AmerConnect(self):
        #Connecting to TDAmeritradeAPI
        api_key=str(input("Enter TD Ameritrade API Key: "))
        #0 Starts on Monday
        
        cond_= datetime.datetime.today().weekday()
        if cond_ < 4:
            beg_date = datetime.datetime.today()
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
        
        
if __name__ == "__main__":
    r = OptionSearch()
    r.path_init()
    #r.BarchartImport()
    r.OptionImport()
    #r.GetEarnings()
    r.TChart()
    




