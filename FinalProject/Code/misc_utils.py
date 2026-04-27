import random as rdm
import math as mt
import time as tm
import wave
import contextlib
import os
import tkinter as tk
#-------------------------------------------------------------------------AI-----------------------------------------------------------
class GraphDrawer(tk.Canvas):
    def __init__(self, parent, width=400, height=200, x_range=(0, 100), y_range=(0, 100), update_frequency_secs=1.0, background="white", point_size=3, line_size=2, **kwargs):
        super().__init__(parent, width=width, height=height, bg=background, **kwargs)
        self.width = width
        self.height = height
        self.update_frequency_secs = float(update_frequency_secs)
        self._background_color = background
        self._padding = 10
        self.point_size = int(point_size)
        self.line_size = int(line_size)

        if isinstance(x_range, (tuple, list)) and len(x_range) == 2:
            self.x_min, self.x_max = float(x_range[0]), float(x_range[1])
        else:
            self.x_min, self.x_max = 0.0, float(x_range)

        if isinstance(y_range, (tuple, list)) and len(y_range) == 2:
            self.y_min, self.y_max = float(y_range[0]), float(y_range[1])
        else:
            self.y_min, self.y_max = 0.0, float(y_range)

        if self.x_max <= self.x_min:
            self.x_max = self.x_min + 1.0
        if self.y_max <= self.y_min:
            self.y_max = self.y_min + 1.0

        self._max_points = int(self.x_max - self.x_min) if self.x_max - self.x_min >= 1 else 1
        self.series_values = {}
        self.series_colors = {}
        self._update_id = None

        self._draw_grid()
        self.bind("<Motion>", self._on_mouse_move)
        self.bind("<Leave>", self._on_mouse_leave)

    def _draw_grid(self):
        self.delete("grid")
        self.create_rectangle(0, 0, self.width, self.height, fill=self._background_color, outline="", tags="grid")
        mid_y = self._padding + (self.height - 2 * self._padding) / 2
        self.create_line(self._padding, mid_y, self.width - self._padding, mid_y, fill="#999999", dash=(2, 4), tags="grid")
        self.create_line(self._padding, self._padding, self._padding, self.height - self._padding, fill="#999999", dash=(2, 4), tags="grid")

    def _draw_hover(self, x):
        self.delete("hover")
        if self._max_points < 1:
            return

        x = max(self._padding, min(self.width - self._padding, x))
        self.create_line(x, self._padding, x, self.height - self._padding, fill="yellow", dash=(3, 3), tags="hover")

        label_text = self._build_hover_label(x)
        if label_text:
            text_id = self.create_text(x + 10, self._padding + 5, text=label_text, anchor="nw", fill="white", font=("Arial", 9), tags="hover")
            bbox = self.bbox(text_id)
            if bbox:
                rect_id = self.create_rectangle(bbox[0] - 4, bbox[1] - 2, bbox[2] + 4, bbox[3] + 2, fill="black", outline="white", tags="hover")
                self.tag_lower(rect_id, text_id)

    def _build_hover_label(self, x):
        available_width = self.width - 2 * self._padding
        if available_width <= 0 or self._max_points < 2:
            return ""

        relative_x = x - self._padding
        if relative_x < 0:
            relative_x = 0
        if relative_x > available_width:
            relative_x = available_width

        idx = round((relative_x / available_width) * (self._max_points - 1))
        idx = max(0, min(self._max_points - 1, idx))

        lines = []
        for name, points in self.series_values.items():
            if idx < len(points):
                lines.append(f"{name}: {points[idx]:.2f}")
        return "\n".join(lines)

    def _on_mouse_move(self, event):
        if event.x < self._padding or event.x > self.width - self._padding or event.y < self._padding or event.y > self.height - self._padding:
            self._clear_hover()
            return
        self._draw_hover(event.x)

    def _on_mouse_leave(self, event):
        self._clear_hover()

    def _clear_hover(self):
        self.delete("hover")

    def _normalize_y(self, value):
        clamped = max(self.y_min, min(self.y_max, float(value)))
        span = self.y_max - self.y_min
        if span == 0:
            return self.height - self._padding
        return self.height - self._padding - ((clamped - self.y_min) / span) * (self.height - 2 * self._padding)

    def update(self, values: dict, colors: dict):
        if not isinstance(values, dict):
            return
        self.series_colors.update(colors or {})
        for name, value in values.items():
            if name not in self.series_values:
                self.series_values[name] = []
            self.series_values[name].append(float(value))
            while len(self.series_values[name]) > self._max_points:
                self.series_values[name].pop(0)
        self._redraw()

    def _redraw(self):
        self.delete("plot")
        if self._max_points < 2:
            return
        available_width = self.width - 2 * self._padding
        for name, points in self.series_values.items():
            if len(points) < 2:
                continue
            color = self.series_colors.get(name, "green")
            coords = []
            count = len(points)
            for index, value in enumerate(points):
                x = self._padding + (index / (self._max_points - 1)) * available_width
                y = self._normalize_y(value)
                coords.extend((x, y))
            self.create_line(*coords, fill=color, width=self.line_size, tags="plot")
            for index, value in enumerate(points):
                x = self._padding + (index / (self._max_points - 1)) * available_width
                y = self._normalize_y(value)
                self.create_oval(x - self.point_size, y - self.point_size, x + self.point_size, y + self.point_size, fill=color, outline=color, tags="plot")

    def clear(self):
        self.series_values.clear()
        self.delete("plot")

    def set_ranges(self, x_range=None, y_range=None):
        if x_range is not None:
            if isinstance(x_range, (tuple, list)) and len(x_range) == 2:
                self.x_min, self.x_max = float(x_range[0]), float(x_range[1])
            else:
                self.x_min, self.x_max = 0.0, float(x_range)
        if y_range is not None:
            if isinstance(y_range, (tuple, list)) and len(y_range) == 2:
                self.y_min, self.y_max = float(y_range[0]), float(y_range[1])
            else:
                self.y_min, self.y_max = 0.0, float(y_range)
        self._max_points = int(self.x_max - self.x_min) if self.x_max - self.x_min >= 1 else 1
        self._draw_grid()
        self._redraw()

    def start_auto_refresh(self, data_provider):
        self.stop_auto_refresh()
        def tick():
            values, colors = data_provider()
            self.update(values or {}, colors or {})
            self._update_id = self.after(int(self.update_frequency_secs * 1000), tick)
        tick()

    def stop_auto_refresh(self):
        if self._update_id is not None:
            self.after_cancel(self._update_id)
            self._update_id = None
#--------------------------------------------------------------------------------------------------------------------------------------

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
#---------------------------------------------------AI MODIFIED------------------------------------------------------------
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
    
    while epoch <= 40:  # Max 20 seconds (40 * 0.5s)
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
        
        tm.sleep(0.5)
def open_prerelval(dict_vars):
    dict_vars["p_valve"] = True