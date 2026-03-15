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
    button.pack(pady=ypad, padx=xpad)
    dict_buttons[name] = button
    return

def add_label(name, parent, xpad, ypad, text, dict_labels, LorR, TorB):
    print(f"creating label Widget named: {name} name with parent: {parent} pad x: {xpad} pad y: {ypad} and text: {text}")
    label = tk.Label(parent, text=text,)
    if LorR.lower() == "left":
        print("LEFT")
        label.pack(pady=ypad, padx=xpad, side=tk.LEFT)
    elif LorR.lower() == "Right":
        print("RIGHT")
        label.pack(pady=ypad, padx=xpad, side=tk.RIGHT)
    else:
        print("none")
        label.pack(pady=ypad, padx=xpad,)
    dict_labels[name] = label
    return

def add_frame(name, parent, xpad, ypad, dict_frames, LorR, TorB, backg):
    print(f"creating frame Widget named: {name} name with parent: {parent} pad x: {xpad} pad y: {ypad}")
    frame = tk.Frame(parent, bg=backg)
    if LorR.lower() == "left":
        print("LEFT")
        frame.pack(pady=ypad, padx=xpad, side=tk.LEFT)
    elif LorR.lower() == "Right":
        print("RIGHT")
        frame.pack(pady=ypad, padx=xpad, side=tk.RIGHT)
    else:
        print("none")
        frame.pack(pady=ypad, padx=xpad,)
    dict_frames[name] = frame
    return

#------------Button actions------------
def play(ls_root):
    ls_root[0].withdraw()
    ls_root[2].deiconify()
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