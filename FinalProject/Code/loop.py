#----import python modules
import math as mt
import random as rdm
import time as tm
import threading as th
import tkinter as tk

#----import internal modules
import misc_utils as misc
import audio_utils as au
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
        #read all variables and write to local variables
        days = dict_vars["days"]
        current_cycle = dict_vars["current_cycle"]
        structural_integrity = dict_vars["structural_integrity"]
        life_support_system_integrity = dict_vars["life_support_system_integrity"]
        temperature_C = dict_vars["temperature_C"]
        temperature_F = dict_vars["temperature_F"]

        print(f"{days}\n{current_cycle}\n{structural_integrity}\n{life_support_system_integrity}\n{temperature_C}\n{temperature_F}\n")
        print(misc.get_duration("Theme1.wav"))
        #todo:
        #check if the main game window (not the root window) exists, if not then call the function ui.quitgame()
        #format tm.time() to an actual clock dictionary

        dict_labels["sidebar title"].config(text=f"{tm.ctime()}")

        #write mutable variable dictionary for reading in the main thread
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

def day_loop(ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars):
    print("day loop ran", ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars)
    dict_vars["current_cycle"] = 0
    #MAIN DAY CYCLE TIMING LOGIC ----------\/
    #stuff
    while True:
        day = dict_vars["current_cycle"]
        if day == 0:
            dict_labels["day counter"].config(text=str(day))
            au.play_audio("TutorialTheme.wav")
            for i in range(int(f"{misc.get_duration("TutorialTheme.wav"):.0f}")):
                print(misc.get_duration("TutorialTheme.wav") - (i))
                dict_labels["timer"].config(text=f"{int(misc.get_duration("TutorialTheme.wav") - (i))} seconds until day {day + 1}")
                tm.sleep(1)
            day += 1
            print("counted a day")
        else:
            dict_labels["day counter"].config(text=str(day))
            au.play_audio(f"Theme{day}.wav")
            for i in range(int(f"{misc.get_duration(f'Theme{day}.wav'):.0f}")):
                print(misc.get_duration(f"Theme{day:.0f}.wav") - (i))
                dict_labels["timer"].config(text=f"{int(misc.get_duration(f'Theme{day}.wav') - (i))} seconds until day {day + 1}")
                tm.sleep(1)
            day += 1
        print("counted a day")
        dict_vars["current_cycle"] = day
    #MAIN DAY CYCLE TIMING LOGIC ----------/\

def begin_day_loop(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars):
    thread = th.Thread(target=day_loop, args=(ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars),  daemon=True)
    thread.start()
    ls_threads.append(thread)
    return thread