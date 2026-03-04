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

#----initialize variables

#create dictionaries
dict_buttons = {}
dict_sliders = {}
dict_labels = {}
dict_entries = {}
dict_frames = {}

#----Main function
def main():
    print("game now loading...")
    ui.create_main_ui("main window", "300x400", True)


#run game
main()

