#----import python modules
import math as mt
import random as rdm
import time as tm
import threading as th
import tkinter as tk

#----import internal modules
import misc_utils as misc
import ui
import events as ev
import tasks as tsk
import alerts as als
import pseudo_terminal as pt

def loop(ls_root):
    while True:
        print(ls_root)

def begin_loop(ls_threads, ls_root):
    thread = th.Thread(target=lambda: loop(ls_root),  daemon=True)
    thread.start()
    ls_threads.append(thread)
    return thread