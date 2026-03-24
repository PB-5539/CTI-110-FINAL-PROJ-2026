import random as rdm
import math as mt
import time as tm
import wave
import contextlib
import os

def get_duration(filename):
    fname = r'finalproject/audio/wav/'+filename
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        print(f"Duration: {duration:.2f} seconds")
        return duration

