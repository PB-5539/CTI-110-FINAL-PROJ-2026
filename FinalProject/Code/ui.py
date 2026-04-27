import threading as th
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
    root.configure(bg="silver")
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

def _anchor_from_sticky(sticky):
    sticky = str(sticky).lower().strip()
    if sticky in {"n", "s", "e", "w", "ne", "nw", "se", "sw", "nsew", "ns", "ew", "c", "center"}:
        return "center" if sticky == "center" else sticky
    return None


def add_button(name, parent, xpad, ypad, action, LorR, fill, sticky="none", dict_buttons=None, bg=None):
    print(f"creating Button Widget named: {name} name with parent: {parent} pad x: {xpad} pad y: {ypad} and action: {action}")
    button = tk.Button(parent, text=name, command=action, bg=bg)
    anchor = _anchor_from_sticky(sticky)
    pack_kwargs = {"pady": ypad, "padx": xpad}
    if anchor:
        pack_kwargs["anchor"] = anchor

    if LorR.lower() == "left":
        print("LEFT")
        pack_kwargs["side"] = tk.LEFT
    elif LorR.lower() == "right":
        print("RIGHT")
        pack_kwargs["side"] = tk.RIGHT
    else:
        print("none")

    button.pack(**pack_kwargs)
    if fill.lower() == "x":
        print("fill X")
        button.pack_configure(fill=tk.X, expand=True)
    elif fill.lower() == "y":
        print("fill Y")
        button.pack_configure(fill=tk.Y)
    elif fill.lower() == "both":
        print ("fill both")
        button.pack_configure(fill=tk.BOTH, expand=True)
    else:
        button.pack_configure()
    dict_buttons[name] = button
    return

def add_slider(name, parent, xpad, ypad, dict_sliders, start_value=0, sticky="none"):
    print(f"creating slider Widget named: {name} name with parent: {parent} pad x: {xpad} pad y: {ypad}")
    slider = tk.Scale(parent,from_=0, to=200, orient=tk.HORIZONTAL, label=f"{name}", command=lambda v: loop.slider_current_values.update({name: float(v)}))
    slider.set(start_value)
    anchor = _anchor_from_sticky(sticky)
    pack_kwargs = {"pady": ypad, "padx": xpad}
    if anchor:
        pack_kwargs["anchor"] = anchor
    slider.pack(**pack_kwargs)
    dict_sliders[name] = slider
    return

def add_label(name, parent, xpad, ypad, text, dict_labels, LorR, TorB, backg, fill, sticky="none"):
    print(f"creating label Widget named: {name} name with parent: {parent} pad x: {xpad} pad y: {ypad} and text: {text}")
    label = tk.Label(parent, text=text, bg=backg)
    anchor = _anchor_from_sticky(sticky)
    pack_kwargs = {"pady": ypad, "padx": xpad}
    if anchor:
        pack_kwargs["anchor"] = anchor
    if LorR.lower() == "left":
        print("LEFT")
        pack_kwargs["side"] = tk.LEFT
    elif LorR.lower() == "right":
        print("RIGHT")
        pack_kwargs["side"] = tk.RIGHT
    else:
        print("none")

    label.pack(**pack_kwargs)
    if fill.lower() == "x":
        print("fill X")
        label.pack_configure(fill=tk.X, expand=True)
    elif fill.lower() == "y":
        print("fill Y")
        label.pack_configure(fill=tk.Y)
    elif fill.lower() == "both":
        print ("fill both")
        label.pack_configure(fill=tk.BOTH, expand=True)
    else:
        label.pack_configure()
    dict_labels[name] = label
    return

