import random as rdm
import math

def send_alert(text, urgency, sound): #urgency will be on a 1-3 scale
    print(f"sending alert: [{text}] with urgency rating of: {urgency}/3 with sound condition: {sound}")