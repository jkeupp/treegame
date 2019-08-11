import pygame


class logic(object):
    def __init__(self,nplayers=2):
        self.nplayers  = nplayers
        return

    def init_game(self):
        self.default_settings()
        return


    def default_settings(self):
        self.nrounds=3
        self.