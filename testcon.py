import socket
from settings import *
import time
s = socket.create_connection((HOST,PORT))
time0 = time.time()
for i in range(10000):
    print(f"{(i + 1)/100}%")
    s.sendall(b"analyze\t[[0,0,0,0,0],[0,6,0,0,0],[0,6,6,6,0],[0,0,7,0,0],[0,0,7,0,0]]\t3\t1\t1\n")
    ans = s.recv(BUFSIZE)
    while not ans.endswith(b"\n"):
        ans += s.recv(BUFSIZE)
    ans = eval(ans.strip(b"\n").decode(ENCODING))
print(time.time() - time0)