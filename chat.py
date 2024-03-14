import keyboard
import os
import time
from ctypes import *
import socket
import threading

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

ch='conecting\n'
sender=''
alphavit = [chr(i) for i in range(97, 123)]

sock = socket.socket()
sock.connect(('192.168.1.165', 9090))

def out_chat():
    global ch
    global sender
    global alphavit

    while True:  # making a loop
        print_at(0,0,ch)
        print_at(20,0,'>'+sender)
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('enter'):
                ch+=('\n'+sender)
                sender=''
                os.system('cls')
                time.sleep(0.1)
            if keyboard.is_pressed('backspace'):
                sender=sender[:-1]
                os.system('cls')
                time.sleep(0.1)
            for bukva in alphavit:
                if keyboard.is_pressed(bukva):  # if key 'q' is pressed
                    sender+=bukva
                    time.sleep(0.1)
        except:
            break  # if user pressed a key other than the given key the loop will break

def recv_server():
    global ch
    global sock

    while True:
        ch= sock.recv(1024).decode()
        time.sleep(1)
        os.system('cls')


def send_server():    
    global ch
    global sock

    while True:
        sock.send(ch.encode())
        time.sleep(1)
        os.system('cls')


t1 = threading.Thread(target=out_chat)
t2 = threading.Thread(target=recv_server)
t3 = threading.Thread(target=send_server)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()    
t3.join()    
