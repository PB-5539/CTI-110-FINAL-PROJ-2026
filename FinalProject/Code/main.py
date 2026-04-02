#Parker Behagg
#2/22/26 - 5/12/26
#FinalProject
# Create a game using the 'time' and 'random' modules and use loops and functions (include a main() function to run the program).

#----import python modules
import random as rdm
#----import internal modules
import ui
import pseudo_terminal as pt

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

    ui.create_main_ui("main window", "1920x1080", True, ls_root, ls_terminal, ls_frame_windows, dict_frames)
    print(ls_root)
    print("game now loading...")
    
    print(dict_buttons)
    ui.add_frame("game window", ls_root[2], 1, 1, dict_frames, "left", "None", "black", "Both")
    ui.add_frame("sidebar", dict_frames["game window"], 1, 1, dict_frames, "left", "None", "grey", "y")
    ui.add_frame("main frame", dict_frames["game window"], 1, 1, dict_frames, "left", "none", "grey", "both")
    pt.start_terminal(ls_terminal, ls_root, dict_frames)
    pt.startup(ls_terminal[0])

    pt.hide(ls_root[3])
    ui.hide(ls_root[2])
    ui.hide(ls_root[1])

    ui.add_button("play", ls_root[0], 20, 20, lambda: ui.play(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars), dict_buttons)
    ui.add_button("settings", ls_root[0], 20, 20, lambda: ui.settings(ls_root[1]), dict_buttons)
    ui.add_button("quit", ls_root[0], 20, 120, lambda: ui.quitgame(ls_root[0]), dict_buttons)

    ui.add_label("sidebar title", dict_frames["sidebar"], 20, 20, "sidebar!",  dict_labels, "none", "None", "light grey")
    ui.add_label("day counter", dict_frames["sidebar"], 20, 20, "", dict_labels, "none", "none", "light grey" )
    ui.add_label("timer", dict_frames["sidebar"], 20, 20, "", dict_labels, "none", "none", "light grey" )
    ui.add_button("Guide", dict_frames["sidebar"], 20, 120, lambda: ui.guidebook(ls_frame_windows, dict_frames), dict_buttons)

    ui.add_label("game window label", dict_frames["main frame"], 20, 20, f"------------------", dict_labels, "None", "None", "grey")
    ui.add_button("terminal", dict_frames["main frame"], 20, 20, lambda: pt.show(ls_root, ls_terminal, dict_frames), dict_buttons)

    ui.add_frame("top left", dict_frames["main frame"], 1, 1, dict_frames, "left", "None", "light grey", "both")
    ui.add_label("Life Support Systems", dict_frames["top left"], 20, 20, "Life Support Systems", dict_labels, "none", "none", "light grey")
    ui.add_frame("top middle", dict_frames["main frame"], 1, 1, dict_frames, "left", "None", "light grey", "both")
    ui.add_label("Propulsion Systems", dict_frames["top middle"], 20, 20, "Propulsion Systems", dict_labels, "none", "none", "light grey")
    ui.add_frame("top right", dict_frames["main frame"], 1, 1, dict_frames, "left", "None", "light grey", "both")
    ui.add_label("Structural Systems", dict_frames["top right"], 20, 20, "Structural Systems", dict_labels, "none", "none", "light grey")

    ui.add_slider("Air Flow Rate", dict_frames["top left"], 20, 20, dict_sliders)
    dict_sliders["Air Flow Rate"].set(100)
    
    #ui.add_label("cycle length")
    #au.play_audio("MainMenu.wav")

    #TO DO:
    #make an audio thread / play audio during cycles and have the cycle end when the music ends for variable cycle lengths
    #add day cycle using time and random modules
    #add a day counter and cycle tracker (time untill next cycle/day and how many cycles have passed)

    #run
    ls_root[2].protocol("WM_DELETE_WINDOW", lambda: ui.quitgame(ls_root[0]))
    ui.run(ls_root[0]) #THIS GOES AT THE END OF THE MAIN FUNCTION, ALL CODE AFTER IT WILL NOT RUN UNTILL THE WINDOWS HAVE EITHER BEEN CLOSED BY THE USER OR DESTROYRD VIA '<object name>.Destroy()'
#run game
main()