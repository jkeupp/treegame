import pygame
import hexy
import itertools
from . import settings

class logic(object):
    def __init__(self,main):
        self.main = main
        self.state = 'initialized'
        self.initialize()
        return

    def initialize(self):
        self.round = 0
        self.tick = 0 
        self.sunpos = 150 # that is position zero
        return

    def check_valid_tree_pos(self,pos,tree):
        # return true or false, drop reason to console if false
        #rules that apply:

        if tree.size == 0: #seedling:
            # field must be emmpty
            if self.main.board.field.get_tile_occupation(pos) is not None:
                self.main.console('field occupied! choose an empty one')
                return False
            # ckeck if distance from center is == 3
            if int(hexy.get_cube_distance((0,0,0),pos)) == 3:
                return True
            # seedlings can be put anywhere at r=3
            # seedlings can be put tree.size tiles away from a tree
            for ptree in itertools.chain(*self.main.current_player.board.values()): # that is the trees the player has on the board
                if int(hexy.get_cube_distance(ptree.position,pos) <= ptree.size):
                    return True
        occ = self.main.board.field.get_tile_occupation(pos) #  occ is a tree instance!
        # all other trees require an othertree.size of tree.size-1 --> empty field forbidden!
        if occ is None: 
            self.main.console('plant a seedling first!')
            return False
        if occ.owner != self.main.current_player: 
            self.main.console('that is not your tree!')
            return False
        if occ.size != tree.size -1: 
            self.main.console('trees have to grow incrementally!')
            return False
        # all eventualities were taken care for, the tree can be planted!
        return True

    def cycle_players(self):
        if (self.main.current_player.idx+1)%self.main.nplayers == self.main.starting_player:
            self.main.starting_player = (self.main.starting_player + 1) % self.main.nplayers
            self.main.current_player = self.main.players[self.main.starting_player]
            self.main.board.let_the_sun_shine()
        else:
            self.main.current_player = self.main.players[(self.main.current_player.idx+1)% self.main.nplayers]
        return

    def cycle_round(self):
        # tbi
        return

    def check_tree_buy(self,treetype):
        player = self.main.current_player
        trees_in_stack = player.n(treetype,'stack')
        if trees_in_stack <= 0:
            self.main.console('no more trees of %d in stack' % (treetype))
            return False
        cost = settings.tree_costs_fromstack[treetype][trees_in_stack]
        if cost > player.sunpoints:
            self.main.console('insufficient credits! %d<%d' % (player.sunpoints,cost))
            return False
        return True