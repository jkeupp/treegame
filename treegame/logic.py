import pygame
import hexy
import numpy
import itertools
from . import settings

class logic(object):
    def __init__(self,main):
        self.main = main
        self.initialize()
        return

    def initialize(self):
        self.round = 0
        self.tick = 0 
        self.startup_rounds=True
        self.nstartup_rounds = 0
        self.sunpos = 150 # that is position zero
        self.trees_planted_at_this_round = []
        return

    def check_valid_tree_pos(self,pos,tree):
        # return true or false, drop reason to console if false
        #rules that apply:

        # in startup round: only trees of size 1 can be plated at the edge of the field
        if self.startup_rounds is True:
            if tree.size != 1:
                self.main.console('smalltrees only in init phase')
                return False
            if self.main.board.field.get_tile_occupation(pos) is not None:
                self.main.console('field occupied! choose an empty one')
                return False           
            if int(hexy.get_cube_distance((0,0,0),pos)) == 3:
                return True
            self.main.console('put trees at edges in init')
            return False

        if tuple(pos) in self.trees_planted_at_this_round:
            self.main.console('only one move per tile per round!')
            return False

        if tree.size == 0: #seedling:
            # field must be emmpty
            if self.main.board.field.get_tile_occupation(pos) is not None:
                self.main.console('field occupied! choose an empty one')
                return False
            # ckeck if distance from center is == 3
            #if int(hexy.get_cube_distance((0,0,0),pos)) == 3:
            #    return True
            # seedlings can be put anywhere at r=3
            # seedlings can be put tree.size tiles away from a tree
            for ptree in itertools.chain(*self.main.current_player.board.values()): # that is the trees the player has on the board
                if int(hexy.get_cube_distance(ptree.position,pos) <= ptree.size):
                    return True
            self.main.console('plant seeds: at edge, next to tree')
            return False
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
            if self.startup_rounds is True:
                if self.nstartup_rounds == 1:
                    self.startup_rounds = False
                    self.let_the_sun_shine()
                else:
                    self.nstartup_rounds += 1
            else:
                self.cycle_round()
                self.let_the_sun_shine()
        else:
            self.main.current_player = self.main.players[(self.main.current_player.idx+1)% self.main.nplayers]
        self.trees_planted_at_this_round = []
        return

    def cycle_round(self):
        if self.tick == 5:
            self.tick=0
            self.round += 1
        else:
            self.tick += 1
        self.check_endgame()
        self.sunpos = (self.sunpos + 60) % 360
        return

    def check_endgame(self):
        term = self.main.settings.gamelength[self.main.gamelength]
        if (self.round >= term[0]) and  (self.tick == term[1]):
            # the end has come. 
            self.apply_endgame()
        return

    def apply_endgame(self):
        self.main.console('the end has come!')
        for i in range(self.main.nplayers):
            pi = self.main.players[i]
        # add one point per three sunpoints
        # print points for each player
        maxpoints, bestplayer = 0,''
        for i in range(self.main.nplayers):
            pi = self.main.players[i]
            pi.points += settings.endgame_sunpoints2points(pi.sunpoints)
            self.main.console(' %s got %3d points' % (pi.name,pi.points))
            if pi.points >= maxpoints:
                bestplayer = pi.name
                maxpoints = pi.points
        self.main.console('%s won !!! yay !!!' % (bestplayer,))

    def let_the_sun_shine(self):
        # get the rays as coordinates
        # hx.get_hex_line
        rays = settings.rays[self.sunpos]
        f = self.main.board.field
        money_earned = [0 for x in self.main.players]
        for i,ray in enumerate(rays):
            shadow = [0,0]
            for j, tile in enumerate(ray):
                tree = f.get_tile_occupation(tile)
                shadow[0] = numpy.max(shadow[0]-1,0)
                if shadow[0] == 0: shadow[1] = 0
                if tree is None: continue
                if tree.size > shadow[1]:
                    money_earned[tree.owner.idx] += tree.size
                    shadow = [tree.size+1,tree.size]
                if shadow[0]==1:
                    shadow = [tree.size+1,tree.size]
        for ip,p in self.main.players.items(): 
            self.main.console('player %d earned %d' % (p.idx,money_earned[p.idx]))
            p.sunpoints += money_earned[p.idx]
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