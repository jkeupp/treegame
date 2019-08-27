import os
import socket
import time

def recv_blocksx(socket, end_of_block='$',mxlen=8192):
    # taken from https://www.python-forum.de/viewtopic.php?t=38665
    total = ''
    data = socket.recv(mxlen).decode()
    while True:
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

def recv_blocks(socket, end_of_block='$',mxlen=8192):
    # taken from https://www.python-forum.de/viewtopic.php?t=38665
    total = ''
    messages = []
    done=False
    while not done:
        try:
            data = socket.recv(mxlen).decode()
        except:
            data = None
        if not data:
            done=True
            return messages
        print(data)
        parts = data.split(end_of_block)
        messages.append(parts[0])
        if len(parts) > 1:
            # end_of_block found
            for total in parts[1:-1]:
                messages.append(total)
    return []

class Server(object):
    def __init__(self,nplayers=2):
        self.port = 16666
        self.host = socket.gethostname()
        self.sockets = {}
        self.players = {}
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
                self.init_network_game()
                break
            else:
                for sock in self.sockets.values():
                    sock.send(('waiting for %d more player(s)$' % (self.nplayers-i)).encode())
        return

    def init_network_game(self):
        for i in self.sockets.keys():
            self.send('you are player %d' % (i),to=i)

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
    def __init__(self,maininstance,hostname,port):
        self.main = maininstance
        self.port = port
        self.hostname = hostname
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message = []
        return

    def connect(self):
        self.socket.connect((self.hostname,self.port))
        self.socket.setblocking(False)
        return

    def recv_blocks(self, end_of_block='$',mxlen=8192):
        # taken from https://www.python-forum.de/viewtopic.php?t=38665
        total = ''
        if len(self.message) != 0:
            return self.message
        socket = self.socket
        messages = []
        done=False
        while not done:
            try:
                data = socket.recv(mxlen).decode()
            except:
                data = None
            if not data:
                done=True
                return messages
            print(data)
            parts = data.split(end_of_block)
            messages.append(parts[0])
            if len(parts) > 1:
                # end_of_block found
                for total in parts[1:-1]:
                    messages.append(total)
        return []

    def wait_start(self):
        start = False
        while start is not True:
            self.message = self.recv_blocks()
            if len(self.message) == 0:
                time.sleep(0.05)
                continue
            print(10*'#')
            print(self.message)
            print(10*'#')
            if self.message[0] =='game starts' != 0:
                print('starting ... ')
                self.message.pop(0)
                start = True
                self.wait_game_info()
            else:
                self.message.pop(0)
            time.sleep(1)

    def interpret (self,txt):
        print(txt)
        if len(txt) > 1:
            print('len != 1')
            for x in txt:
                self.interpret([x])
        elif len(txt) == 1:
            txt = txt[0]
            if txt.count('you are player') != 0:
                self.main.network_playerid=int(txt.split()[-1])
                return True
        else:
            return False

    def wait_game_info(self):
        done=False
        while not done:
            self.message = self.recv_blocks()
            if len(self.message) == 0:
                time.sleep(0.05)
                continue
            else:
                print(self.message)
            success =  self.interpret(self.message)
            if success is True: done=True
        return

class Lobby(object):
    def __init__(self):
        # maybe at some point ... 
        return

