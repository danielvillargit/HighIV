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
    
    if start_ > len(k1) - 1:
        print("Reached max length")
    else:
        
        start_ = start_ + 1
        
        
        
        path = r'C:\Pythonsaves\8-23-2021\{}.png'.format(k1[start_])
        new_image = ImageTk.PhotoImage(Image.open(path))
        label1.configure(image = new_image)
        label1.image = new_image
        label2.configure(text = k1[start_])
        
        sourcefilterquery()
        
def previousimage(event):
    print("Previousimage!")
    global start_
    
    if start_ == 0:
        print("Reached index 0")
    else:
        
        start_ = start_ -1
        path = r'C:\Pythonsaves\8-23-2021\{}.png'.format(k1[start_])
        new_image = ImageTk.PhotoImage(Image.open(path))
        label1.configure(image = new_image)
        label1.image = new_image
        
        label2.configure(text = k1[start_])
        sourcefilterquery()
    
def df_to_treeview(source_df):
    global tv
    source_df.reset_index(drop=True,inplace=True)
    tv = ttk.Treeview(frame1, columns = source_df.columns,show='headings',height = 12)
    
    for num,sd in enumerate(source_df.columns):
        tv.heading(str(num),text=sd)
        #tv.column(str(num),width=100)
    
    for i in source_df.index:
        
        tv.insert(parent='',index=i,values=tuple(source_df.loc[i].values))
        
    if b4b5_var == 1:
        frame1.place(x=20,y=500)
        tv.place(x = 0,y = 0)  
     
    

def sourcefilterquery(*event):
    global start_

    
    df_to_treeview(source_[(source_["root_symbol"] == k1[start_])  & (source_["expiration_date"] == cb3_sv.get()) & (source_["option_type"] == cb2_sv.get())   ])


def togglechain(*event):
    
    if cb4_sv.get() == True:
        print("TRUE")
        
        
        
    else:
        print("FALSE")
        frame1.place_forget()
        tv.place_forget()
        
    
    
    



#variables; belong in an init

global start_, k1
start_ = 0
k0 = sb.OptionSearch()
k1 = ["AMC","APLS","AUPH"]
path = r'C:\Pythonsaves\8-23-2021\{}.png'.format(k1[start_])
source_ = oca.main(k1)

#GUI Initialization
root = tk.Tk()
get_wombo = tk.StringVar()
cb2_sv = tk.StringVar()
cb3_sv = tk.StringVar()
lb1_sv = tk.StringVar()
root.state("zoomed")
cb4_sv = tk.BooleanVar()

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
#frame1.place(x=20,y=500)


cb2 = ttk.Combobox(root,values=tuple(source_["option_type"].unique()),textvariable=cb2_sv)
cb2.place(x=100,y=0)
cb2.bind("<<ComboboxSelected>>",sourcefilterquery)

cb3 = ttk.Combobox(root,values=tuple(source_["expiration_date"].unique()),textvariable=cb3_sv)
cb3.place(x=250,y=0)
cb3.bind("<<ComboboxSelected>>",sourcefilterquery)


def toggleoption():
    if b4b5_var.get() == 1:
        frame1.place(x=20,y=500)
        tv.place(x = 0,y = 0)
    if b4b5_var.get() == 2:
        frame1.place_forget()
        tv.place_forget()



b4b5_var = tk.IntVar()
b4 = tk.Radiobutton(root,text="Show Option Chain",variable = b4b5_var, value = 1,command = toggleoption)
b4.place(x=500,y=5)


b5 = tk.Radiobutton(root,text="Hide Option Chain",variable = b4b5_var, value = 2,command = toggleoption)
b5.place(x=650,y=5)




#cb4.bind("<<ButtonSelected>>",togglechain)
#cb4.place(x=500,y=5)




#cb4.place(x=400,y=0)

df_to_treeview(source_)


class Frame(tk.Tk):
    def __init__(self,*args,*kwargs):
        super().__init__()
        
        self.title("HighIV")
        self.mainloop()













root.bind('<KeyPress-a>',previousimage)
#root.bind('<KeyPress-a',sourcefilterquery)
root.bind('<KeyPress-d>',nextimage)


root.title("HighIV")
root.mainloop()