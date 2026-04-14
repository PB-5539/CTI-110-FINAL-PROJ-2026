import random as rdm
import math as mt
import time as tm
import wave
import contextlib
import os
import tkinter as tk

def get_duration(filename):
    fname = r'finalproject/audio/wav/'+filename
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        print(f"Duration: {duration:.0f} seconds")
        return duration

class DraggableWindow(tk.Frame):
    def __init__(self, parent, title="Window", x=50, y=50, w=200, h=150, color="lightgray"):
        super().__init__(parent, bd=2, relief="raised", bg=color)
        self.master = parent

        # Position using place
        self.place(x=x, y=y, width=w, height=h)

        # Title bar
        self.title_bar = tk.Frame(self, bg="dimgray", height=20)
        self.title_bar.pack(fill="x")

        self.title_label = tk.Label(self.title_bar, text=title, bg="dimgray", fg="white")
        self.title_label.pack(side="left", padx=5)

        # Close button
        self.close_button = tk.Button(self.title_bar, text="X", bg="light grey", fg="Black",bd=0, command=self.destroy)
        self.close_button.pack(side="right", padx=5)

        # Content area
        self.content = tk.Frame(self, bg=color)
        self.content.pack(fill="both", expand=True)

        # Drag bindings (only on title bar, not the close button!)
        self.title_bar.bind("<Button-1>", self.start_drag)
        self.title_bar.bind("<B1-Motion>", self.drag)

        # Bring to front on click (anywhere in window)
        self.bind("<Button-1>", self.bring_to_front)
        self.title_bar.bind("<Button-1>", self.start_drag)
        self.title_label.bind("<Button-1>", self.start_drag)

    def bring_to_front(self, event=None):
        self.lift()

    def start_drag(self, event):
        self.lift()
        self._drag_x = event.x
        self._drag_y = event.y

    def drag(self, event):
        new_x = self.winfo_x() + event.x - self._drag_x
        new_y = self.winfo_y() + event.y - self._drag_y

        # Clamp inside parent
        parent_width = self.master.winfo_width()
        parent_height = self.master.winfo_height()
        win_width = self.winfo_width()
        win_height = self.winfo_height()
        new_x = max(0, min(new_x, parent_width - win_width))
        new_y = max(0, min(new_y, parent_height - win_height))

        self.place(x=new_x, y=new_y)
        
def slider_value(slider):
    return slider.get()

def tween_slider(slider_key, slider_dict, target):
    """Tween a slider value smoothly over time (queue-safe for background threads).
    NEVER reads directly from slider widget - uses queued value tracking instead.
    
    Args:
        slider_key: The key name for the slider (must match in dict_sliders)
        slider_dict: The dict_sliders dictionary from main
        target: Target value to reach
    """
    import loop
    
    epoch = 0
    
    while epoch <= 100:
        # Re-read current value each iteration to respect manual changes
        current_value = loop.slider_current_values.get(slider_key, 100)
        
        if current_value == target:
            break  # Reached target
        
        epoch += 1
        
        if current_value < target:
            current_value += 1
            loop.queue_slider_value(slider_key, current_value)
        elif current_value > target:
            current_value -= 1
            loop.queue_slider_value(slider_key, current_value)
        
        tm.sleep(0.1)
def open_prerelval(dict_vars):
    dict_vars["p_valve"] = True