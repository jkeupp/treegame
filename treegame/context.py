import pygame; pg = pygame


class context(object):
    def __init__(self):
        self.onMouseDown = {}
        self.onMouseUp = {}
        self.onMouseMove = {}
        self.tobecleaned = []
        return

    def clear_context(self):
        self.onMouseDown = {}
        self.onMouseUp = {}
        self.onMouseMove = {}
        return

    def clean_context(self):
        for i,tbc in enumerate(self.tobecleaned):
            del tbc[0][tbc[1]]
        self.tobecleaned = []