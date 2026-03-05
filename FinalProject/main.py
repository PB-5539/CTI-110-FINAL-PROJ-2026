#Parker Behagg
#
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

#create dictionaries
ls_root = []
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
    ui.add_button("play", ls_root[2], 20, 20, None, dict_buttons)
    print(dict_buttons)
    
    pt.start_terminal()

    #run
    ui.run(ls_root[0])
#run game
main()

