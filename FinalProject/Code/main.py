#Parker Behagg
#2/22/26 - 5/12/26
#FinalProject
# Create a game using the 'time' and 'random' modules and use loops and functions (include a main() function to run the program).

#----import python modules
import random as rdm
import time as tm
import tkinter as tk
#----import internal modules
import ui
import misc_utils as misc
import pseudo_terminal as pt
import loop

#----Main function
def main():
    #----initialize variables
    #mutable variables are stored within a dictionary for a more easy way to transfer between threads using dict_vars["variable name"] to get the variable rather than passing through all the variables through the loop.begin_loop(...) function
    dict_vars = {"days":0, "current_cycle":0, "structural_integrity":0, "life_support_system_integrity":0, "temperature_C":0, "temperature_F":0}
    dict_vars["days"] = rdm.randrange(30,55,1)
    dict_vars["current_cycle"] = 0
    dict_vars["current_cycle_week"] = 1
    dict_vars["current_cycle_tday"] = 0
    dict_vars["structural_integrity"] = 1000
    dict_vars["life_support_system_integrity"] = 1000
    dict_vars["propulsion_system_integrity"] = 1000
    dict_vars["temperature_C"] = 0
    dict_vars["temperature_F"] = 32
    dict_vars["fun_value"] = rdm.randrange(0,100)
    #the fun value is a variable hidden from the user that dictates the rate of occurance for random events.
    dict_vars["oxy_err"] = False
    dict_vars["sens_err"] = False
    dict_vars["align_err"] = False
    #create dictionaries and lists
    ls_root = [] #0=root 1=settings menu 2=main game window 3=psedo-terminal
    ls_terminal = [] #0=pseudo-terminal text area
    ls_threads = [] #0=game logic loop thread
    ls_frame_windows = []#0=Guidebook #1=terminal

    dict_buttons = {}
    dict_sliders = {}
    dict_labels = {}
    dict_entries = {}
    dict_frames = {}
    dict_text_areas = {}


    ui.create_main_ui("main window", "1920x1080", True, ls_root, ls_terminal, ls_frame_windows, dict_frames)
    print(ls_root)
    print("game now loading...")
    
    print(dict_buttons)
    ui.add_frame("game window", ls_root[2], 1, 1, dict_frames, "left", "None", "black", "Both", "none")
    ui.add_frame("sidebar", dict_frames["game window"], 1, 1, dict_frames, "left", "None", "grey", "y", "none")
    ui.add_frame("main frame", dict_frames["game window"], 1, 1, dict_frames, "left", "none", "grey", "both", "none")
    pt.start_terminal(ls_terminal, ls_root, dict_frames)
    pt.startup(ls_terminal[0])

    pt.hide(ls_root[3])
    ui.hide(ls_root[2])
    ui.hide(ls_root[1])

    ui.add_button("play", ls_root[0], 20, 20, lambda: ui.play(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars, dict_text_areas),"none","none","none", dict_buttons)
    ui.add_button("settings", ls_root[0], 20, 20, lambda: ui.settings(ls_root[1]),"none","none","none", dict_buttons)
    ui.add_button("quit", ls_root[0], 20, 120, lambda: ui.quitgame(ls_root[0]),"none","none","none", dict_buttons)

    ui.add_label("sidebar title", dict_frames["sidebar"], 20, 20, "sidebar!",  dict_labels, "none", "None", "light grey", "none", "none")
    ui.add_label("day counter", dict_frames["sidebar"], 20, 20, "", dict_labels, "none", "none", "light grey", "none", "none")
    ui.add_label("timer", dict_frames["sidebar"], 20, 20, "", dict_labels, "none", "none", "light grey", "none", "none")
    ui.add_text_area("alerts", dict_frames["sidebar"], 20, 20, dict_text_areas, "none", "light grey", "y", 30, None, False, "none")
    ui.add_button("Guide", dict_frames["sidebar"], 20, 120, lambda: ui.guidebook(ls_frame_windows, dict_frames),"none","none","none", dict_buttons)

    ui.add_label("game window label", dict_frames["main frame"], 20, 20, f"------------------", dict_labels, "None", "None", "grey", "none", "none")
    ui.add_button("terminal", dict_frames["main frame"], 20, 20, lambda: pt.show(ls_root, ls_terminal, dict_frames),"none","none","none", dict_buttons)

    ui.add_frame("top left", dict_frames["main frame"], 1, 1, dict_frames, "left", "None", "silver", "both", "none")
    ui.add_label("Life Support Systems", dict_frames["top left"], 20, 20, "Life Support Systems", dict_labels, "none", "none", "silver", "none", "none")
    ui.add_frame("top middle", dict_frames["main frame"], 1, 1, dict_frames, "left", "None", "light grey", "both", "none")
    ui.add_label("Propulsion Systems", dict_frames["top middle"], 20, 20, "Propulsion Systems", dict_labels, "none", "none", "light grey", "none", "none")
    ui.add_frame("top right", dict_frames["main frame"], 1, 1, dict_frames, "left", "None", "silver", "both", "none")
    ui.add_label("Structural Systems", dict_frames["top right"], 20, 20, "Structural Systems", dict_labels, "none", "none", "silver", "none", "none")

