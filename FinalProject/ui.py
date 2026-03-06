import tkinter as tk
import time as tm
from tkinter import ttk
import events as ev
import tasks as tsk
import alerts as als
import misc_utils as msc

#-------------Create Main Windows------------
def create_main_ui(name, geometry, resizeable, ls_root):
    print(f"creating Main Ui element named: {name} with geometry: {geometry}")
    root = tk.Tk()
    root.title(name)
    root.geometry(geometry)
    ls_root.insert(0, root)
    root.withdraw()

    print(f"creating sub uis with default geometry {geometry}")
#create windows
    start_menu = tk.Toplevel()
    start_menu.title("A Good Enough Cycle")
    start_menu.geometry(geometry)
    
    settings = tk.Toplevel()
    settings.title("Settings")
    settings.geometry(geometry)
    settings.withdraw()
    
    ls_root.insert(1, settings)
    ls_root.insert(2, start_menu)
    return root



#-------------Create Other Widgets------------
def add_button(name, parent, xpad, ypad, acton, dict_buttons):
    print(f"creating Button Widget named: {name} name with parent: {parent} pad x: {xpad} pad y: {ypad} and action: {acton}")
    button = tk.Button(parent, text=name)
    button.pack(pady=ypad, padx=xpad)
    dict_buttons[name] = "button"
    return



def run(root):
    print("it ran!", root)
    root.mainloop()

def show(ls_root):
    ls_root.deiconify()

def hide(ls_root):
    ls_root.withdraw()