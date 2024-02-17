import socket
import threading


sock = socket.socket()
sock.bind(('127.0.0.1', 9090))
sock.listen(1)

arr_conn=[]
arr_addr=[]
index=0

def acept_klient():
    while True:
        arr_conn[index], arr_addr[index] = sock.accept()
        print ('connected:',arr_addr[index])
        index+=1

def send_klient():
    while True:
        for i in range(index):
            data = arr_conn.recv(1024)
            if not data:
                break
            conn.send(data.upper())

# conn.close()