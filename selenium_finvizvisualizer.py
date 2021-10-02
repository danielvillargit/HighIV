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
        
        current_date = datetime.datetime.today()
        current_date = current_date.strftime("%Y-%m-%d")
        self.subfolder_finviz_path = r'C:\Users\Daniel\server_001\HighIV_2\{}'.format(current_date)
        self.write_finviz_path = self.subfolder_finviz_path + r'\finviz'
        self.path_adblock = r'C:\Users\Daniel\server_001\HighIV_2\Adblock.crx'
        self.source_data_loc = r'C:\Users\Daniel\server_001\HighIV_2'
        
        self.folderWriter()
        
        
    def path_init(self,download_path):
        
        global path_adblock , options_ , driver , action
        
        self.write_finviz_path = download_path
        
        
        options_= Options()
        
        if self.write_finviz_path is not None:
            prefs = {}
            prefs["profile.default_content_settings.popups"] = 0
            prefs["download.default_directory"] = self.write_finviz_path
            options_.add_experimental_option("prefs",prefs)
        
        
        options_.add_extension(self.path_adblock)
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options_)
        driver.set_window_size(1024, 600)
        driver.maximize_window()
        action=ActionChains(driver)
        driver.switch_to_window(driver.window_handles[0])
        
    def getpicture(self):
        
        self.path_init(self.write_finviz_path)
        #for now defining data source as OptionVisualizer
        
        self.source_data = pd.read_csv(self.source_data_loc + "\\opvis.csv")
        self.source_data = pd.DataFrame(self.source_data)
        
        del self.source_data["Unnamed: 0"]
            
        for f in self.source_data["Ticker"]:
            try:   
                
                driver.get(r'https://finviz.com/quote.ashx?t={}'.format(f))
                img = driver.find_element_by_xpath("//canvas[@class='second']")
                img_save_path = self.write_finviz_path + r'\{}.png'.format(f)
                img.screenshot(img_save_path)
            
            except Exception as exp:
                print(exp)
        driver.quit()
        return "Finviz photoscrape complete."
        
    def folderWriter(self):
        
        if os.path.isdir(self.subfolder_finviz_path):
            pass
        
            if os.path.isdir(self.write_finviz_path):
                pass
            
            else:
                os.makedirs(self.write_finviz_path)
            
        else:
            os.makedirs(self.subfolder_finviz_path)
            os.makedirs(self.write_finviz_path)
            
    
        
if __name__ == "__main__":
    fv = FinvizVisualizer()
    fv.getpicture()