import keyboard
import os
import time
from ctypes import *

# ================================= для изменения кординаты курсора в cmd
STD_OUTPUT_HANDLE = -11

class COORD(Structure):
    pass

COORD._fields_ = [("X", c_short), ("Y", c_short)]

def print_at(r, c, s):
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))

    c = s.encode("cp866")
    windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)
# ========================================================================

ch='asd\nzcv'
sender=''

while True:  # making a loop
    print_at(0,0,ch)
    print_at(20,0,'>'+sender)
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('q'):  # if key 'q' is pressed
            sender+='q'
            time.sleep(0.1)
            # print('You Pressed A Key!')
            # break  # finishing the loop
    except:
        break  # if user pressed a key other than the given key the loop will break