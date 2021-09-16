# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 23:55:56 2021

@author: Daniel
"""

import tkinter as tk
from PIL import ImageTk,Image
from tkinter.ttk import Combobox
import selenium_barchart_2 as sb

def NewElement(event):
    print(get_wombo.get())
    r = get_wombo.get()
    path = r'C:\Pythonsaves\8-23-2021\{}.png'.format(r)
    new_image = ImageTk.PhotoImage(Image.open(path))
    label1.configure(image = new_image)
    label1.image = new_image

def Tabout(event):
    print("Tabbed out!")
    



k0 = sb.OptionSearch()

k1 = ["AMC","APLS","AUPH"]

path = r'C:\Pythonsaves\8-23-2021\{}.png'.format(k1[0])




root = tk.Tk()
get_wombo = tk.StringVar()

root.state("zoomed")




wombo_combo = Combobox(root,values=tuple(k1),textvariable=get_wombo)   
wombo_combo.place(x=0,y=0)
wombo_combo.bind("<<ComboboxSelected>>",NewElement)


image2 = ImageTk.PhotoImage(Image.open(path))

label1 = tk.Label(root,image = image2)
label1.place(x=20,y=20)






root.title("HighIV")
root.mainloop()