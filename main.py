import socket
from settings import *
from socket_handler import Handler
from multiprocessing import Process
from time import sleep
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((HOST,PORT))
s.setblocking(False)
s.listen()
def domulpro(h:Handler):
    while h.active:
        h.update_command()
        h.handle()
        sleep(0.001)
while True:
    try:
        con,addr = s.accept()
    except BlockingIOError:
        sleep(0.001)
        continue
    print(addr,"connected.")
    Process(target=domulpro,args=[Handler(con)],daemon=True).start()
    s.listen()