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

#----Thread-safe print lock
print_lock = th.Lock()

def safe_print(*args, **kwargs):
    """Thread-safe print function to prevent deadlock from concurrent prints."""
    with print_lock:
        print(*args, **kwargs)

#----Thread-safe widget update dictionary
pending_widget_updates = {}
pending_slider_values = {}
slider_current_values = {}  # Track slider values for background threads

def queue_config(widget_key, **kwargs):
    """Queue a widget config change (thread-safe). 
    Usage: queue_config("widget_name", text="new text", bg="red")
    """
    if widget_key not in pending_widget_updates:
        pending_widget_updates[widget_key] = {}
    pending_widget_updates[widget_key].update(kwargs)

def queue_slider_value(slider_key, value):
    """Queue a slider value change (thread-safe).
    Usage: queue_slider_value("Air Flow Rate", 50)
    """
    pending_slider_values[slider_key] = value

def loop(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars):
    tween_thread = None
    iteration_count = 0
    
    while True:
        iteration_count += 1
        
        # Only print every 100 iterations to reduce output
        if iteration_count % 100 == 0:
            safe_print(f"[GAME LOOP] Iteration {iteration_count}")
        
        #Main Game Logic---------------------\/
        dict_vars["p_valve"] = False
        #read all variables and write to local variables
        days = dict_vars["days"]
        current_cycle = dict_vars["current_cycle"]
        structural_integrity = dict_vars["structural_integrity"]
        life_support_system_integrity = dict_vars["life_support_system_integrity"]
        temperature_C = dict_vars["temperature_C"]
        temperature_F = dict_vars["temperature_F"]
        
        if tween_thread is None or not tween_thread.is_alive():
            tween_thread = th.Thread(target=misc.tween_slider, args=("Air Flow Rate", dict_sliders, rdm.randrange(5,185)), daemon=True)
            tween_thread.start()
            ls_threads.append(tween_thread)
        #goal is to keep it within the range of 60-130 and not let it be out of that range for more than 60 seconds and not at any extreme values (<15 and >185) for more than 25 seconds, if it is then the life support system integrity will decrease by 10 points every 2.5 seconds until it is back in the safe range, if it reaches 0  then the game is over
        #each day a percentage of the remaining integrity of each item will be repaired.    
        
        #write mutable variable dictionary for reading in the main thread
        dict_vars["structural_integrity"] = structural_integrity
        dict_vars["life_support_system_integrity"] = life_support_system_integrity
        dict_vars["temperature_C"] = temperature_C
        dict_vars["temperature_F"] = temperature_F
        #Main Game logic---------------------/\

def begin_loop(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars):
    thread = th.Thread(target=loop, args=(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars),  daemon=True)
    thread.start()
    ls_threads.append(thread)
    return thread

def day_loop(ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars):
    # NOTE: Removed problematic print of all shared objects - was causing deadlock
    # print("day loop ran", ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars)
    safe_print("[DAY LOOP] Starting day cycle...")
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
            queue_config("day counter", text=str(f"Day {day} (Tutorial)"))
            au.play_audio("TutorialTheme.wav")
            for i in range(int(f"{misc.get_duration("TutorialTheme.wav"):.0f}")):
                # Removed individual print - too many prints causing deadlock
                queue_config("timer", text=f"{int(misc.get_duration("TutorialTheme.wav") - (i))} seconds until Day {tomorrow}")
                queue_config("sidebar title", text=f"{tm.ctime()}")
                tm.sleep(1)
            day += 1
            true_day += 1
            safe_print("[DAY LOOP] Counted a day")
            safe_print(f"[DAY LOOP] Day: {day} Week: {week}")
            safe_print(f"[DAY LOOP] Tomorrow will be Day: {tomorrow}")
            safe_print(f"[DAY LOOP] True day: {true_day}")
        else:
            queue_config("day counter", text=str(f"Day: {day} Week: {week}"))
            au.play_audio(f"Theme{day}.wav")
            for i in range(int(f"{misc.get_duration(f'Theme{day}.wav'):.0f}")):
                # Removed individual print - too many prints causing deadlock
                queue_config("timer", text=f"{int(misc.get_duration(f'Theme{day}.wav') - (i))} seconds until Day {tomorrow}")
                queue_config("sidebar title", text=f"{tm.ctime()}")
                tm.sleep(1)
            day += 1
            true_day += 1
            safe_print("[DAY LOOP] Counted a day")
            safe_print(f"[DAY LOOP] Day: {day} Week: {week}")
            safe_print(f"[DAY LOOP] Tomorrow will be Day: {tomorrow}")
            safe_print(f"[DAY LOOP] True day: {true_day}")

        dict_vars["current_cycle"] = day
        dict_vars["current_cycle_week"] = week
        dict_vars["current_cycle_tday"] = true_day
    #MAIN DAY CYCLE TIMING LOGIC ----------/\

def begin_day_loop(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars):
    thread = th.Thread(target=day_loop, args=(ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars),  daemon=True)
    thread.start()
    ls_threads.append(thread)
    return thread