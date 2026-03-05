import math as mt
import random as rdm
import time as tm
import misc_utils as misc
import events as ev
import tasks as tsk
import alerts as als
import winsound as ws
import tkinter as tk
from tkinter import ttk

def start_terminal():
    ls_commands = ["hello","help","exit"]
    def handle_command(command):
        command = command.strip().lower()
        if command == "hello":
            return "Hi!"
        elif command == "help":
            return f"{ls_commands}"
        elif command == "exit":
            terminal.destroy()
        else:
            return f"Unknown command: {command}"

    def on_enter(event=None):
        cmd = entry.get()
        text_area.insert(tk.END, f"> {cmd}\n")
        entry.delete(0, tk.END)
        
        response = handle_command(cmd)
        if response:
            text_area.insert(tk.END, f"{response}\n")
        text_area.see(tk.END)
    def startup():
        text_area.insert(tk.END, f"initializing...\n")
        text_area.insert(tk.END, f"discovering disks...\n")
        text_area.insert(tk.END, f"reading bootloader...\n")
        text_area.insert(tk.END, f"Booting...\n")
        text_area.insert(tk.END, f"----EvrenOS----\n")
        text_area.insert(tk.END, f"Keyboard [OK]\n")
        text_area.insert(tk.END, f"CMD Loader [OK]\n")
        text_area.insert(tk.END, f"Display Out [OK]\n")
        text_area.insert(tk.END, f"Load [SUCCESS]\n")
        text_area.insert(tk.END, f"---------------\n")
        text_area.insert(tk.END, f'Welcome To EvrenOS, type "help" for a list of commands.\n')

    terminal = tk.Toplevel()
    terminal.title("Terminal")

    text_area = tk.Text(terminal, bg="black", fg="white")
    text_area.pack(pady=1, fill=tk.BOTH, expand=True)

    entry = tk.Entry(terminal, width=80, bg="gray15", fg="white", insertbackground="white")
    entry.pack(pady=1, fill=tk.X, expand=True)
    entry.bind("<Return>", on_enter)
    startup()
    entry.focus()