# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 23:55:56 2021

@author: Daniel
"""

import tkinter as tk
from PIL import ImageTk,Image
import tkinter.ttk as ttk
import selenium_barchart_2 as sb
import option_chain_api as oca



def NewElement(event):
    print(get_wombo.get())
    r = get_wombo.get()
    path = r'C:\Pythonsaves\8-23-2021\{}.png'.format(r)
    new_image = ImageTk.PhotoImage(Image.open(path))
    label1.configure(image = new_image)
    label1.image = new_image

def nextimage(event):
    print("Nextimage!")
    global start_
    start_ = start_ + 1
    
    
    
    path = r'C:\Pythonsaves\8-23-2021\{}.png'.format(k1[start_])
    new_image = ImageTk.PhotoImage(Image.open(path))
    label1.configure(image = new_image)
    label1.image = new_image
    
def previousimage(event):
    print("Previousimage!")
    global start_
    
    
    start_ = start_ -1
    path = r'C:\Pythonsaves\8-23-2021\{}.png'.format(k1[start_])
    new_image = ImageTk.PhotoImage(Image.open(path))
    label1.configure(image = new_image)
    label1.image = new_image

def df_to_treeview(source_df):
    source_df.reset_index(drop=True,inplace=True)
    tv = ttk.Treeview(frame1, columns = source_df.columns,show='headings',height = 12)
    
    for num,sd in enumerate(source_df.columns):
        tv.heading(str(num),text=sd)
        #tv.column(str(num),width=100)
    
    for i in source_df.index:
        
        tv.insert(parent='',index=i,values=source_df.loc[i].values)

    tv.place(x = 0,y = 0)

#variables; belong in an init

global start_
start_ = 0
k0 = sb.OptionSearch()
k1 = ["AMC","APLS","AUPH"]
path = r'C:\Pythonsaves\8-23-2021\{}.png'.format(k1[start_])
source_ = oca.main(["AMC"])

#GUI Initialization
root = tk.Tk()
get_wombo = tk.StringVar()

root.state("zoomed")


#widgets

#wombo_combo = ttk.Combobox(root,values=tuple(k1),textvariable=get_wombo)   
#wombo_combo.place(x=0,y=0)
#wombo_combo.bind("<<ComboboxSelected>>",NewElement)

image2 = ImageTk.PhotoImage(Image.open(path))
label1 = tk.Label(root,image = image2)
label1.place(x=20,y=30)

frame1 = tk.Frame(root,width=1450,height=500)
frame1.place(x=20,y=500)

df_to_treeview(source_)














root.bind('<KeyPress-a>',previousimage)
root.bind('<KeyPress-d>',nextimage)

root.title("HighIV")
root.mainloop()