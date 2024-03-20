# импортируем библиотеки
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

def print_at(r,c):
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))
    windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)
# ========================================================================

# проверка устоновки соеденения с сервером
ch='conecting\n'
sender=''
alphavit = [chr(i) for i in range(97, 123)]

sock = socket.socket()
sock.connect(('192.168.1.188', 9090))

def out_chat():
    while True:  # создание цикла
        print_at(0,0,ch)
        print_at(20,0,'>'+sender)

        try:  # используется попытка, чтобы при нажатии пользователем другой клавиши, кроме данной, ошибка не отображалась
            if keyboard.is_pressed('enter'):
                # ch+=('\n'+sender)
                send_server(sender+"\n")
                sender=''
                os.system('cls')
                time.sleep(0.1)
            if keyboard.is_pressed('backspace'):
                sender=sender[:-1]
                os.system('cls')
                time.sleep(0.1)
            for bukva in alphavit:
                if keyboard.is_pressed(bukva):  # если нажата клавиша «q»
                    sender+=bukva
                    time.sleep(0.1)
        except:
            break  # если пользователь нажал клавишу, отличную от данной, цикл прервется

def recv_server():
    while True:
        ch+= sock.recv(1024).decode()
        time.sleep(1)
        os.system('cls')

def send_server(msg):    
    # while True:
    sock.send(msg.encode())
    time.sleep(1)
    os.system('cls')

t1 = threading.Thread(target=out_chat)
t2 = threading.Thread(target=recv_server)
# t3 = threading.Thread(target=send_server)

t1.start()
t2.start()
# t3.start()

t1.join()
t2.join()    
# t3.join()    
