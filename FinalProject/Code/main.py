#Parker Behagg
#2/22/26 - 5/12/26
#FinalProject
# Create a game using the 'time' and 'random' modules and use loops and functions (include a main() function to run the program).

#----import python modules
import math as mt
import random as rdm
import time as tm

#----import internal modules
import misc_utils as misc
import ui
import events as ev
import tasks as tsk
import alerts as als
import audio_utils as au
import pseudo_terminal as pt
import loop

#----initialize variables
#mutable variables are stored within a dictionary for a more easy way to transfer between threads using dict_vars["variable name"] to get the variable rather than passing through all the variables through the loop.begin_loop(...) function
#days = 0
#current_cycle = 0
#structural_integrity = 1000
#life_support_system_integrity = 1000
#temperature_C = 0
#temperature_F = 32
dict_vars = {"days":0, "current_cycle":0, "structural_integrity":0, "life_support_system_integrity":0, "temperature_C":0, "temperature_F":0}

dict_vars["days"] = 0
dict_vars["current_cycle"] = 0
dict_vars["structural_integrity"] = 1000
dict_vars["life_support_system_integrity"] = 1000
dict_vars["temperature_C"] = 0
dict_vars["temperature_F"] = 32
#create dictionaries and lists
ls_root = [] #0=root 1=settings menu 2=main game window 3=psedo-terminal
ls_terminal = [] #0=pseudo-terminal
ls_threads = [] #0=game logic loop thread

dict_buttons = {}
dict_sliders = {}
dict_labels = {}
dict_entries = {}
dict_frames = {}

#----Main function
def main():
    ui.create_main_ui("main window", "300x400", True, ls_root)
    print(ls_root)
    print("game now loading...")
    
    print(dict_buttons)
    
    pt.start_terminal(ls_terminal, ls_root)
    pt.startup(ls_terminal[0])
    pt.hide(ls_root[3])
    ui.hide(ls_root[2])
    ui.hide(ls_root[1])

    ui.add_button("play", ls_root[0], 20, 20, lambda: ui.play(ls_root), dict_buttons)
    ui.add_button("settings", ls_root[0], 20, 20, lambda: ui.settings(ls_root[1]), dict_buttons)
    ui.add_button("quit", ls_root[0], 20, 120, lambda: ui.quitgame(ls_root[0]), dict_buttons)

    ui.add_label("game window label", ls_root[2], 20, 20, f"------------------", dict_labels, "None", "None")
    ui.add_button("terminal", ls_root[2], 20, 20, lambda: pt.show(ls_root, ls_terminal), dict_buttons)
    ui.add_frame("sidebar", ls_root[2], 20, 20, dict_frames, "left", "None", "red")
    ui.add_label("sidebar title", dict_frames["sidebar"], 20, 20, "sidebar!",  dict_labels, "none", "None")
    #au.play_audio("MainMenu.wav")

    #TO DO: 
    #add top/botton alignment logic
    #make an audio thread

    
    #run
    loop.begin_loop(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars)
    ui.run(ls_root[0]) #THIS GOES AT THE END OF THE MAIN FUNCTION, ALL CODE AFTER IT WILL NOT RUN UNTILL THE WINDOWS HAVE EITHER BEEN CLOSED NY THE USER OR DESTROYRD VIA '<object name>.Destroy()'

#run game
main()