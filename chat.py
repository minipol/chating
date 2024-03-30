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

print('введите ip: ')
ip_input = input()
print('введите ник: ')
nicname = input()
os.system('cls')

ch='conecting\n'                            # Хранит весь чат
sender=''                                   # Хранит то что ввел пользователь
alphavit = [chr(i) for i in range(97, 123)] # Хранит английский алфавит

# Создание сокета и подключения к серверу
sock = socket.socket()
sock.connect((ip_input, 9090))
sock.send("-".encode())

def out_chat(): # Создание функции для вывода чата
    global ch
    global sender
    global alphavit
    global sock
    global nicname

    while True: # Создание цикла
        print_at(0,0,ch)                    # Вывод чата в координатах 0,0
        print_at(20,0,nicname+'> '+sender)  # Вывод то что ввел пользователь в координатах 20,0

        try:    # Используется попытка, чтобы при нажатии пользователем другой клавиши, кроме данной, ошибка не отображалась 
            if keyboard.is_pressed('enter'):    # Если пользователь нажал enter то
                send_server(nicname + ": " + sender+"\n")   # Отправляем на сервер сообщение
                sender=''                                   # Очищаем то что ввел пользователь
                os.system('cls')                            # Очищаем консоль
                time.sleep(0.1)                             # Задержка

            if keyboard.is_pressed('backspace'):    # Если пользователь нажал "backspace" то
                sender=sender[:-1]  # Удаляем последний символ
                os.system('cls')
                time.sleep(0.1)
            if keyboard.is_pressed("space"):  # если пользователь нажал "space" то
                sender+=" "
                os.system('cls')            #обновляем консоль
                time.sleep(0.1)
            if keyboard.is_pressed(":"):    #отбражение ":"
                sender+=":"
                os.system('cls')
                time.sleep(0.1)
            for bukva in alphavit:  # Если пользователь нажал на букву из алфавита то она вставится в "sender"
                if keyboard.is_pressed(bukva):  # отображеине нажатых букв
                    sender+=bukva
                    os.system('cls')
                    time.sleep(0.1)
        except:
            break  # если пользователь нажал клавишу, отличную от данной, цикл прервется

def recv_server():  # Получения сообщения от сервера
    global ch
    global sock

    while True: # Бесконечный цикл
        ch= sock.recv(1024).decode()     #Получаем данные с сервера и добавляем в ch
        sock.send("-".encode())
        time.sleep(0.1)
        os.system('cls')

def send_server(msg):   # Отправка сервера сообщения
    global sock
    sock.send(msg.encode())
    os.system('cls')

def send_server2():
    global sock

# Потоки
t1 = threading.Thread(target=out_chat)
t2 = threading.Thread(target=recv_server)
t3 = threading.Thread(target=send_server2)

# запуск
t1.start()
t2.start()
t3.start()

# соеденение
t1.join()
t2.join()    
t3.join()    
