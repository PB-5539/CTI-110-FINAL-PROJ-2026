#this was generated using OpenAI's ChatGPT website with GPT-5
#this was generated using OpenAI's ChatGPT website with GPT-5
#this was generated using OpenAI's ChatGPT website with GPT-5
#this was generated using OpenAI's ChatGPT website with GPT-5
import tkinter as tk

class DraggableWindow(tk.Frame):
    def __init__(self, parent, title="Window", x=50, y=50, w=200, h=150, color="lightgray"):
        super().__init__(parent, bd=2, relief="raised", bg=color)
        self.master = parent

        # Position using place
        self.place(x=x, y=y, width=w, height=h)

        # Title bar
        self.title_bar = tk.Frame(self, bg="gray", height=20)
        self.title_bar.pack(fill="x")

        self.title_label = tk.Label(self.title_bar, text=title, bg="gray", fg="white")
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


# Main app
root = tk.Tk()
root.geometry("600x450")
root.title("Tkinter Window System Demo")

# Background frame (acts like your "main window")
background = tk.Frame(root, bg="darkblue")
background.place(relwidth=1, relheight=1)

# Create multiple draggable windows
win1 = DraggableWindow(root, title="Terminal", x=80, y=80, color="#2b2b2b")
tk.Label(win1.content, text="> hello world", fg="lime", bg="#2b2b2b").pack(padx=10, pady=10)

win2 = DraggableWindow(root, title="Guidebook", x=200, y=150, color="#ddd")
tk.Label(win2.content, text="This is your guidebook!", bg="#ddd").pack(padx=10, pady=10)

win3 = DraggableWindow(root, title="Extra Panel", x=150, y=50, color="#cce")
tk.Button(win3.content, text="Click me").pack(padx=10, pady=10)

root.mainloop()