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

def print_at(r, c, s):
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))

    c = s.encode("cp866")
    windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)
# ========================================================================

# Хранит весь чат
ch='conecting\n'
# Хранит то что ввел пользователь
sender=''
# Хранит английский алфавит
alphavit = [chr(i) for i in range(97, 123)]

# Создание сокета и подключения к серверу
sock = socket.socket()
sock.connect(('192.168.1.61', 9090))

# Создание функции для вывода чата
def out_chat():
    global ch
    global sender
    global alphavit
    global sock

    # Создание цикла
    while True:
        # Вывод чата в координатах 0,0
        print_at(0,0,ch)
        # Вывод то что ввел пользователь в координатах 20,0
        print_at(20,0,os.getlogin()+'> '+sender)
        # print(os.getlogin())

        # Используется попытка, чтобы при нажатии пользователем другой клавиши, кроме данной, ошибка не отображалась
        try:
            # Если пользователь нажал enter то 
            if keyboard.is_pressed('enter'):
                # Отправляем на сервер сообщение
                send_server(os.getlogin() + ": " + sender+"\n")
                # Очищаем то что ввел пользователь
                sender=''
                # Очищаем консоль
                os.system('cls')
                # Задержка
                time.sleep(0.1)
            # Если пользователь нажал backspace то
            if keyboard.is_pressed('backspace'):
                # Удаляем последний символ
                sender=sender[:-1]
                os.system('cls')
                time.sleep(0.1)
            if keyboard.is_pressed("space"):  # если нажата клавиша «q»
                sender+=" "
                os.system('cls')
                time.sleep(0.1)
            if keyboard.is_pressed(":"):  # если нажата клавиша «q»
                sender+=":"
                os.system('cls')
                time.sleep(0.1)
            # Если пользователь нажал на букву из алфавита то она вставится в sender
            for bukva in alphavit:
                if keyboard.is_pressed(bukva):  # если нажата клавиша «q»
                    sender+=bukva
                    os.system('cls')
                    time.sleep(0.1)
        except:
            break  # если пользователь нажал клавишу, отличную от данной, цикл прервется

# Получения сообщения от сервера
def recv_server():
    global ch
    global sock

# Бесконечный цикл
    while True:
        # Получаем данные с сервера и добавляем в ch
        ch= sock.recv(1024).decode()
        sock.send("-".encode())
        time.sleep(0.1)
        os.system('cls')

# Отправка сервера сообщения
def send_server(msg):
    global sock

    # while True:
    sock.send(msg.encode())
    # time.sleep(1)
    os.system('cls')

# Отправка сервера сообщения
def send_server2():
    global sock

    # while True:
    #     sock.send("-".encode())
    #     time.sleep(1)

# Потоки
t1 = threading.Thread(target=out_chat)
t2 = threading.Thread(target=recv_server)
t3 = threading.Thread(target=send_server2)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()    
t3.join()    
