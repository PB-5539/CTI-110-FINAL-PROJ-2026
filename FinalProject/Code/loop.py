#----import python modules
import math as mt
import random as rdm
import time as tm
import threading as th
import tkinter as tk

#----import internal modules
import misc_utils as misc
import ui
import events as ev
import tasks as tsk
import alerts as als
import pseudo_terminal as pt

def loop(ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars):
    for i in range(100):
        print(ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars)
        #Main Game Logic---------------------\/
        print("game logic")
        #update local variables
        days = dict_vars["days"]
        current_cycle = dict_vars["current_cycle"]


        print(f"{days}\n{current_cycle}\n")
        #Main Game logic---------------------/\
def begin_loop(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars):
    thread = th.Thread(target=loop, args=(ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars),  daemon=True)
    thread.start()
    ls_threads.append(thread)
    return thread