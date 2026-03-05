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

def start_terminal(ls_terminal):
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
            return f"{command} : The term '{command}' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path was included, verify that the path is correct and try again."

    def on_enter(event=None):
        text_area.config(state=tk.NORMAL)
        cmd = entry.get()
        text_area.insert(tk.END, f"> {cmd}\n")
        entry.delete(0, tk.END)
        
        response = handle_command(cmd)
        if response:
            text_area.insert(tk.END, f"{response}\n")
        text_area.see(tk.END)
        text_area.config(state=tk.DISABLED)

    terminal = tk.Toplevel()
    terminal.title("Terminal")

    text_area = tk.Text(terminal, bg="black", fg="white")
    text_area.pack(pady=1, fill=tk.BOTH, expand=True)


    entry = tk.Entry(terminal, width=80, bg="gray15", fg="white", insertbackground="white")
    entry.pack(pady=1, fill=tk.X, expand=True)
    entry.bind("<Return>", on_enter)
    entry.focus()
    ls_terminal.insert(0, text_area)

def startup(ls_terminal):
        ls_terminal.insert(tk.END, f"initializing...\n")    
        ls_terminal.insert(tk.END, f"discovering disks...\n")   
        ls_terminal.insert(tk.END, f"reading bootloader...\n")  
        ls_terminal.insert(tk.END, f"Booting...\n") 
        ls_terminal.insert(tk.END, f"----EvrenOS----\n")    
        ls_terminal.insert(tk.END, f"Keyboard [OK]\n")  
        ls_terminal.insert(tk.END, f"CMD Loader [OK]\n")    
        ls_terminal.insert(tk.END, f"Display Out [OK]\n")   
        ls_terminal.insert(tk.END, f"Load [SUCCESS]\n") 
        ls_terminal.insert(tk.END, f"---------------\n")    
        ls_terminal.insert(tk.END, f'Welcome To EvrenOS, type "help" for a list of commands.\n')    