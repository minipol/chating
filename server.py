import socket #Для работы с сетью
import threading #Для работы с потоками
import select #Для: ?
import time

print('введите ip: ')
ip_input = input()

sock = socket.socket()              #Создается сокет и записывается в переменную
sock.bind((ip_input, 9090))         #"Создание сервера" и настройка
sock.listen()                       #Запускаем сервер на прослушивание порта

arr_conn = []   #Храним подключение пользователей (клиентов)
index = 0       #Счетчик подключенных пользователей
message = ''    #Создание пустой строки для сообщения ввода

def recv_clients():
    global sock
    global arr_conn
    global index
    global message
    
    # while True:
    #     for i in range(len(arr_conn)):
    #         timeout=10
    #         ready_socket,_,_=select.select([arr_conn[i][0]],[],[],None)
    #         if ready_socket:
    #             if arr_conn[i][0].fileno():
    #                 try:
    #                     message+=arr_conn[i][0].recv(1024).decode()
    #                     if message[len(message) - 1] == "-":
    #                         message=message[:-1]
    #                     time.sleep(1)
    #                 except Exception:
    #                     print(arr_conn[i][0])
    #                     print("offline")
    #                     arr_conn.pop(0)
    #                     index-=1
    #             else:
    #                 print('bim')
    #         else:
    #             print('bam')

#Для того чтобы принимать подключение других пользователей
def acept_klient():
    global sock
    global arr_conn
    global index

    #Для подключение многих пользователей 
    while True:
        #Добавление подключенного пользователя, подключение пользователя
        arr_conn.append(sock.accept())
        #Выводим в консоль подключеного пользователей
        print ('connected:',arr_conn[index][1])
        #Обновление счетчика
        index+=1

def send_klients():
    global sock
    global arr_conn
    global index
    global message

    while True:
        for i in range(len(arr_conn)):
            timeout=10
            ready_socket,_,_=select.select([arr_conn[i][0]],[],[],None)
            if ready_socket:
                if arr_conn[i][0].fileno():
                    try:
                        message += arr_conn[i][0].recv(1024).decode().replace('-', '')
                        # if tttt.find('-')==-1:
                        #     message+=tttt
                        # time.sleep(1)
                    except Exception:
                        print(arr_conn[i][0])
                        print("offline")
                        arr_conn.pop(0)
                        index-=1
                else:
                    print('bim')
            else:
                print('bam')
        for i in arr_conn:
            i[0].send(message.encode())

t1 = threading.Thread(target=acept_klient)
t2 = threading.Thread(target=send_klients)
t3 = threading.Thread(target=recv_clients)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()     
t3.join()     
# conn.close()