#------------------------------------------------------------------------Life Support Systems------------------------------------------------------------
    ui.add_frame("Left-sub-0", dict_frames["top left"], 1, 1, dict_frames, "none", "None", "silver", "none", "none")
    ui.add_frame("Left-sub-1", dict_frames["top left"], 1, 1, dict_frames, "none", "None", "silver", "none", "none")
    ui.add_button("Change Air Filter", dict_frames["Left-sub-1"], 1, 1,lambda: print("Changing air filter"),"Left","none","none", dict_buttons)
    ui.add_label("filter timer", dict_frames["Left-sub-1"], 3, 1, "10", dict_labels, "Left", "none", "white", "none", "none")
    ui.add_slider("Air Flow Rate", dict_frames["top left"], 20, 20, dict_sliders, "none")
    
    
    
    ui.add_frame("left-sub-3", dict_frames["top left"], 1, 1, dict_frames, "none", "None", "silver", "none", "none")
    
    ui.add_frame("left-sub-1.5", dict_frames["left-sub-3"], 20, 1, dict_frames, "none", "none", "light grey", "x", "none")
    ui.add_frame("sub1.5-sub1", dict_frames["left-sub-1.5"], 1, 1, dict_frames, "none", "none", "light grey", "x", "none")
    ui.add_label("temp-label", dict_frames["sub1.5-sub1"], 5, 0, "Temperature", dict_labels, "left", "none", "light grey", "none", "none")
    dict_labels["temp-label"].config(font=("Arial", 8))
    ui.add_label("Temperature", dict_frames["left-sub-1.5"], 5, 5, "75", dict_labels, "none", "none", "light green", "x", "none")
    dict_labels["Temperature"].config(font=("Arial", 18))
    
    ui.add_frame("Left-sub-2", dict_frames["left-sub-3"], 1, 1, dict_frames, "none", "None", "silver", "none", "none")
    ui.add_frame("sub-2-sub-1", dict_frames["Left-sub-2"], 20, 1, dict_frames, "none", "None", "light grey", "x", "none")
    ui.add_button("Air Conditioner", dict_frames["sub-2-sub-1"], 20, 1,lambda: print("AC toggle"),"Left","none","none", dict_buttons)
    ui.add_label("AC state", dict_frames["sub-2-sub-1"], 20, 20, "Off", dict_labels, "none", "none", "silver", "none", "none")
    ui.add_frame("sub-2-sub-2", dict_frames["Left-sub-2"], 20, 1, dict_frames, "none", "none", "light grey", "x", "none")
    ui.add_button("Heat", dict_frames["sub-2-sub-2"], 20, 1,lambda: print("heat toggle"),"Left","x","none", dict_buttons)
    ui.add_label("Structural Systems", dict_frames["sub-2-sub-2"], 20, 20, "Off", dict_labels, "none", "none", "silver", "none", "none")
#------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------Propulsion Systems------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------Structural Systems------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------AI----------------------------------------------------------------

    #----Thread-safe widget update handler
    update_counter = 0
    
    # Initialize slider tracking for background threads
    for slider_key in dict_sliders.keys():
        try:
            loop.slider_current_values[slider_key] = dict_sliders[slider_key].get()
        except:
            loop.slider_current_values[slider_key] = 100
    
    def update_widgets():
        """
        Process all queued widget updates on the main tkinter thread.
        This runs as fast as possible (1ms) to apply changes from background threads safely.
        """
        nonlocal update_counter
        update_counter += 1
        
        # Process widget config updates
        if loop.pending_widget_updates:
            for widget_key, attrs in list(loop.pending_widget_updates.items()):
                # Find the widget in the dictionaries
                widget = None
                if widget_key in dict_labels:
                    widget = dict_labels[widget_key]
                elif widget_key in dict_buttons:
                    widget = dict_buttons[widget_key]
                elif widget_key in dict_sliders:
                    widget = dict_sliders[widget_key]
                elif widget_key in dict_frames:
                    widget = dict_frames[widget_key]
                
                # Apply the update SAFELY on main thread
                if widget:
                    try:
                        widget.config(**attrs)
                    except tk.TclError:
                        pass  # Widget was destroyed, skip it
            
            # Clear processed updates
            loop.pending_widget_updates.clear()
        
        # Process slider value updates
        if hasattr(loop, 'pending_slider_values') and loop.pending_slider_values:
            for slider_key, value in list(loop.pending_slider_values.items()):
                if slider_key in dict_sliders:
                    try:
                        current_widget_value = dict_sliders[slider_key].get()
                        tracked_value = loop.slider_current_values.get(slider_key, current_widget_value)
                        if current_widget_value == tracked_value:
                            # No manual change, apply the queued update
                            dict_sliders[slider_key].set(value)
                            loop.slider_current_values[slider_key] = value
                        else:
                            # Manual change detected, update tracking to current widget value instead
                            loop.slider_current_values[slider_key] = current_widget_value
                    except tk.TclError:
                        pass  # Widget was destroyed, skip it
            
            # Clear processed updates
            loop.pending_slider_values.clear()
        
        # Schedule next update as fast as possible (1ms)
        ls_root[0].after(1, update_widgets)
    
    # Start the widget update handler
    update_widgets()
#-------------------------------------------------------------------------------------------------------------------------------------------


    #run
    ls_root[2].protocol("WM_DELETE_WINDOW", lambda: ui.quitgame(ls_root[0]))
    ui.run(ls_root[0]) #THIS GOES AT THE END OF THE MAIN FUNCTION, ALL CODE AFTER IT WILL NOT RUN UNTILL THE WINDOWS HAVE EITHER BEEN CLOSED BY THE USER OR DESTROYRD VIA '<object name>.Destroy()'
#run game
main()