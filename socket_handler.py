from socket import socket
from settings import *
from fsm import *
class Handler:
    def __init__(self,con:socket):
        self.con = con
        self.con.setblocking(False)
        self.buffer = ""
        self.todo_cmds = []
        self.commands = {"analyze":self.handle_analyze,"step":self.handle_step}
        self.active = True
    def handle(self):
        if self.todo_cmds:
            command = self.todo_cmds.pop(0)
            ls = command.split("\t")
            if ls[0] in self.commands:
                self.commands[ls[0]](*ls[1:])
    def update_command(self):
        try:
            data = self.con.recv(BUFSIZE)
        except BlockingIOError:
            return
        if data:
            self.buffer += data.decode(ENCODING)
            self.todo_cmds += self.buffer.split("\n")[:-1]
            self.buffer = self.buffer.split("\n")[-1]
        else:
            self.close_con()
    def handle_analyze(self,mapstr,cnt_2,cnt_3,cnt_5):
        _map = eval(mapstr)
        cnt_2 = eval(cnt_2)
        cnt_3 = eval(cnt_3)
        cnt_5 = eval(cnt_5)
        self.con.sendall(str(analyze(_map,cnt_2,cnt_3,cnt_5)).encode(ENCODING) + b"\n")
    def handle_step(self,mapstr,cnt_2,cnt_3,cnt_5):
        _map = eval(mapstr)
        cnt_2 = eval(cnt_2)
        cnt_3 = eval(cnt_3)
        cnt_5 = eval(cnt_5)
        self.con.sendall(str(next_step(_map,cnt_2,cnt_3,cnt_5)).encode(ENCODING) + b"\n")
    def close_con(self):
        self.con.close()
        self.active = False