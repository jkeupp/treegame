import pygame as pg
import numpy as np
import hexy as hx



class Player(object):
    def __init__(self,name):
        # init variables
        self.sunpoints = 1 
        self.name = name
        self.trees = {}
        self.position = None
        self.init_trees()
    
    def init_trees(self):
        """ Initializes the players' Trees
        """
        #default settings hard coded
        # five seeds, one available, rest to be bought
        self.trees[0] = [Tree(0,0,status='available')]
        for i in range(4):
            self.trees[0].append(Tree(0,i+1,status='stack'))
        # eight lvl 1 trees, four available
        self.trees[1] = [Tree(1,0,status='available')]
        for i in range(3):
            self.trees[1].append(Tree(1,i+1,status='available'))
        for i in range(4):
            self.trees[1].append(Tree(1,i+4,status='stack'))
        # four lvl 2 trees, one available
        self.trees[2] = [Tree(2,0,status='available')]
        for i in range(3):
            self.trees[2].append(Tree(2,i+1,status='stack'))
        # two lvl 2 trees, none available
        self.trees[3] = [Tree(3,0,status='stack'),Tree(3,0,status='stack')]
        return
            
class Tree(object):
    def __init__(selfs,size,idx,status='stack'):
        self.size = size
        self.idx = idx
        self.set_status(status)

    def set_status(self,status):
        assert status in ['available','stack','board','graveyard']
        self.status = status

    def set_position(self,position):
        self.position = position

    def get_position(self,mode='cube'):
        assert mode in ['cube','cartesian']:
        if mode  == 'cube':
            return self.position
        elif mode == 'cartesian':
            # TBI, convert to cartesian coords and return
            return None
        