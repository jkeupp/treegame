import pygame
import time
import os
from . import board
from .lib import Player, Tree
from . import context
from . import logic
from . import console
from . import settings
from . import network
from pathlib import Path

class treegame(object):
    def __init__(self,nplayers=2,network=False,gamelength='default',imgpath = 'default'):
        """ Initializes the Treegame
        
        Args:
            nplayers (int, optional): Number of players. Defaults to 2.
            network (bool, optional): if True, game is run as a network game. Defaults to False.
            gamelength (str, optional): macro for different game length settings. Defaults to 'default'.
                                        'default': three epochs,
                                        'long': four epochs
            imgpath (str, optional): [description]. Defaults to 'default'.
        """     
        assert gamelength in ['long','default']
        self.gamelength = gamelength
        self.nplayers = nplayers
        self.init_players()
        self.starting_player = 0
        self.current_player =self.players[self.starting_player]
        self.time_zero = time.time()
        self.settings = settings
        self.network = network
        if imgpath == 'default':
            import inspect
            self.imgpath = Path(Path(inspect.getfile(self.__class__)).as_posix().rsplit('/',2)[0]) / 'images'     ##retrieve from where we are now
        else:
            self.imgpath = imgpath
        return

    def init_players(self):
        self.players = {}
        for i in range(self.nplayers):
            self.players[i] = Player(self,'player_'+str(i),i)

    def startup(self):
        # initialize board
        pygame.init()
        self.console = console.console(self)
        self.context = context.context()
        self.console('context initialized',toscreen=False)
        self.board = board.board(self)
        self.gui = board.GUI(self)
        self.logic = logic.logic(self)
        self.clock = pygame.time.Clock()
        self.console('game initialized')

    def connect(self,hostname,port):
        from .network import Client
        self.server_hostname = hostname
        self.server_port = port
        self.client = Client(self,hostname,port)
        self.client.connect()
        self.client.wait_start()

    def loop(self):
        ### pygame main loop
        self.running = True
        while self.running:
            self.clock.tick(30)
            self.interpret_events()
            self.gui.draw()
            self.gui.render()
            if self.network is True:
                self.client.listen()

    def interpret_events(self):
        events = pygame.event.get()
        for i,event in enumerate(events):
            #print(event)
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.type == pygame.MOUSEBUTTONDOWN and len(self.context.onMouseDown) != 0:
                #print(event,events)
                #skip=False
                #for e in events[i:]:
                #    if e.type == pygame.MOUSEBUTTONUP: 
                #        skip = True; 
                #if skip is True: continue
                for callback in self.context.onMouseDown.values():
                    callback(event,self)
            elif event.type == pygame.MOUSEMOTION and len(self.context.onMouseMove) != 0:
                #print(event,events)
                for callback in self.context.onMouseMove.values():
                    callback(event,self)
            elif event.type == pygame.MOUSEBUTTONUP and len(self.context.onMouseUp) != 0:
                #print(event,events)
                for callback in self.context.onMouseUp.values():
                    callback(event,self)
            self.context.clean_context()

                    
