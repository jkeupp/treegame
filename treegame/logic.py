import pygame


class logic(object):
    def __init__(self):
        self.state = 'initialized'
        return

    def init_game(self):
        self.default_settings()
        return


    def default_settings(self):
        self.nrounds=3
        return