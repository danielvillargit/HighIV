# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 17:17:59 2021

@author: Daniel
"""

import tkinter as tk
from PIL import ImageTk,Image
import tkinter.ttk as ttk
import selenium_barchart_2 as sb
import option_chain_api as oca
import pandas as pd
import os


class FrameView:
    
    
    def __init__(self,*args,**kwargs):
        global oc_return
        self.root = tk.Tk()
        self.root.state("zoomed")
        self.input_date = input("Insert Date to look at (YYYY-MM-DD Format) : ")
        
        
        
        
        self.package_path = r'C:/Users/Daniel/server_001/HighIV_2/{}'.format(self.input_date)
        self.list_dir = os.listdir(self.package_path+r'/finviz')
        self.int_ = tk.IntVar()
        self.int_.set(0)
        
        self.ticker = tk.StringVar()
        self.ticker.set(self.list_dir[self.int_.get()])
        
        
        
        self.init_tradingview_path = self.package_path + r'/tradingview/{}'.format(self.ticker.get())
        self.init_finviz_path = self.package_path + r'/finviz/{}'.format(self.ticker.get())
        
        print(self.ticker.get(), self.init_tradingview_path, self.init_finviz_path)
        
        
    
        self.root.title("HighIV")
    
        self.timg = Image.open(self.init_tradingview_path)
        self.timg = self.timg.resize((1280,600),Image.ANTIALIAS)
        self.tviewimg = ImageTk.PhotoImage(self.timg)
        self.tview_pic = tk.Label(self.root,image = self.tviewimg)
        self.tview_pic.place(x=0, y = 350)
        
        
        self.fimg = Image.open(self.init_finviz_path)
        self.fimg = self.fimg.resize((1280,350))
        self.finvizimg = ImageTk.PhotoImage(self.fimg)
        self.finviz_pic = tk.Label(self.root,image = self.finvizimg)
        self.finviz_pic.place(x=0,y= 0)
        
        
        
        self.tickername = tk.Label(self.root,textvariable = self.ticker)
        self.tickername.place(x=1280,y=0)
        
        

        
        oc = OptionChain(r'C:/Users/Daniel/server_001/HighIV_2/opchain.csv')
        oc_return = oc.returncsv()
        
        self.cb2_sv = tk.StringVar()
        cb_optiontype = ttk.Combobox(self.root,values=tuple(oc_return["option_type"].unique()),textvariable=self.cb2_sv)#postcommand = lambda: cb_optiontype.configure(values = oc_return )
        cb_optiontype.place(x=1285,y=40)
        cb_optiontype.bind("<<ComboboxSelected>>",self.sourcefilterquery)
        
        self.cb3_sv = tk.StringVar()
        cb3 = ttk.Combobox(self.root,values=tuple(oc_return["expiration_date"].unique()),textvariable=self.cb3_sv)
        cb3.place(x=1285,y=100)
        cb3.bind("<<ComboboxSelected>>",self.sourcefilterquery)
        
        self.df_to_treeview(oc_return)
        
        self.b4b5_var = tk.IntVar()
        b4 = tk.Radiobutton(self.root,text="Show Option Chain",variable = self.b4b5_var, value = 1,command = self.toggleoption)
        b4.place(x=1285,y=200)
        
        b5 = tk.Radiobutton(self.root,text="Hide Option Chain",variable = self.b4b5_var, value = 2,command = self.toggleoption)
        b5.place(x=1285,y=250)   
        
        self.root.bind('<KeyPress-a>',self.previousimage)
        
        self.root.bind('<KeyPress-d>',self.nextimage)
        
        self.root.mainloop()
        
    
    
    def df_to_treeview(self,csv_sourcepath):
        
        self.csv_sourcepath = csv_sourcepath
    
        self.csv_sourcepath.reset_index(drop=True,inplace=True)
        
        if self.csv_sourcepath.empty:
            pass
        
        else:
        
        
            if "Unnamed: 0" in self.csv_sourcepath.columns:
                del self.csv_sourcepath["Unnamed: 0"]
                
            
                
            self.tv = ttk.Treeview(self.root, columns = self.csv_sourcepath.columns,show='headings',height = 14)
            
            for num,sd in enumerate(self.csv_sourcepath.columns):
                
                
                self.tv.heading(str(num),text=sd)
                #tv.column(str(num),width=100)
            
            for i in self.csv_sourcepath.index:
                
                self.tv.insert(parent='',index=i,values=tuple(self.csv_sourcepath.loc[i].values))
            #self.tv.place(x = 0,y = 500)
            
        
    
    def toggleoption(self,*event):
        
        if self.b4b5_var.get() == 1:
            
            self.tv.place(x = 0,y = 580)
            
        if self.b4b5_var.get() == 2:
            
            self.tv.place_forget()
    
    
    
    
    
    
    
    
    
    
    def sourcefilterquery(self,*event):
        
        self.str_ = self.ticker.get()
        self.str_ = self.str_.replace(".png","")
        
        self.df_to_treeview(oc_return[(oc_return["root_symbol"] ==self.str_)  & (oc_return["expiration_date"] == self.cb3_sv.get()) & (oc_return["option_type"] == self.cb2_sv.get())   ])
        self.toggleoption()
        
        
    def nextimage(self,*event):
        print("Nextimage!")
        
        
        if self.int_.get() > len(self.list_dir) - 1:
            print("Reached max length")
        else:
            
            self.int_.set(self.int_.get() + 1)
            
            self.imageSet()
            
    def imageSet(self):
        
        self.ticker.set(self.list_dir[self.int_.get()])
        self.init_finviz_path = self.package_path + r'/finviz/{}'.format(self.ticker.get())
        self.init_tradingview_path = self.package_path + r'/tradingview/{}'.format(self.ticker.get())
        
        newimg1 = Image.open(self.init_finviz_path)
        newimg1 = newimg1.resize((1280,350),Image.ANTIALIAS)
        newimg1_pi = ImageTk.PhotoImage(newimg1)
        
        self.finviz_pic.image = newimg1_pi
        self.finviz_pic.configure(image = newimg1_pi)
        
        
        newimg2 = Image.open(self.init_tradingview_path)
        newimg2 = newimg2.resize((1280,600),Image.ANTIALIAS)
        newimg2_pi = ImageTk.PhotoImage(newimg2)
        
        self.tview_pic.image = newimg2_pi
        self.tview_pic.configure(image = newimg2_pi)
        
    def previousimage(self,*event):
        print("Previousimage!")
        
        
        if self.int_.get() == 0:
            print("Reached index 0")
        else:
            
            self.int_.set(self.int_.get() - 1)
            
            self.imageSet()
        
        
        
        
class OptionChain:
    def __init__(self,csv_sourcepath,*args,**kwargs):
        self.csv_sourcepath = pd.read_csv(csv_sourcepath)
        self.csv_sourcepath = pd.DataFrame(self.csv_sourcepath)
        
    def returncsv(self):
        return self.csv_sourcepath 
        
        
        
if __name__ == "__main__":
    frame = FrameView()
    
    