def add_frame(name, parent, xpad, ypad, dict_frames, LorR, TorB, backg, fill, sticky="none"):
    print(f"creating frame Widget named: {name} name with parent: {parent} pad x: {xpad} pad y: {ypad}")
    frame = tk.Frame(parent, bg=backg)
    anchor = _anchor_from_sticky(sticky)
    pack_kwargs = {"pady": ypad, "padx": xpad}
    if anchor:
        pack_kwargs["anchor"] = anchor
    if LorR.lower() == "left":
        print("LEFT")
        pack_kwargs["side"] = tk.LEFT
    elif LorR.lower() == "right":
        print("RIGHT")
        pack_kwargs["side"] = tk.RIGHT
    else:
        print("none")

    frame.pack(**pack_kwargs)
    if fill.lower() == "x":
        print("fill X")
        frame.pack_configure(fill=tk.X, expand=True)
    elif fill.lower() == "y":
        print("fill Y")
        frame.pack_configure(fill=tk.Y)
    elif fill.lower() == "both":
        print ("fill both")
        frame.pack_configure(fill=tk.BOTH, expand=True)
    else:
        frame.pack_configure()
    dict_frames[name] = frame
    return

def add_text_area(name, parent, xpad, ypad, dict_text_areas, LorR, backg, fill, width=None, height=None, editable=True, sticky="none"):
    print(f"creating text area Widget named: {name} name with parent: {parent} pad x: {xpad} pad y: {ypad}")
    text_kwargs = {"bg": backg, "state": tk.NORMAL if editable else tk.DISABLED}
    if width is not None:
        text_kwargs["width"] = width
    if height is not None:
        text_kwargs["height"] = height
    text_area = tk.Text(parent, **text_kwargs)
    anchor = _anchor_from_sticky(sticky)
    pack_kwargs = {"pady": ypad, "padx": xpad}
    if anchor:
        pack_kwargs["anchor"] = anchor
    if LorR.lower() == "left":
        print("LEFT")
        pack_kwargs["side"] = tk.LEFT
    elif LorR.lower() == "right":
        print("RIGHT")
        pack_kwargs["side"] = tk.RIGHT
    else:
        print("none")

    text_area.pack(**pack_kwargs)
    if fill.lower() == "x":
        print("fill X")
        text_area.pack_configure(fill=tk.X, expand=True)
    elif fill.lower() == "y":
        print("fill Y")
        text_area.pack_configure(fill=tk.Y)
    elif fill.lower() == "both":
        print ("fill both")
        text_area.pack_configure(fill=tk.BOTH, expand=True)
    else:
        text_area.pack_configure()
    dict_text_areas[name] = text_area
    return

def add_graph(name, parent, xpad, ypad, dict_graphs, width=400, height=200, x_range=(0, 100), y_range=(0, 100), update_frequency_secs=1.0, background="white", point_size=3, line_size=2, sticky="none"):
    print(f"creating graph Widget named: {name} name with parent: {parent} pad x: {xpad} pad y: {ypad}")
    graph = msc.GraphDrawer(parent, width=width, height=height, x_range=x_range, y_range=y_range, update_frequency_secs=update_frequency_secs, background=background, point_size=point_size, line_size=line_size)
    anchor = _anchor_from_sticky(sticky)
    pack_kwargs = {"pady": ypad, "padx": xpad}
    if anchor:
        pack_kwargs["anchor"] = anchor
    graph.pack(**pack_kwargs)
    dict_graphs[name] = graph
    return graph

#------------Button actions------------
def play(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars, dict_text_areas, dict_graphs):
    ls_root[0].withdraw()
    ls_root[2].deiconify()
    loop.begin_day_loop(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars, dict_text_areas) #manages the day cycle using the time and random modules and various loops and conditional branches
    loop.begin_loop(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars, dict_text_areas)#manages most behaviors, most of which are conditional if or elif or else statements, maybe some switch cases and various loops
    loop.begin_speed_thread(ls_threads, dict_sliders, dict_labels, dict_vars, dict_graphs) #manages the speed slider and label updates in a separate thread to prevent blocking the main loop
    print("play!")
    dict_vars["play"] = True

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
