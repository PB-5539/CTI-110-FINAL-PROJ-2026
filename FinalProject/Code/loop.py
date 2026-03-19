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
    while True:
        print(ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars)
        #Main Game Logic---------------------\/
        print("game logic")
        #update local variables
        days = dict_vars["days"]
        current_cycle = dict_vars["current_cycle"]
        structural_integrity = dict_vars["structural_integrity"]
        life_support_system_integrity = dict_vars["life_support_system_integrity"]
        temperature_C = dict_vars["temperature_C"]
        temperature_F = dict_vars["temperature_F"]

        print(f"{days}\n{current_cycle}\n{structural_integrity}\n{life_support_system_integrity}\n{temperature_C}\n{temperature_F}\n")

        #todo:
        #check if the main game window (not the root window) exists, if not then call the function ui.quitgame()
        #format tm.time() to an actual clock dictionary






        #write to variable dictionary for reading in the main thread
        dict_vars["days"] = days
        dict_vars["current_cycle"] = current_cycle
        dict_vars["structural_integrity"] = structural_integrity
        dict_vars["life_support_system_integrity"] = life_support_system_integrity
        dict_vars["temperature_C"] = temperature_C
        dict_vars["temperature_F"] = temperature_F
        #Main Game logic---------------------/\
def begin_loop(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars):
    thread = th.Thread(target=loop, args=(ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars),  daemon=True)
    thread.start()
    ls_threads.append(thread)
    return thread