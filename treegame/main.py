import pygame
from . import board
from .lib import Player, Tree



class treegame(object):
    def __init__(self,nplayers=1):
        self.nplayers = nplayers
        self.init_players()
        self.current_player = 1
        return

    def init_players(self):
        self.players = {}
        for i in range(self.nplayers):
            self.players[i] = Player('player_'+str(i))

    def startup(self):
        # initialize board
        pygame.init()
        self.board = board.board()
        self.GUI = board.GUI(self.board)
        #self.logic = logic.logic()
        self.clock = pygame.time.Clock()


    def loop(self):
        ### pygame main loop
        self.running = True
        while self.running:
            self.clock.tick(30)
            self.interpret_events()
            self.GUI.draw_board()
            self.GUI.draw_hud(player=self.current_player)
            self.GUI.render()

    def interpret_events(self):
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
