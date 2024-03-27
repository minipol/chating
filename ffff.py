import socket #Для работы с сетью
import threading #Для работы с потоками
import select #Для: ?

#Создается сокет и записывается в переменную
sock = socket.socket()
#"Создание сервера" и настройка
sock.bind(('192.168.1.14', 9090))
#Запускаем сервер на прослушивание
sock.listen()

#Храним подключение пользователей (клиентов)
arr_conn=[]
#Счетчик подключенных пользователей
index=0

#Для того чтобы принимать подключение других пользователей
def acept_klient():
    #Для подключение многих пользователей 
    while True:
        #Добавление подключенного пользователя, подключение пользователя
        arr_conn.append(sock.accept())
        #Выводим в консоль подключение пользователей
        print ('connected:',arr_conn[index][1])
        #Обновление счетчика
        index+=1

#Создание функции получения и отправки всем пользователям 
def send_klients():
    #Создание бесконечноого цикла
    while True:
        #Создание пустой строки для сообщения ввода
        message=''
        #Создание цикла для пробегания по соединениям
        for i in range(len(arr_conn)):
            #Для проверки отправил ли соединения сообщения
            # ready_socket,_,_=select.select([arr_conn[0][i]],[],[],None)
            #
            # if ready_socket:
                #Проверка что соединение существует
                if arr_conn[i][0].fileno():
                    try:
                        #Получение и сохранение сообщения от соединении
                        message+=arr_conn[i][0].recv(1024).decode()
                    #В случае ошибки убираем соединение, пишем в консоль что отключился и уменьшаем количество подключенных на 1
                    except Exception:
                        print(arr_conn[i][0])
                        print("offline")
                        arr_conn.pop(0)
                        index-=1
                else:
                    print('bim')
            # else:
            #     print('bam')
        # Всем рассылаем сообщение
        for i in arr_conn:
            i[0].send(message.encode())

# Запускаем в потоки для функции
t1 = threading.Thread(target=acept_klient)
t2 = threading.Thread(target=send_klients)

# Запуск
t1.start()
t2.start()

# Соединение потоков
t1.join()
t2.join()
