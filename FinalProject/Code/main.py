#Parker Behagg
#2/22/26 - 5/12/26
#FinalProject
# Create a game using the 'time' and 'random' modules and use loops and functions (include a main() function to run the program).

#----import python modules
import math as mt
import random as rdm
import time as tm
import tkinter as tk
#----import internal modules
import misc_utils as misc
import ui
import events as ev
import tasks as tsk
import alerts as als
import audio_utils as au
import pseudo_terminal as pt
import loop



#----Main function
def main(display_scale):
    #----initialize variables
    #mutable variables are stored within a dictionary for a more easy way to transfer between threads using dict_vars["variable name"] to get the variable rather than passing through all the variables through the loop.begin_loop(...) function
    #days = 0
    #current_cycle = 0
    #structural_integrity = 1000
    #life_support_system_integrity = 1000
    #temperature_C = 0
    #temperature_F = 32
    dict_vars = {"days":0, "current_cycle":0, "structural_integrity":0, "life_support_system_integrity":0, "temperature_C":0, "temperature_F":0}

    dict_vars["days"] = rdm.randrange(30,55,1)
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
    ui.create_main_ui("main window", display_scale, True, ls_root)
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

    ui.add_frame("sidebar", ls_root[2], 1, 1, dict_frames, "left", "None", "grey", "y")
    ui.add_label("sidebar title", dict_frames["sidebar"], 20, 20, "sidebar!",  dict_labels, "none", "None", "light grey")
    ui.add_label("Day counter", dict_frames["sidebar"], 20, 20, "", dict_labels, "none", "none", "light grey" )

    ui.add_frame("main frame", ls_root[2], 1, 1, dict_frames, "left", "none", "grey", "both")
    ui.add_label("game window label", dict_frames["main frame"], 20, 20, f"------------------", dict_labels, "None", "None", "grey")
    ui.add_button("terminal", dict_frames["main frame"], 20, 20, lambda: pt.show(ls_root, ls_terminal), dict_buttons)
    
    #ui.add_label("cycle length")
    #au.play_audio("MainMenu.wav")

    #TO DO: 
    #add top/botton alignment logic
    #make an audio thread / play audio during cycles and have the cycle end when the music ends for variable cycle lengths
    #add day cycle using time and random modules
    #add a day counter and cycle tracker (time untill next cycle/day and how many cycles have passed)
    
    #run
    loop.begin_day_loop(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars) #manages the day cycle using the time and random modules and various loops and conditional branches
    loop.begin_loop(ls_threads, ls_root, ls_terminal, dict_buttons, dict_entries, dict_frames, dict_labels, dict_sliders, dict_vars)#manages most behaviors, most of which are conditional if or elif or else statements, maybe some switch cases and various loops
    ui.run(ls_root[0]) #THIS GOES AT THE END OF THE MAIN FUNCTION, ALL CODE AFTER IT WILL NOT RUN UNTILL THE WINDOWS HAVE EITHER BEEN CLOSED NY THE USER OR DESTROYRD VIA '<object name>.Destroy()'


def prompt(display_scale, scale):
    #prompt for display scale
    prompt = tk.Tk()
    prompt.geometry("400x300")
    label = tk.Label(prompt, text="Please enter your display scale (default: 1920x1080) fomat: WIDTHxHEIGHT")
    label.pack()
    entry = tk.Entry(prompt)
    entry.pack()
    enter = tk.Button(prompt, text="Submit", command=lambda: entry_text(scale, prompt, entry))
    enter.pack(pady=10)
    prompt.mainloop()
    display_scale = scale
    return display_scale
def entry_text(scale , prompt, entryobj):
        entryval = entryobj.get()
        print(entryval, scale)
        scale = entryval
        prompt.destroy()


#run game
main()