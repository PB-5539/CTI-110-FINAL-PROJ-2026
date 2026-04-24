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





#-----------------------------------------------------------------------ai----------------------------------------------------------------------------
#----Thread-safe print lock
print_lock = th.Lock()

def safe_print(*args, **kwargs):
    """Thread-safe print function to prevent deadlock from concurrent prints."""
    with print_lock:
        print(*args, **kwargs)

#----Thread-safe widget update dictionary
pending_widget_updates = {}
pending_slider_values = {}
pending_graph_updates = []
slider_current_values = {}  # Track slider values for background threads
graph_update_lock = th.Lock()

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

def queue_graph_update(graph_key, values, colors=None):
    """Queue a graph data update (thread-safe).
    values: dict[name -> value]
    colors: dict[name -> color]
    """
    if not isinstance(values, dict):
        return
    with graph_update_lock:
        pending_graph_updates.append((graph_key, values.copy(), colors.copy() if isinstance(colors, dict) else {}))
#-----------------------------------------------------------------------------------------------------------------------------------------------------




def loop(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars, dict_text_areas):
    tween_thread = None
    iteration_count = 0
    
    while True:
        #read all variables and write to local variables
        days = dict_vars["days"]
        current_cycle = dict_vars["current_cycle"]
        structural_integrity = dict_vars["structural_integrity"]
        life_support_system_integrity = dict_vars["life_support_system_integrity"]
        temperature_C = dict_vars["temperature_C"]
        temperature_F = dict_vars["temperature_F"]
        oxy_err = dict_vars["oxy_err"]
        iteration_count += 1
        
        # Only print every 100 iterations to reduce output
        if iteration_count % 100 == 0:
            safe_print(f"[GAME LOOP] Iteration {iteration_count}")



        
        #Main Game Logic---------------------\/
        
        
        if tween_thread is None or not tween_thread.is_alive():
            tween_thread = th.Thread(target=misc.tween_slider, args=("Air Flow Rate", dict_sliders, rdm.randrange(5,185)), daemon=True)
            tween_thread.start()
            ls_threads.append(tween_thread)
        if not(dict_sliders["Air Flow Rate"].get() > 60 and dict_sliders["Air Flow Rate"].get() < 130):
            if life_support_system_integrity > 5000:
                als.send_alert("Oxygen levels dropping!", 2, True, dict_text_areas, "alerts")
            elif life_support_system_integrity <= 5000:
                als.send_alert("Oxygen levels critical!", 3, True, dict_text_areas, "alerts")
            else:
                als.send_alert("Oxygen levels stable.", 1, False, dict_text_areas, "alerts")
            oxy_err = True
        else:
            oxy_err = False
        #goal is to keep it within the range of 60-130 and not let it be out of that range for more than 60 seconds and not at any extreme values (<15 and >185) for more than 25 seconds, if it is then the life support system integrity will decrease by 10 points every 2.5 seconds until it is back in the safe range, if it reaches 0  then the game is over
        #each day a percentage of the remaining integrity of each item will be repaired.
        
        #write mutable variable dictionary for reading in the main thread
        dict_vars["structural_integrity"] = structural_integrity
        dict_vars["life_support_system_integrity"] = life_support_system_integrity
        dict_vars["temperature_C"] = temperature_C
        dict_vars["temperature_F"] = temperature_F
        dict_vars["oxy_err"] = oxy_err
        #Main Game logic---------------------/\

def begin_loop(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars, dict_text_areas):
    thread = th.Thread(target=loop, args=(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars, dict_text_areas),  daemon=True)
    thread.start()
    ls_threads.append(thread)
    return thread

def day_loop(ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars, dict_text_areas):
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
            tutorial_duration = misc.get_duration("TutorialTheme.wav")
            for i in range(int(f"{tutorial_duration:.0f}")):

                queue_config("timer", text=f"{int(tutorial_duration - i)} seconds until Day {tomorrow}")
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

def begin_day_loop(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars, dict_text_areas):
    thread = th.Thread(target=day_loop, args=(ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars, dict_text_areas),  daemon=True)
    thread.start()
    ls_threads.append(thread)
    return thread

# Smoothly simulate a speed value based on the Main Throttle setting.
# This thread never reads the widget directly; it reads tracked throttle values from
# loop.slider_current_values and uses queue_config to update the "Speed" label safely.
# The target speed is derived from the slider value via (throttle * 335 / 200).
# The speed moves by a percentage of the remaining distance each 0.1 seconds.
#thread creation function to call on play.
def begin_speed_thread(ls_threads, dict_sliders, dict_labels, dict_vars, dict_graphs):
    thread = th.Thread(target=speed_thread, args=(dict_sliders, dict_labels, dict_vars, dict_graphs), daemon=True)
    thread.start()
    ls_threads.append(thread)
    return thread

#main function
def speed_thread(dict_sliders, dict_labels, dict_vars, dict_graphs):
    import random as rdm
    throttle_key = "Main Throttle"
    speed_label_key = "Speed"
    graph_key = "SpeedGraph"
    current_speed = 0.0
    accumulated_time = 0.0
    update_interval = dict_graphs[graph_key].update_frequency_secs if graph_key in dict_graphs else 1.0

    while True:
        # Read current throttle from the shared tracking dictionary.
        target_throttle = slider_current_values.get(throttle_key, 100.0)
        target_speed = target_throttle * (335.0 / 200.0)

        # Move speed toward target using 10% of the remaining distance.
        speed_difference = target_speed - current_speed
        if abs(speed_difference) <= 0.1:
            current_speed = target_speed
        else:
            current_speed += speed_difference * 0.1

        queue_config(speed_label_key, text=f"{current_speed:.2f} m/s")

        accumulated_time += 0.1
        if accumulated_time >= update_interval:
            accumulated_time -= update_interval
            queue_graph_update(graph_key, {"Speed": current_speed}, {"Speed": "light green"})

        tm.sleep(0.1)
