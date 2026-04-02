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
        tm.sleep(0.5)
        misc.tween_slider(dict_sliders["slidinator"], rdm.randrange(5,185))
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
    true_day = dict_vars["current_cycle_tday"]
    #MAIN DAY CYCLE TIMING LOGIC ----------\/
    #stuff
    while true_day <= dict_vars["days"]:
        day = dict_vars["current_cycle"]
        week = dict_vars["current_cycle_week"]
        if (day + 1)>7:
            if day == 7:
                tomorrow = f"1 (Week {week + 1})"
            else:
                tomorrow = f"2"
        else:
            tomorrow = day + 1
        if day > 7:
            day = 1
            week += 1
        if day == 0:
            dict_labels["day counter"].config(text=str(f"Day {day} (Tutorial)"))
            au.play_audio("TutorialTheme.wav")
            for i in range(int(f"{misc.get_duration("TutorialTheme.wav"):.0f}")):
                print(misc.get_duration("TutorialTheme.wav") - (i))
                dict_labels["timer"].config(text=f"{int(misc.get_duration("TutorialTheme.wav") - (i))} seconds until Day {tomorrow}")
                tm.sleep(1)
            day += 1
            true_day += 1
            print("counted a day")
            print(f"Day: {day} Week: {week}")
            print(f"Tomorrow will be Day: {tomorrow}")
            print(f"True day: {true_day}")
        else:
            dict_labels["day counter"].config(text=str(f"Day: {day} Week: {week}"))
            au.play_audio(f"Theme{day}.wav")
            for i in range(int(f"{misc.get_duration(f'Theme{day}.wav'):.0f}")):
                print(misc.get_duration(f"Theme{day:.0f}.wav") - (i))
                dict_labels["timer"].config(text=f"{int(misc.get_duration(f'Theme{day}.wav') - (i))} seconds until Day {tomorrow}")
                tm.sleep(1)
            day += 1
            true_day += 1
            print("counted a day")
            print(f"Day: {day} Week: {week}")
            print(f"Tomorrow will be Day: {tomorrow}")
            print(f"True day: {true_day}")

        print("counted a day")
        dict_vars["current_cycle"] = day
        dict_vars["current_cycle_week"] = week
        dict_vars["current_cycle_tday"] = true_day
    #MAIN DAY CYCLE TIMING LOGIC ----------/\

def begin_day_loop(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars):
    thread = th.Thread(target=day_loop, args=(ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars),  daemon=True)
    thread.start()
    ls_threads.append(thread)
    return thread