import random
import time
import math

def main():
    print("main")

def choice():
    from_user = ""
    ls_1 = ["yes", "y", "1", "accept"]
    ls_2 = ["no", "n", "2", "decline"]
    while from_user not in [ls_1, ls_2]:
        from_user = input("Choice: ")
        from_user = from_user.lower()
        if from_user in ls_1:
            print("1")
        elif from_user in ls_2:
            print("2")
        elif from_user in ["stat", "stats", "status", "overview", "player stats"]:
            print("stat")
        else:
            print("invalid input, please try again")

while True:
    choice()