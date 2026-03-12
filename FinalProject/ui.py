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

    print(f"creating sub uis with default geometry {geometry}")
#create windows
    start_menu = tk.Toplevel()
    start_menu.title("A Good Enough Cycle")
    start_menu.geometry(geometry)
    
    settings = tk.Toplevel()
    settings.title("Settings")
    settings.geometry(geometry)
    
    ls_root.insert(1, settings)
    ls_root.insert(2, start_menu)
    return root



#-------------Create Other Widgets------------
def add_button(name, parent, xpad, ypad, action, dict_buttons):
    print(f"creating Button Widget named: {name} name with parent: {parent} pad x: {xpad} pad y: {ypad} and action: {action}")


    button = tk.Button(parent, text=name, command=action)
    print(f"no function for button: {name} in parent: {parent}. attempted action input: {action}")
    button.pack(pady=ypad, padx=xpad)
    dict_buttons[name] = "button"
    return

#------------Button actions------------
def play():
    print("play!")

def quitgame(ls_root):
    ls_root.destroy()
    print("buttoneventinterupt-quit")

def settings(ls_root):
    if ls_root.winfo_exists():
        ls_root.deiconify()
    else:
        settings = tk.Toplevel()
    settings.title("Settings")
    settings.geometry("300x400")
        
    print("open settings!")


def run(root):
    print("it ran!", root)
    root.mainloop()

def show(ls_root):
    ls_root.deiconify()

def hide(ls_root):
    ls_root.withdraw()