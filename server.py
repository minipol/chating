#импорт билиотек
import socket 
import threading 
import select 
import time

print('введите ip: ')
ip_input = input()

sock = socket.socket()      #Создается сокет и записывается в переменную
sock.bind((ip_input, 9090)) #"Создание сервера" и настройка
sock.listen()               #Запускаем сервер на прослушивание порта

arr_conn = []   #Храним подключение пользователей (клиентов)
index = 0       #Счетчик подключенных пользователей
message = ''    #Создание пустой строки для сообщения ввода

def recv_clients():
    global sock
    global arr_conn
    global index
    global message

def acept_klient(): #Для того чтобы принимать подключение других пользователей
    global sock
    global arr_conn
    global index

    while True: #Для подключение многих пользователей 
        arr_conn.append(sock.accept())          #Добавление подключенного пользователя, подключение пользователя
        print ('connected:',arr_conn[index][1]) #Выводим в консоль подключеного пользователей
        index+=1        #Обновление счетчика

def send_klients(): #Создание функции получения и отправки всем пользователям
    global sock
    global arr_conn
    global index
    global message

    while True: #Создание бесконечноого цикла
        for i in range(len(arr_conn)):  #Создание цикла для пробегания по соединениям
            timeout=10
            ready_socket,_,_=select.select([arr_conn[i][0]],[],[],None) #Для проверки отправил ли соединения сообщения
            if ready_socket:
                if arr_conn[i][0].fileno(): #Проверка что соединение существует
                    try:
                        message += arr_conn[i][0].recv(1024).decode().replace('-', '')  #Получение и сохранение сообщения от соединении
                    except Exception:   #В случае ошибки убираем соединение, пишем в консоль что отключился и уменьшаем количество подключенных на 1
                        print(arr_conn[i][0])
                        print("offline")
                        arr_conn.pop(0)
                        index-=1
                else:
                    print('bim')
            else:
                print('bam')
        for i in arr_conn:  #Всем рассылаем сообщение
            i[0].send(message.encode())

#Запускаем в потоки для функции
t1 = threading.Thread(target=acept_klient)
t2 = threading.Thread(target=send_klients)
t3 = threading.Thread(target=recv_clients)

# Запуск
t1.start()
t2.start()
t3.start()

#Соединение потоков
t1.join()
t2.join()     
t3.join()     
