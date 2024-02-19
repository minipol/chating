import socket
import threading
import select


sock = socket.socket()
sock.bind(('127.0.0.1', 9090))
sock.listen(1)

arr_conn=[]
arr_addr=[]
index=0

def acept_klient():
    while True:
        arr_conn[index] = sock.accept()
        print ('connected:',arr_conn[index][1])
        index+=1

def send_klients():
    while True:
        message=''
        for i in range(len(arr_conn)):
            timeout=10
            ready_socket,_,_=select.select([arr_conn[i][0]],[],[],None)
            if ready_socket:
                if arr_conn[i][0].fileno():
                    try:
                        # aaaa=arr_conn[i][0].recv(1024).decode()
                        message=arr_conn[i][0].recv(1024).decode()
                    except Exception:
                        print(arr_conn[i][1]+'off')
                        arr_conn.pop(i)
                else:
                    print('')
            else:
                print('')
        for i in arr_conn:
            i[0].send(message.encode())

t1 = threading.Thread(target=acept_klient)
t2 = threading.Thread(target=send_klients)

t1.start()
t2.start()

t1.join()
t2.join()     
# conn.close()