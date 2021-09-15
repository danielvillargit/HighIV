# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 23:30:31 2021

@author: Daniel
"""

import tkinter as tk
from PIL import ImageTk,Image
from tkinter.ttk import Combobox
import selenium_barchart_2 as sb


k0 = sb.OptionSearch()
k1 = k0.OptionImport()
root = tk.Tk()

image1 = Image.open(r'C:\Pythonsaves\8-23-2021\AMC.png')

image2 = ImageTk.PhotoImage(image1)



wombo_combo = Combobox(root,values=tuple(k1.values))
wombo_combo.place(x=0,y=0)

#label1 = tk.Label(root,image = image2)
#label1.place(x=20,y=20)

#canvas = tk.Canvas(width = 400, height = 400, bg = 'black')
#canvas.pack(expand=True)
#canvas.create_image(0,0,image=image1)
root.title("HighIV")
root.mainloop()