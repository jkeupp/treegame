import pygame; pg= pygame
import numpy; np = numpy
import hexy as hx
from . import settings
from . import util
import pygame



class Player(object):
    def __init__(self,main,name,idx):
        # init variables
        self.main = main
        self.sunpoints = settings.num_sunpoints
        self.idx = idx
        self.name = name
        self.trees = {}
        self.position = None
        self.init_trees()

    def init_trees(self):
        """ Initializes the players' Trees
        """
        # get number of starting trees and total trees from settingms
        self.trees[0] =  [Tree(self,0,i,status='available') for i in range(settings.num_start_seedlings)]
        self.trees[0] += [Tree(self,0,i+1,status='stack')   for i in range(settings.num_start_seedlings, settings.num_seedlings)]
        self.trees[1] =  [Tree(self,1,i,status='available') for i in range(settings.num_start_smalltrees)]
        self.trees[1] += [Tree(self,1,i+1,status='stack')   for i in range(settings.num_start_smalltrees, settings.num_smalltrees)]
        self.trees[2] =  [Tree(self,2,i,status='available') for i in range(settings.num_start_mediumtrees)]
        self.trees[2] += [Tree(self,2,i+1,status='stack')   for i in range(settings.num_start_mediumtrees, settings.num_mediumtrees)]
        self.trees[3] =  [Tree(self,3,i,status='available') for i in range(settings.num_start_largetrees)]
        self.trees[3] += [Tree(self,3,i+1,status='stack')   for i in range(settings.num_start_largetrees, settings.num_largetrees)]
        return

    def n(self,treetype,statustype):
        c = 0
        for x in self.trees[treetype]:
            if x.status == statustype:
                c += 1
        return c

    @property
    def available(self):
        return {i:[x for x in self.trees[i] if x.status=='available'] for i in range(4)}

    @property
    def stack(self):
        return {i:[x for x in self.trees[i] if x.status=='stack'] for i in range(4)}
    
    @property
    def board(self):
        return {i:[x for x in self.trees[i] if x.status=='board'] for i in range(4)}

    @property
    def graveyard(self):
        return {i:[x for x in self.trees[i] if x.status=='graveyard'] for i in range(4)}
            
class Tree(object):
    def __init__(self,owner,size,idx,status='stack'):
        self.owner = owner
        self.main = owner.main
        self.size = size
        self.idx = idx
        self.set_status(status)
        self.position = None

    def set_status(self,status):
        assert status in ['available','stack','board','graveyard']
        self.status = status

    def set_position(self,position):
        self.position = position
    
    def add_to_board(self,position):
        self.set_position(position)
        self.set_status('board')
        self.main.board.field.tile_occupation[
            self.main.board.field.cube_indices[tuple(position)]] = self

    def get_position(self,mode='cube'):
        assert mode in ['cube','cartesian']
        if mode  == 'cube':
            return self.position
        elif mode == 'cartesian':
            return self.main.board.field.get_cartesian_point(self.position) + self.main.gui.woods_center 

    def draw(self):
        center = self.get_position(mode='cartesian')
        #center = numpy.random.uniform(400,400,(2,))
        #import pdb; pdb.set_trace()
        pos = util.get_lt_coords(self.main.gui.usertrees[self.size][self.owner.idx],center)
        self.main.gui.screen.blit(self.main.gui.usertrees[self.size][self.owner.idx],pos)
    
    def __gt__(self,other):
        return self.idx > other

    def __ge__(self,other):
        return self.idx >= other

class TreeSprite(pg.sprite.Sprite):
    def __init__(self,image,center):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=center)
        return 

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class DrawItem(pg.sprite.Sprite):
    def __init__(self,image,screen,**kwargs):
        super().__init__()
        self.image = image
        self.screen = screen
        self.kwargs = kwargs
        self.rect = self.image.get_rect()
        if 'pos' in kwargs.keys():
            self.pos = kwargs['pos']
        else:
            self.pos = image.rect.center
        return 

    def draw(self):
        self.screen.blit(self.image, self.rect.move(self.pos))

class Callback(object):
    def __init__(self, callback_fun, args=(), kwargs={}):
        self.callback_fun = callback_fun
        self.args = args
        self.kwargs = kwargs
        return

    def __call__(self,*args,**kwargs):
        #import pdb; pdb.set_trace()
        tmpargs = args + self.args # get rid of self in args!
        self.kwargs.update(kwargs)
        #print(30*'#')
        #print(tmpargs)
        #print(30*'#')
        #print(self.kwargs)
        #print(30*'#')
        return self.callback_fun(*tmpargs,**self.kwargs)


def draw_on_move(event,main,item=None,pos=None):
    if pos is None:
        pos = event.pos
    if item is None:
        print('no item to draw, returning ... ')
        return
    main.gui.draw_queue.append(DrawItem(item,main.gui.screen,pos=pos))
    print('item drawn at', pos)

def draw_until_deregister(event,main,uuid,item=None,pos=None):
    if pos is None:
        pos = event.pos
    if item is None:
        print('no item to draw, returning ... ')
        return
    if uuid in main.gui.permanent_draw_queue:
        main.gui.permanent_draw_queue[uuid].pos = pos
    else:
        main.gui.permanent_draw_queue[uuid] = DrawItem(item,main.gui.screen,pos=pos)

def drop_tree(event,main,uuid,tree=None):
    #deregister mouse_move callback
    main.context.tobecleaned.append([main.context.onMouseMove, uuid])
    del main.gui.permanent_draw_queue[uuid]
    pygame.mouse.set_visible(1)
    # check if that tree can go there. apply if so -- TBI
    cubepos = main.board.check_valid_tree_coord(event.pos,tree)
    print(cubepos)
    if cubepos is not False:
        main.board.add_tree(cubepos,tree)
    #kill self
    main.context.tobecleaned.append([main.context.onMouseUp, uuid])
    return


