import os
import socket
import time
import numpy; np=numpy

class Server(object):
    def __init__(self,nplayers=2):
        self.port = 16666
        self.host = socket.gethostname()
        self.sockets = {}
        self.players = {}
        self.connected_address = {}
        self.nplayers = nplayers
        self.messages = {}
        return

    def recv_blocks(self, end_of_block='$',mxlen=8192):
        # taken from https://www.python-forum.de/viewtopic.php?t=38665
        for k in self.sockets.keys():
            socket = self.sockets[k]
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
                    self.messages[k] = messages
                    continue 
                parts = data.split(end_of_block)
                messages.append(parts[0])
                if len(parts) > 1:
                    # end_of_block found
                    for total in parts[1:-1]:
                        messages.append(total)
            self.messages[k] = messages
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

    def loop(self):
        #main loop to send and recieve 
        self.done=False
        while not self.done:
            self.recv_blocks() # adds messages to self.messages dictionary
            for kmessage in self.messages.keys():
                for msg in self.messages[kmessage]:
                    for ksocket in self.sockets.keys():
                        if ksocket == kmessage: continue # don't send back to the origin of the message
                        self.send(msg,to=ksocket)
                self.messages[kmessage] = [] # empty buffer

    def init_network_game(self):
        for i in self.sockets.keys():
            self.messages[i] = []
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
            if self.message[0] =='game starts' != 0:
                print('starting ... ')
                self.message.pop(0)
                start = True
                self.wait_game_info()
            else:
                self.message.pop(0)
            time.sleep(1)

    def send(self,message,marker='$'):
        self.socket.send((message+'$').encode())
        return

    def interpret(self,txt):
        print(txt)
        if len(txt) > 1:
            print('len != 1')
            for x in txt:
                self.interpret([x])
        elif len(txt) == 1:
            txt = txt[0]
            # all the different messages are interpreted here!

            # recieve own network playerid
            if txt.count('you are player') != 0:
                self.main.network_playerid=int(txt.split()[-1])
                return True
            elif txt.count(' bought tree' ) != 0:
                treetype = int(txt.split(' bought tree')[-1].strip())
                self.main.board.buy_tree(treetype)
                pass
            elif txt.count(' upgraded tree' ) != 0:
                pos = tuple([int(x) for x in txt.split('upgraded tree')[-1].split(' ')[-1].split('_')])
                treetype = int(txt.split('upgraded tree')[-1].split(' ')[0].strip())
                # get tree instance
                tree = self.main.current_player.available[treetype][0]
                self.main.board.add_tree(numpy.array(pos,dtype='int'),tree)
                pass
            elif txt.count(' placed tree' ) != 0:
                pos = tuple([int(x) for x in txt.split('placed tree')[-1].split(' ')[-1].split('_')])
                treetype = int(txt.split('placed tree')[-1].strip().split(' ')[0].strip())
                # get tree instance
                tree = self.main.current_player.available[treetype][0]
                self.main.board.add_tree(numpy.array(pos,dtype='int'),tree)
                pass
            elif txt.count(' sold tree' ) != 0:
                # Needs to be checked if any of that works!
                pos = tuple([int(x) for x in txt.split('sold tree')[-1].split(' ')[-1].split('_')])
                tree = self.main.board.field.get_tile_occupation(numpy.array(pos,dtype='int'))
                self.main.board.chop_tree(numpy.array(pos,dtype='int'),tree)
                pass
            elif txt.count(' is done' ) != 0:
                self.main.logic.cycle_players()
                pass
            else:
                print(txt, 'not understood!')
                
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

    def listen(self):
        # this function is meant to be called during main game to recieve 
        # all the data from the server
        self.message = self.recv_blocks()
        if len(self.message)  == 0:
            return
        self.interpret(self.message)
        self.message = []

class Lobby(object):
    def __init__(self):
        # maybe at some point ... 
        return

