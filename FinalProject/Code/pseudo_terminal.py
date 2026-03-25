import math as mt
import random as rdm
import time as tm
import ui
import misc_utils as misc
import events as ev
import tasks as tsk
import alerts as als
import winsound as ws
import tkinter as tk
from tkinter import ttk

def start_terminal(ls_terminal, ls_root, dict_frames):
    ls_commands = ["hello","help","exit", "nuke", "pseudo"] #pseudo will have a similar function to sudo with the pseudo-terminal because funnies lol
    def handle_command(command):
        command = command.strip().lower()
        if command == ls_commands[0]:
            return "Hi!"
        elif command == ls_commands[1]:
            return f"{ls_commands}\n"
        elif command == ls_commands[2]:
            hide(ls_root[3])
        elif command == ls_commands[3]:
            ui.quitgame(ls_root[0])
            return command
        else:
            return f"{command} : The term '{command}' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path was included, verify that the path is correct and try again."

    def on_enter(event=None):
        text_area.config(state=tk.NORMAL)
        cmd = entry.get()
        text_area.insert(tk.END, f"> {cmd}\n")
        entry.delete(0, tk.END)
        
        response = handle_command(cmd)
        if response and cmd != "nuke":
            text_area.insert(tk.END, f"{response}\n")
        if cmd != "nuke":
            text_area.see(tk.END)
            text_area.config(state=tk.DISABLED)

    terminal = misc.DraggableWindow(dict_frames["main frame"], title="Terminal", x=80, y=80, w=650, h=500, color="black")

    text_area = tk.Text(terminal, bg="black", fg="white")
    text_area.pack(pady=1, fill=tk.BOTH, expand=True)


    entry = tk.Entry(terminal, width=80, bg="gray15", fg="white", insertbackground="white")
    entry.pack(pady=1, fill=tk.X, expand=True)
    entry.bind("<Return>", on_enter)
    entry.focus()
    while len(ls_root) <= 3:
        ls_root.append(None)

    if len(ls_terminal) == 0:
        ls_terminal.append(None)

    ls_root[3] = terminal
    ls_terminal[0] = text_area

def startup(ls_terminal):
        ls_terminal.config(state=tk.NORMAL)
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
        ls_terminal.config(state=tk.DISABLED)  

def show(ls_root, ls_terminal, dict_frames):
    print(ls_root[3].winfo_exists())
    if ls_root[3].winfo_exists():
        ls_root[3].place(x=80, y=80, width=650, height=500)
    else:
        start_terminal(ls_terminal, ls_root, dict_frames)
        startup(ls_terminal[0])
        
def hide(ls_root):
    ls_root.place_forget()