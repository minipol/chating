import socket #Для работы с сетью
import threading #Для работы с потоками
import select #Для: ?

#Создается сокет и записывается в переменную
sock = socket.socket()
#"Создание сервера" и настройка
sock.bind(('192.168.1.61', 9090))
#Запускаем сервер на прослушивание порта
sock.listen()

#Храним подключение пользователей (клиентов)
arr_conn=[]
#Счетчик подключенных пользователей
index=0

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
    while True:
        message=''
        for i in range(len(arr_conn)):
            timeout=10
            ready_socket,_,_=select.select([arr_conn[i][0]],[],[],None)
            if ready_socket:
                if arr_conn[i][0].fileno():
                    try:
                        message+=arr_conn[i][0].recv(1024).decode()
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

t1.start()
t2.start()

t1.join()
t2.join()     
# conn.close()