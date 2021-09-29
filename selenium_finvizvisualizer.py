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

class FinvizVisualizer:
    
    def __init__(self):
        
        print("Finviz Visualizer Object Created")
        self.download_path = r'C:\Users\Daniel\HighIV'
        
        
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
        
        
        #options_.add_extension(path_adblock)
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options_)
        driver.set_window_size(1024, 600)
        driver.maximize_window()
        action=ActionChains(driver)
        
        
    def getpicture(self):
        
        self.path_init(self.download_path)
        
        
        
        
        
if __name__ == "__main__":
    fv = FinvizVisualizer()
    fv.getpicture()