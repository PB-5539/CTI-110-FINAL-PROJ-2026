import tkinter as tk
import time as tm
from tkinter import ttk
import events as ev
import tasks as tsk
import alerts as als
import misc_utils as msc

#-------------Create Main Windows------------
def create_main_ui(name, geometry, resizeable):
    print(f"creating Main Ui element named: {name} with geometry: {geometry}")
    root = tk.Tk()
    root.title(name)
    root.geometry(geometry)

    print(f"creating sub uis with default geometry {geometry}")
#create windows
    start_menu = tk.Toplevel()
    settings = tk.Toplevel()    
#setup widgets
    start_label_name = tk.Label(start_menu,)
    start_button_play = tk.Button(start_menu,)
#package widgets
    start_label_name.pack(pady = 20)
    start_button_play.pac(pady = 20)


    root.mainloop()

#-------------Create Other Widgets------------
def add_button(name, parent, xpad, ypad, acton):
    print(f"creating Button Widget named: {name} name with parent: {parent} pad x: {xpad} pad y: {ypad} and action: {acton}")