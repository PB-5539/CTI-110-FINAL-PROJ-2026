import tkinter as tk
from tkinter import ttk
import events as ev
import tasks as tsk
import alerts as als
import misc_utils as msc

def create_main_ui(name, geometry):
    print(f"creating Ui element named: {name} with geometry: {geometry}")

def add_button(name, parent, xpad, ypad, acton):
    print(f"creating Button Widget named: {name} name with parent: {parent} pad x: {xpad} pad y: {ypad} and action: {acton}")