# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 16:32:01 2021

@author: Daniel
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import os
import datetime
class FinvizVisualizer:
    
    def __init__(self):
        
        global current_date
        print("Finviz Visualizer Object Created")
        
        self.download_path = r'C:\Users\Daniel\HighIV'
        current_date = datetime.datetime.today()
        current_date = current_date.strftime("%Y-%m-%d")
        
        self.checkdir()
        
        
    def path_init(self,download_path):
        
        global path_adblock , options_ , driver , action
        
        self.download_path = download_path
        
        path_adblock=r'C:\Users\Daniel\HighIV\Adblock.crx'
        options_= Options()
        
        if self.download_path is not None:
            prefs = {}
            prefs["profile.default_content_settings.popups"] = 0
            prefs["download.default_directory"] = download_path
            options_.add_experimental_option("prefs",prefs)
        
        
        options_.add_extension(path_adblock)
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options_)
        driver.set_window_size(1024, 600)
        driver.maximize_window()
        action=ActionChains(driver)
        driver.switch_to_window(driver.window_handles[0])
        
    def getpicture(self):
        
        self.path_init(self.download_path)
        #for now defining data source as OptionVisualizer
        
        self.source_data = pd.read_csv(self.download_path + "\\opvis.csv")
        self.source_data = pd.DataFrame(self.source_data)
        
        del self.source_data["Unnamed: 0"]
            
        for f in self.source_data["Ticker"]:
            try:   
                
                driver.get(r'https://finviz.com/quote.ashx?t={}'.format(f))
                img = driver.find_element_by_xpath("//canvas[@class='second']")
                img_save_path = self.check_path + r'\\{}.png'.format(f)
                img.screenshot(img_save_path)
            
            except Exception as exp:
                print(exp)
            
        return "Finviz photoscrape complete."
        
    def checkdir(self):
        self.check_path = self.download_path + r'\\{}'.format(current_date)
        if os.path.isdir(self.check_path):
            pass
        else:
            os.makedirs(self.check_path)
            
    
        
if __name__ == "__main__":
    fv = FinvizVisualizer()
    fv.getpicture()