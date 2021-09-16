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
    label2.configure(text = k1[start_])
def previousimage(event):
    print("Previousimage!")
    global start_
    
    
    start_ = start_ -1
    path = r'C:\Pythonsaves\8-23-2021\{}.png'.format(k1[start_])
    new_image = ImageTk.PhotoImage(Image.open(path))
    label1.configure(image = new_image)
    label1.image = new_image
    
    label2.configure(text = k1[start_])
    
def df_to_treeview(source_df):
    source_df.reset_index(drop=True,inplace=True)
    tv = ttk.Treeview(frame1, columns = source_df.columns,show='headings',height = 12)
    
    for num,sd in enumerate(source_df.columns):
        tv.heading(str(num),text=sd)
        #tv.column(str(num),width=100)
    
    for i in source_df.index:
        
        tv.insert(parent='',index=i,values=tuple(source_df.loc[i].values))

    tv.place(x = 0,y = 0)

def sourcefilterquery():
    
    #filter doesn't work completely right yet, need to tweak root_symbol
    
    df_to_treeview(source_[(source_["root_symbol"] ==k1[start_] )  & (source_["expiration_date"] == cb3_sv.get()) & (source_["option_type"] == cb2_sv.get())   ])


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
cb2_sv = tk.StringVar()
cb3_sv = tk.StringVar()
root.state("zoomed")


#widgets

#wombo_combo = ttk.Combobox(root,values=tuple(k1),textvariable=get_wombo)   
#wombo_combo.place(x=0,y=0)
#wombo_combo.bind("<<ComboboxSelected>>",NewElement)

image2 = ImageTk.PhotoImage(Image.open(path))
label1 = tk.Label(root,image = image2)
label1.place(x=20,y=30)

label2 = tk.Label(root,text=k1[start_])
label2.place(x=40,y=0)
frame1 = tk.Frame(root,width=1450,height=500)
frame1.place(x=20,y=500)

cb2 = ttk.Combobox(root,values=tuple(source_["option_type"].unique()),textvariable=cb2_sv)
cb2.place(x=100,y=0)


cb3 = ttk.Combobox(root,values=tuple(source_["expiration_date"].unique()),textvariable=cb3_sv)
cb3.place(x=250,y=0)

cb4 = tk.Button(root,text='Filter Query',command = sourcefilterquery)
cb4.place(x=400,y=0)

df_to_treeview(source_)














root.bind('<KeyPress-a>',previousimage)
root.bind('<KeyPress-d>',nextimage)

root.title("HighIV")
root.mainloop()