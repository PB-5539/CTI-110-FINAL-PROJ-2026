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
import pseudo_terminal as pt

#----initialize variables

#create dictionaries and lists
ls_root = [] #0=root 1=settings menu 2=start menu 3=psedo-terminal
ls_terminal = [] #0=pseudo-terminal

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
    
    ui.add_button("play", ls_root[0], 20, 20, None, dict_buttons)
    ui.add_button("settings", ls_root[0], 20, 20, None, dict_buttons)
    ui.add_button("quit", ls_root[0], 20, 120, None, dict_buttons)

    #debug printing
    print(dict_buttons, ls_root, ls_terminal)

    #run
    ui.run(ls_root[0]) #THIS GOES AT THE END OF THE MAIN FUNCTION, ALL CODE AFTER IT WILL NOT RUN UNTILL THE WINDOWS HAVE EITHER BEEN CLOSED NY THE USER OR DESTROYRD VIA '<object name>.Destroy()'
    print("it seems the windows have been closed!")
#run game
main()