import random as rdm
import time as tm
import math
import tkinter as tk

# Track last alert send times to prevent duplicate alerts within 30 seconds
_alert_history = {}

def send_alert(text, urgency, sound, dict_text_areas=None, text_area_name=None): #urgency will be on a 1-3 scale
    global _alert_history
    
    # Create a key for this specific alert
    alert_key = (text, urgency, sound)
    current_time = tm.time()
    
    # Check if this alert was sent recently (within 30 seconds)
    if alert_key in _alert_history:
        last_sent_time = _alert_history[alert_key]
        if current_time - last_sent_time < 30:
            return  # Don't send, too recent
    
    # Update the last send time for this alert
    _alert_history[alert_key] = current_time
    
    print(f"sending alert: [{text}] with urgency rating of: {urgency}/3 with sound condition: {sound}")
    
    # Write alert to text area if dict_text_areas and text_area_name are provided
    if dict_text_areas is not None and text_area_name is not None:
        if text_area_name in dict_text_areas:
            text_widget = dict_text_areas[text_area_name]
            # Make writable
            text_widget.config(state=tk.NORMAL)
            # Write alert
            text_widget.insert(tk.END, f"[ALERT - Urgency {urgency}/3] {text}\n")
            # Make read-only again
            text_widget.config(state=tk.DISABLED)
