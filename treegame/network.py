import os
import socket
import time

def recv_blocks(socket, end_of_block='$',mxlen=8192):
    # taken from https://www.python-forum.de/viewtopic.php?t=38665
    total = ''
    while True:
        data = socket.recv(mxlen).decode()
        if not data:
            if total:
                raise ValueError("Partial Block", total)
            return
        parts = data.split(end_of_block)
        total += parts[0]
        if len(parts) > 1:
            # end_of_block found
            yield total
            for total in parts[1:-1]:
                yield total
            total = parts[-1]

class Server(object):
    def __init__(self,nplayers=2):
        self.port = 16666
        self.host = socket.gethostname()
        self.sockets = {}
        self.connected_address = {}
        self.nplayers = nplayers
        return

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host,self.port))
        #self.socket.setblocking(False)
        return

    def listen(self):
        self.socket.listen()
        i=0
        while True:
            time.sleep(1)
            sock,addr = self.socket.accept()
            sock.setblocking(False)
            self.sockets[i] = sock
            self.connected_address[i] = addr
            print(addr)
            i += 1
            if i == self.nplayers: # we have as many players as needed
                self.send('game starts')
                break
            else:
                for sock in self.sockets.values():
                    sock.send(('waiting for %d more player(s)$' % (self.nplayers-i)).encode())
        return

    def send(self,message,to=None,marker='$'):
        if to is None:
            for sock in self.sockets.values():
                sock.send((message+'$').encode())
        else:
            if to in self.sockets.keys():
                self.sockets[to].send((message+'$').encode())
            else:
                print('%s not in socket list!' % (to,)) 
        return
    
    def cleanup(self):
        self.socket.close()
        print ('socket closed')

class Client(object):
    def __init__(self,hostname,port):
        self.port = port
        self.hostname = hostname
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return

    def connect(self):
        self.socket.connect((self.hostname,self.port))
        return

    def wait_start(self):
        start = False
        while not start:
            x = recv_blocks(self.socket)
            #x = self.socket.recv(8192)
            print(10*'#')
            print(x)
            print(10*'#')
            for xx in x: print(xx)
            print(10*'#')
            if x == 'game starts':
                start = True
                continue
            time.sleep(1)
    
    def wait_game_info(self):
        return

class Lobby(object):
    def __init__(self):
        # maybe at some point ... 
        return

