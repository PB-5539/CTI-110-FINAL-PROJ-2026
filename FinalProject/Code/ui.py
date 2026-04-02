import tkinter as tk
import time as tm
from tkinter import ttk
import events as ev
import tasks as tsk
import alerts as als
import misc_utils as msc
import loop
import pseudo_terminal as pt
#-------------Create Main Windows------------
def create_main_ui(name, geometry, resizeable, ls_root, ls_terminal, ls_frame_windows, dict_frames):
    print(f"creating Main Ui element named: {name} with geometry: {geometry}")
    root = tk.Tk()
    root.title(name)
    root.geometry(geometry)
    ls_root.insert(0, root)

    placeholder = tk.Toplevel()
    print(ls_frame_windows)
    placeholder.title("temp window")
    placeholder.geometry("400x700")
    ls_frame_windows.insert(0,placeholder)
    print(ls_frame_windows)
    placeholder.destroy()
    print(ls_frame_windows)

    print(f"creating sub uis with default geometry {geometry}")
    
    start_menu = tk.Toplevel()
    start_menu.title("A Good Enough Cycle")
    start_menu.geometry(geometry)
    
    settings = tk.Toplevel()
    settings.title("Settings")
    settings.geometry("300x400")

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

def add_slider(name, parent, xpad, ypad, dict_sliders):
    print(f"creating slider Widget named: {name} name with parent: {parent} pad x: {xpad} pad y: {ypad}")
    slider = tk.Scale(parent,from_=0, to=200, orient=tk.HORIZONTAL, label=f"{name}")
    slider.pack(pady=ypad, padx=xpad)
    dict_sliders[name] = slider
    return

def add_label(name, parent, xpad, ypad, text, dict_labels, LorR, TorB, backg):
    print(f"creating label Widget named: {name} name with parent: {parent} pad x: {xpad} pad y: {ypad} and text: {text}")
    label = tk.Label(parent, text=text, bg=backg)
    if LorR.lower() == "left":
        print("LEFT")
        label.pack(pady=ypad, padx=xpad, side=tk.LEFT)
    elif LorR.lower() == "right":
        print("RIGHT")
        label.pack(pady=ypad, padx=xpad, side=tk.RIGHT)
    else:
        print("none")
        label.pack(pady=ypad, padx=xpad,)
    dict_labels[name] = label
    return

def add_frame(name, parent, xpad, ypad, dict_frames, LorR, TorB, backg, fill):
    print(f"creating frame Widget named: {name} name with parent: {parent} pad x: {xpad} pad y: {ypad}")
    frame = tk.Frame(parent, bg=backg)
    if LorR.lower() == "left":
        print("LEFT")
        frame.pack(pady=ypad, padx=xpad, side=tk.LEFT)
    elif LorR.lower() == "right":
        print("RIGHT")
        frame.pack(pady=ypad, padx=xpad, side=tk.RIGHT)
    else:
        print("none")
    if fill.lower() == "x":
        print("fill X")
        frame.pack_configure(pady=ypad, padx=xpad,fill=tk.X,expand=True)
    elif fill.lower() == "y":
        print("fill Y")
        frame.pack_configure(pady=ypad, padx=xpad,fill=tk.Y)
    elif fill.lower() == "both":
        print ("fill both")
        frame.pack_configure(pady=ypad, padx=xpad,fill=tk.BOTH,expand=True)
    else:
        frame.pack_configure(pady=ypad, padx=xpad)
    dict_frames[name] = frame
    return

#------------Button actions------------
def play(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars):
    ls_root[0].withdraw()
    ls_root[2].deiconify()
    loop.begin_day_loop(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars) #manages the day cycle using the time and random modules and various loops and conditional branches
    loop.begin_loop(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars)#manages most behaviors, most of which are conditional if or elif or else statements, maybe some switch cases and various loops

    print("play!")

def quitgame(ls_root):
    ls_root.deiconify()
    ls_root.destroy()
    print("buttoneventinterupt-quit")

def settings(ls_root):
    if ls_root.winfo_exists():
        ls_root.deiconify()
    else:
        settings = tk.Toplevel()
        settings.title("Settings")
        settings.geometry("300x400")
        ls_root.insert(1 ,settings )
    print("open settings!")

def guidebook(ls_frame_windows, dict_frames):
    if ls_frame_windows[0].winfo_exists():
        ls_frame_windows[0].deiconify()
        print("guide exists")
    else:
        guide = msc.DraggableWindow(dict_frames["main frame"], title="Guide", x=80, y=80, w=500, h=600, color="grey")
        g_text = tk.Text(guide)
        g_text.pack(pady=20, padx=40,fill=tk.BOTH,expand=True)
        ls_frame_windows.insert(0 , guide)
        print("new guidebook created")
        

def run(root):
    print("it ran!", root)
    root.mainloop()

def show(ls_root):
    ls_root.deiconify()

def hide(ls_root):
    ls_root.withdraw()
