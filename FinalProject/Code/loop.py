#----import python modules
import math as mt
import random as rdm
import time as tm
import threading as th
import tkinter as tk
import numpy as np
import os
import soundfile as sf


#----import internal modules
import misc_utils as misc
import audio_utils as au
import ui
import events as ev
import tasks as tsk
import alerts as als
import pseudo_terminal as pt

#use for loops for iterations of while loop running with a tm.sleep(0.01) at the end and check for whether how much has passed by a if (iteration) % 100 : #would run every second and still let other programs run seperatley.





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
#-----------------------------------------------------------------------AI--------------------------------------------------------------------------------------------------------------------------------------------------------------
#----Audio Analysis Cache
audio_analysis_cache = {}

def analyze_audio_file(filepath):
    """Analyze audio file and extract simple audio features.
    Each feature has its own independent 0-100 range based on the audio file's characteristics.
    """
    if filepath in audio_analysis_cache:
        safe_print(f"[AUDIO ANALYSIS] Using cached analysis for {filepath}")
        return audio_analysis_cache[filepath]
    
    try:
        # Construct full path to audio file (matching audio_utils.py path structure)
        full_path = os.path.join("finalproject", "Audio", "WAV", filepath)
        safe_print(f"[AUDIO ANALYSIS] Loading file: {full_path}")
        
        # Check if file exists
        if not os.path.isfile(full_path):
            safe_print(f"[AUDIO ANALYSIS ERROR] File not found: {full_path}")
            return None
        
        # Load audio file using soundfile
        safe_print(f"[AUDIO ANALYSIS] Reading audio with soundfile...")
        audio_data, sample_rate = sf.read(full_path)
        safe_print(f"[AUDIO ANALYSIS] Loaded: sample_rate={sample_rate}, shape={audio_data.shape}")
        
        # Handle stereo/mono
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)  # Convert stereo to mono
        
        # Calculate frames for 0.1s steps
        frame_size = int(sample_rate * 0.1)
        num_frames = len(audio_data) // frame_size
        safe_print(f"[AUDIO ANALYSIS] Frame size: {frame_size}, Total frames: {num_frames}")
        
        # First pass: Calculate all raw features to find min/max
        raw_features = []
        
        for i in range(num_frames):
            start_idx = i * frame_size
            end_idx = start_idx + frame_size
            frame = audio_data[start_idx:end_idx]
            
            # Feature 1: Progress (0-1 based on position in song, with random noise)
            progress = i / num_frames * 100
            noise = rdm.uniform(-5, 5)
            progress_with_noise = np.clip(progress + noise, 0, 100)
            
            # Feature 2: Frequency Content (estimated from zero crossing rate)
            # More zero crossings = higher frequency content
            zero_crossings = np.sum(np.abs(np.diff(np.sign(frame)))) / 2
            freq_estimate = (zero_crossings / len(frame)) * 100
            
            # Feature 3: Brightness (spectral centroid approximation)
            # High frequency content estimation
            fft = np.abs(np.fft.fft(frame))
            freqs = np.fft.fftfreq(len(frame), 1/sample_rate)
            brightness = np.sum(fft[:len(fft)//2]) / len(fft) * 100
            
            # Feature 4: Energy Envelope (RMS with smooth trending)
            rms = np.sqrt(np.mean(frame ** 2)) * 100
            
            # Feature 5: Attack/Release (how fast amplitude changes)
            amplitude_changes = np.abs(np.diff(np.abs(frame)))
            attack_release = np.mean(amplitude_changes) * 1000
            
            raw_features.append({
                "Progress": progress_with_noise,
                "Frequency": freq_estimate,
                "Brightness": brightness,
                "Energy": rms,
                "Attack": attack_release
            })
        
        # Find min/max for each feature
        feature_names = ["Progress", "Frequency", "Brightness", "Energy", "Attack"]
        feature_ranges = {}
        
        for feature_name in feature_names:
            values = [f[feature_name] for f in raw_features]
            feature_ranges[feature_name] = {
                "min": min(values),
                "max": max(values)
            }
        
        safe_print(f"[AUDIO ANALYSIS] Feature ranges:")
        for feature_name, range_dict in feature_ranges.items():
            safe_print(f"  {feature_name}: {range_dict['min']:.4f} - {range_dict['max']:.4f}")
        
        # Second pass: Normalize each feature to 0-100 range independently
        frames_data = []
        
        for raw_frame in raw_features:
            normalized_frame = {}
            for feature_name in feature_names:
                raw_val = raw_frame[feature_name]
                feat_min = feature_ranges[feature_name]["min"]
                feat_max = feature_ranges[feature_name]["max"]
                
                # Normalize to 0-100
                if feat_max > feat_min:
                    normalized_val = ((raw_val - feat_min) / (feat_max - feat_min)) * 100
                else:
                    normalized_val = 50  # Default middle if no range
                
                normalized_frame[feature_name] = max(0, min(100, normalized_val))
            
            frames_data.append(normalized_frame)
        
        safe_print(f"[AUDIO ANALYSIS] Extracted and normalized {len(frames_data)} frames successfully")
        audio_analysis_cache[filepath] = frames_data
        return frames_data
        
    except Exception as e:
        safe_print(f"[AUDIO ANALYSIS ERROR] {e}")
        import traceback
        traceback.print_exc()
        return None

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
        if (dict_sliders["Air Flow Rate"].get() < 60):
            if life_support_system_integrity > 5000 and life_support_system_integrity <= 15000:
                als.send_alert("Oxygen levels low", 2, True, dict_text_areas, "alerts")
            elif life_support_system_integrity <= 1000:
                als.send_alert("Oxygen levels critical", 3, True, dict_text_areas, "alerts")
            else:
                als.send_alert("Oxygen levels falling", 1, False, dict_text_areas, "alerts")
            oxy_err = True
            life_support_system_integrity -= 3
            tm.sleep(0.1)
        elif (dict_sliders["Air Flow Rate"].get() > 130):
            if life_support_system_integrity > 5000 and life_support_system_integrity <= 15000:
                als.send_alert("Oxygen levels high", 2, True, dict_text_areas, "alerts")
            elif life_support_system_integrity <= 1000:
                als.send_alert("Oxygen levels critical", 3, True, dict_text_areas, "alerts")
            else:
                als.send_alert("Oxygen levels rising", 1, False, dict_text_areas, "alerts")
            oxy_err = True
            life_support_system_integrity -= 1
            tm.sleep(0.1)
        elif dict_sliders["Air Flow Rate"].get() >60 and dict_sliders["Air Flow Rate"].get() < 130:
            oxy_err = False
            als.reset_alert_delay(("Oxygen levels low", 2, True))
            als.reset_alert_delay(("Oxygen levels critical", 3, True))
            als.reset_alert_delay(("Oxygen levels falling", 1, False))
            als.reset_alert_delay(("Oxygen levels high", 2, True))
            als.reset_alert_delay(("Oxygen levels critical", 3, True))
            als.reset_alert_delay(("Oxygen levels rising", 1, False))
            als.send_alert("Oxygen levels stable", 0, False, dict_text_areas, "alerts")
        #goal is to keep it within the range of 60-130 and not let it be out of that range for more than 60 seconds and not at any extreme values (<15 and >185) for more than 25 seconds, if it is then the life support system integrity will decrease by 10 points every 2.5 seconds until it is back in the safe range, if it reaches 0  then the game is over
        #each day a percentage of the remaining integrity of each item will be repaired.
        


    #if you're looking for the where the commit message refrenced, it's not here anymore.



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
#------------------------------------------------------------------------------AI-----------------------------------------------------------------------------
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
        target_speed = target_throttle * (rdm.randint(300, 360) / 200.0)

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
#------------------------------------------------------------------------------------------------------------------------------------------------------

def start_fun_thread(ls_threads, dict_vars):
    thread = th.Thread(target=fun_thread,args=(dict_vars,), daemon=True)
    thread.start()
    ls_threads.append(thread)
    return thread
#turns out, somehow between debugging a wierd situation with the threading module and passing arguments, i learned what a string indice is as well as how to make arguments optional!
#also why the hell does threading by default try to pass arguments as the value they represent not the item itself like how passing dict_vars was trying to pass 14 different arguments probably each tied to a key:value pair.
#modules are wierd, threading is wierder, it works now, thats all I care about.

#----------------------------------------------------------------------------------------AI Modified Fun Thread--------------------------------------------------------------------------------------
def fun_thread(dict_vars):
    while not dict_vars['play']:
        audio_file = "MainMenu.wav"
        safe_print("[FUN THREAD] Starting fun_thread")
        au.play_audio(audio_file)
        
        # Analyze audio file
        safe_print("[FUN THREAD] Analyzing audio file...")
        frames_data = analyze_audio_file(audio_file)
        if frames_data is None:
            safe_print("[FUN THREAD] Audio analysis failed, skipping this iteration")
            tm.sleep(1)
            continue
        
        safe_print(f"[FUN THREAD] Got {len(frames_data)} frames of audio data")
        
        # Get total duration
        total_duration = misc.get_duration(audio_file)
        safe_print(f"[FUN THREAD] Audio duration: {total_duration}s")
        
        frame_index = 0
        
        # Play audio reactively through its features
        while frame_index < len(frames_data) and not dict_vars['play']:
            frame_values = frames_data[frame_index]
            
            # Map each line to its own vertical range to prevent overlap
            # Line 1 (Progress): 0-20 - Runtime with randomization
            # Line 2 (Frequency): 20-40 - Pitch/frequency content
            # Line 3 (Brightness): 40-60 - Brightness/spectral content
            # Line 4 (Energy): 60-80 - Energy envelope
            # Line 5 (Attack): 80-100 - Attack/release sharpness
            
            progress_scaled = (frame_values["Progress"] / 100) * 20 + 0
            freq_scaled = (frame_values["Frequency"] / 100) * 40 + 20
            bright_scaled = (frame_values["Brightness"] / 100) * 20 + 40
            energy_scaled = (frame_values["Energy"] / 100) * 20 + 60
            attack_scaled = (frame_values["Attack"] / 100) * 20 + 80
            
            # Queue graph updates with non-overlapping ranges
            queue_graph_update("FunGraph", {
                "Progress": progress_scaled*2,
                "Frequency": freq_scaled,
                "Brightness": bright_scaled,
                "Energy": energy_scaled,
                "Attack": attack_scaled
            }, {
                "Progress": "blue",
                "Frequency": "red",
                "Brightness": "green",
                "Energy": "yellow",
                "Attack": "cyan"
            })
            
            if frame_index % 10 == 0:  # Print every 1 second
                safe_print(f"[FUN THREAD] Frame {frame_index}: Progress={progress_scaled:.1f} Freq={freq_scaled:.1f} Bright={bright_scaled:.1f} Energy={energy_scaled:.1f} Attack={attack_scaled:.1f}")
            
            frame_index += 1
            tm.sleep(0.1)