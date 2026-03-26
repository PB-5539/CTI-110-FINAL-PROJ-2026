import math as mt
import time as tm
import random as rd

#i would eventually like to add this as something you can play in the terminal of the main game lol


def main(dict_player_info):
    ls_items = ["ominous horn", "shattered orb", "mysterious potion", "necromancer staff", "red orb", "glowing scroll", ]
    attempts = 0
    player_stats = {"name":dict_player_info["name"],"gold":0, "health":10, "arcane_dust":0}
    dict_encounters = {"elf":["dialogue", "dialogue", "+8 gold"], "placeholder":["dialogue list...", "...", "reward"]}

    while (player_stats["health"] > 0) and (player_stats["gold"] >=0 ):
        player_stats["gold"] = player_stats["gold"] - 1 #THIS IS A PLACEHOLDER FOR THE GAME LOGIC
    #on death/bankrupcy logic goes here
    if (player_stats["gold"] < 0) and (player_stats["health"] > 0):
        print()
        print()
        print("=====================")
        print("  you went bankrupt! ")
        print("=====================")
    elif player_stats["health"] > 1:
        print()
        print()
        print("=====================")
        print("       you Died      ")
        print("=====================")
    print(overview(player_stats))





















def intro():
    dict_player_info = {"name":"", }#idk what other choices to add
    ls_intro = []
    for i in range(len(ls_intro)):
        print(ls_intro[i])
        tm.sleep(2)
    for i in range(100):    #clears the area a bit
        print()
    print("====================================================================")
    print("                             Welcome                                ")
    print("====================================================================")
    tm.sleep(2)
    print()
    print("---\This is your status bar/---")
    tm.sleep(0.5)
    print("         |===========|")
    tm.sleep(0.5)
    print("         |health:  10|")
    tm.sleep(0.5)
    print("         |gold:    0 |")
    tm.sleep(0.5)
    print("         |Dust:    0 |")
    tm.sleep(0.5)
    print("         |===========|")
    tm.sleep(2)
    print("---\open it at any time by/---")
    print("-/typing 'stat' in an input\-")
    tm.sleep(2)
    print("====================================================================")
    print()
    print("====================================================================")
    print()
    print("To start, What's your name?")
    tm.sleep(1)
    dict_player_info["name"] = str(input("Name:"))


    return dict_player_info


def encounter(ls_dialogue):
    for i in range(len(ls_dialogue)):
        print(ls_dialogue[i])
        tm.sleep(2)

def overview(player_stats):
    gold = player_stats["gold"]
    health = player_stats["health"]
    name = player_stats["name"]
    overview = f"====overview====\n{'Name:':<12}{name}\n{'Gold:':<12}{gold:<12}\n{'Health:':<12}{health:<12}\n"
    return overview

main(intro())