import pygame; pg = pygame
import numpy; np = numpy
import collections
import hexy as hx
import os
import uuid

from . import util
from . import settings
from . import context

#from .lib import TreeSprite, Callback, draw_on_move, draw_until_deregister, drop_tree
from .lib import * 
from .example_hex import  make_hex_surface, HexTile, Selection, CyclicInteger, ClampedInteger

# the hexagonal coordinate system: 
# https://www.redblobgames.com/grids/hexagons/
# --> cube coordinates


#  +--------|----#
#  |        | H  |
#  | field  | U  |
#  |        | D  |
#  +--------|----#

HORIZONTAL_MARGIN = 20

COL_IDX = np.random.randint(0, 4, (7 ** 3))
COLORS = np.array([
    [244, 98, 105],   # red
    [251, 149, 80],   # orange
    [141, 207, 104],  # green
    [53, 111, 163],   # water blue
    [85, 163, 193],   # sky blue
])

RED   = [255,0,0]
GREEN = [0,255,0]
BLUE  =  [0,0,255]
BACKGROUND = [188,238,104]
BLACK = [0,0,0]

GREEN2 = [141, 207, 104]

P1= [61,89,171]
P2= [238,154,0]
P3= [200,25,118]
P4= [69,139,0]

PLAYER_COLORS = {0:P1,
                 1:P2,
                 2:P3,
                 3:P4}

class board(object):
    def __init__(self,main_instance):
        self.main = main_instance
        self.main.board = self
        self.create_board(n=settings.board_size_radius)
        return
    
    @property
    def players(self):
        return self.main.players

    def create_board(self,n=3):
        self.field_range=n
        self.field = HexField(self.main)
        return

    def check_valid_tree_coord(self,pos,tree):
        player = self.main.current_player
        hex_pos = self.field.get_hex_point(pos)
        if numpy.sum(numpy.abs(hex_pos)) < self.field.max_coord*3:
            return hex_pos
        else:
            return False

    def add_tree(self,cubepos,tree): # tree must be the tree instance already
        tree.add_to_board(cubepos)
        self.main.current_player.sunpoints -= settings.tree_costs[tree.size]
        self.main.logic.trees_planted_at_this_round.append(tuple(cubepos))
        #self.main.logic.cycle_players()
        #tree.

    def buy_tree(self,treetype):
        # we assume here checks have already been made
        cost = settings.tree_costs_fromstack[treetype][self.main.current_player.n(treetype,'stack')]
        self.main.console('tree %d bought for %d' % (treetype,cost))
        self.main.current_player.sunpoints -= cost
        self.main.current_player.stack[treetype][0].set_status('available')
        return
    
    def let_the_sun_shine(self):
        # TBI 
        # Evaluates Trees w.r.t. the current sun position
        return

class HUD(object):
    def __init__(self,main_instance,size,pos):
        self.main = main_instance
        self.main.gui.hud = self
        self.size = numpy.array(size,dtype='int')
        self.pos = numpy.array(pos,dtype='int')
        self.background_image = pygame.image.load("/home/julian/sandbox/treegame/images/hud.png")
        self.dx_sun = settings.sun_box_size / (len(self.players) +1)
        self.dx_treerow = settings.tree_row_height / (len(self.players) +1)
        self.make_tree_sprites()
        return

    @property
    def screen(self):
        return self.main.gui.screen

    @property
    def players(self):
        return self.main.players

    @property
    def gui(self):
        return self.main.gui

    def make_tree_sprites(self):
        self.seedsprites   =  {i:TreeSprite(img,self.pos+settings.hud_tree_seedpos)   for i, img in self.gui.seedlings.items()}
        self.smallsprites  =  {i:TreeSprite(img,self.pos+settings.hud_tree_smallpos)  for i, img in self.gui.smalltrees.items()}
        self.mediumsprites =  {i:TreeSprite(img,self.pos+settings.hud_tree_mediumpos) for i, img in self.gui.mediumtrees.items()}
        self.largesprites  =  {i:TreeSprite(img,self.pos+settings.hud_tree_largepos)  for i, img in self.gui.largetrees.items()}

    def draw(self):
        active_player = self.main.current_player
        self.screen.blit(self.background_image,self.pos)
        self.draw_sunpoints(active_player)
        self.draw_seedling_box(active_player)
        self.draw_smalltree_box(active_player)
        self.draw_mediumtree_box(active_player)
        self.draw_largetree_box(active_player)
        self.draw_stats()
        self.main.console.draw()
        self.draw_cycle_button()
        self.draw_buy_buttons()
        pass

    def draw_sunpoints(self,player):
        for i,pk in enumerate(self.players):
            p = self.players[pk]
            text = self.gui.font.render('%s: %2d' % (p.name,p.sunpoints),
                                        False,PLAYER_COLORS[i])      
            if p.name == player.name:
                text.set_alpha(255)
            else:
                text.set_alpha(95)
            pos = (int(numpy.round(self.pos[0]+10)), 
                   int(numpy.round(self.pos[1]+(i+1) * self.dx_sun - text.get_height()/2.0)))
            self.screen.blit(text,pos)
    
    def draw_seedling_box(self,player):
        self.seedsprites[player.idx].draw(self.screen)
        self.main.context.onMouseDown['seedlingCallback'] = self.set_seedling_callback

    def draw_seedling_box(self,player):
        self.seedsprites[player.idx].draw(self.screen)
        self.main.context.onMouseDown['seedlingCallback'] = self.set_seedling_callback

    def draw_smalltree_box(self,player):
        self.smallsprites[player.idx].draw(self.screen)
        self.main.context.onMouseDown['smalltreeCallback'] = self.set_smalltree_callback
    
    def draw_mediumtree_box(self,player):
        self.mediumsprites[player.idx].draw(self.screen)   
        self.main.context.onMouseDown['mediumtreeCallback'] = self.set_mediumtree_callback
    
    def draw_largetree_box(self,player):
        self.largesprites[player.idx].draw(self.screen) 
        self.main.context.onMouseDown['largetreeCallback'] = self.set_largetree_callback
    
    def draw_stats(self):
        player = self.main.current_player
        labels = ['available','stack','board']
        #import pdb; pdb.set_trace()
        for i,label in enumerate(labels): # i = kind_idx
            for j in range(4): # j = tree_idx
                label_txt = self.gui.font_medium.render(label, False, BLACK)
                center = settings.hud_tree_labels[i,j,:] # tree_idx, kind_idx
                pos = util.get_pos_to_center_text(label_txt,center) 
                self.screen.blit(label_txt,pos)
                for k,pk in enumerate(self.players): # k = player_idx
                    p = self.players[pk]
                    text = self.gui.font_xlarge.render(str(p.n(j,label)),False,PLAYER_COLORS[k])  
                    center2 = center + settings.hud_tree_labels_player_offset[k]
                    pos = util.get_pos_to_center_text(text,center2) 
                    self.screen.blit(text,pos)
    
    def draw_cycle_button(self):
        text = self.gui.font_large.render('DONE',False,PLAYER_COLORS[self.main.current_player.idx])
        if  'cyclebutton' in self.main.context.onMouseUp.keys():
            pass
        else:
            self.main.context.onMouseUp['cyclebutton'] = Callback(player_cycle_callback)
            self.main.gui.hud.donerect =  text.get_rect()
            self.draw_btn_pos = util.get_pos_to_center_text(text,settings.hud_done_btn_pos)
            self.main.gui.hud.donerect=self.main.gui.hud.donerect.move(self.draw_btn_pos[0],self.draw_btn_pos[1])
        self.gui.screen.blit(text,self.draw_btn_pos)
        return

    def draw_buy_buttons(self):
        # if one's ablle to buy: player color
        # if not: gray
        # show cost 
        p = self.main.current_player
        cost_dummy=1
        costs = [str(settings.tree_costs_fromstack[i][self.main.current_player.n(i,'stack')]) if self.main.current_player.n(i,'stack') != 0 else '-'  for i in range(4)
                    ]
        text_seed_buy = self.gui.font_medium.render('BUY (%1s)' % (costs[0],),False,PLAYER_COLORS[p.idx])
        text_small_buy = self.gui.font_medium.render('BUY (%1s)' % (costs[1],),False,PLAYER_COLORS[p.idx])
        text_medium_buy = self.gui.font_medium.render('BUY (%1s)' % (costs[2],),False,PLAYER_COLORS[p.idx])
        text_large_buy = self.gui.font_medium.render('BUY (%1s)' % (costs[3],),False,PLAYER_COLORS[p.idx])
        text = {0:text_seed_buy, 1:text_small_buy, 2:text_medium_buy, 3:text_large_buy}
        if  'buybutton_seed' in self.main.context.onMouseUp.keys():
            pass
        else:
            self.main.context.onMouseUp['buybutton_seed'] = Callback(player_buy_callback,args=(0,))
            self.main.context.onMouseUp['buybutton_small'] = Callback(player_buy_callback,args=(1,))
            self.main.context.onMouseUp['buybutton_medium'] = Callback(player_buy_callback,args=(2,))
            self.main.context.onMouseUp['buybutton_large'] = Callback(player_buy_callback,args=(3,))
            self.buyrect =  {}; self.buy_btn_pos = {}
            #text.get_rect()
            for i in range(4):
                self.buy_btn_pos[i] = util.get_pos_to_center_text(text[i],settings.hud_buy_btn_pos[i])
                self.buyrect[i]= text[i].get_rect().move(self.buy_btn_pos[i][0],self.buy_btn_pos[i][1]) 
        for i in range(4):
            self.gui.screen.blit(text[i],self.buy_btn_pos[i])
        return

    def set_seedling_callback(self,event,main):
        #import pdb; pdb.set_trace()
        if self.seedsprites[self.main.current_player.idx].rect.collidepoint(event.pos) is 0: return
        if self.main.current_player.n(0,'available') == 0: 
            # TBI: drop a note that it's not possible
            print('no more seedlings available!')
            return
        #ok, we got it! let's do something
        move_callback_identifier = uuid.uuid4()
        # register on_mouse_move for drawer 
        self.main.context.onMouseMove[move_callback_identifier] = Callback(
            draw_until_deregister, args = (move_callback_identifier,), kwargs={
                'item':self.gui.seedlings[self.main.current_player.idx],
                }
            )
        self.main.context.onMouseMove[move_callback_identifier](event,main)
        pygame.mouse.set_visible(0)
        # register on_mouse_down to check of seedling can be placed there and to cleanup
        self.main.context.onMouseUp[move_callback_identifier] =\
            Callback(drop_tree, args = (move_callback_identifier,),
            kwargs = {'tree':self.main.current_player.available[0][0]})

    def set_smalltree_callback(self,event,main):
        #import pdb; pdb.set_trace()
        if self.smallsprites[self.main.current_player.idx].rect.collidepoint(event.pos) is 0: return
        if self.main.current_player.n(1,'available') == 0: 
            # TBI: drop a note that it's not possible
            print('no more smalltrees available!')
            return
        #ok, we got it! let's do something
        move_callback_identifier = uuid.uuid4()
        # register on_mouse_move for drawer 
        self.main.context.onMouseMove[move_callback_identifier] = Callback(
            draw_until_deregister, args = (move_callback_identifier,), kwargs={
                'item':self.gui.smalltrees[self.main.current_player.idx],
                }
            )
        self.main.context.onMouseMove[move_callback_identifier](event,main)
        pygame.mouse.set_visible(0)
        # register on_mouse_down to check of seedling can be placed there and to cleanup
        self.main.context.onMouseUp[move_callback_identifier] =\
            Callback(drop_tree, args = (move_callback_identifier,),
            kwargs = {'tree':self.main.current_player.available[1][0]})

    def set_mediumtree_callback(self,event,main):
        #import pdb; pdb.set_trace()
        if self.mediumsprites[self.main.current_player.idx].rect.collidepoint(event.pos) is 0: return
        if self.main.current_player.n(2,'available') == 0: 
            # TBI: drop a note that it's not possible
            print('no more mediumtrees available!')
            return
        #ok, we got it! let's do something
        move_callback_identifier = uuid.uuid4()
        # register on_mouse_move for drawer 
        self.main.context.onMouseMove[move_callback_identifier] = Callback(
            draw_until_deregister, args = (move_callback_identifier,), kwargs={
                'item':self.gui.mediumtrees[self.main.current_player.idx],
                }
            )
        self.main.context.onMouseMove[move_callback_identifier](event,main)
        pygame.mouse.set_visible(0)
        # register on_mouse_down to check of seedling can be placed there and to cleanup
        self.main.context.onMouseUp[move_callback_identifier] =\
            Callback(drop_tree, args = (move_callback_identifier,),
            kwargs = {'tree':self.main.current_player.available[2][0]})

    def set_largetree_callback(self,event,main):
        #import pdb; pdb.set_trace()
        if self.largesprites[self.main.current_player.idx].rect.collidepoint(event.pos) is 0: return
        if self.main.current_player.n(3,'available') == 0: 
            # TBI: drop a note that it's not possible
            print('no more largetrees available!')
            return
        #ok, we got it! let's do something
        move_callback_identifier = uuid.uuid4()
        # register on_mouse_move for drawer 
        self.main.context.onMouseMove[move_callback_identifier] = Callback(
            draw_until_deregister, args = (move_callback_identifier,), kwargs={
                'item':self.gui.largetrees[self.main.current_player.idx],
                }
            )
        self.main.context.onMouseMove[move_callback_identifier](event,main)
        pygame.mouse.set_visible(0)
        # register on_mouse_down to check of seedling can be placed there and to cleanup
        self.main.context.onMouseUp[move_callback_identifier] =\
            Callback(drop_tree, args = (move_callback_identifier,),
            kwargs = {'tree':self.main.current_player.available[3][0]})

class GUI(object):
    def __init__(self,main_instance,nx=1200, ny=800):
        self.main = main_instance
        self.main.gui = self
        self.image_dir = '/home/julian/sandbox/treegame/images/' # sry for hardcoded path!
        self.board = self.main.board
        self.board.field.gui = self
        self.res   = (nx,ny)
        self.woods = (ny,ny)
        self.woods_center = numpy.array([ny/2,ny/2])
        self.draw_queue = []
        self.permanent_draw_queue = {}
        self.create_window()     
        self.load_tree_images()
        self.load_sun_and_arrows()
        self.hud = HUD(self.main,(nx-ny,ny), (ny,0)) # main, hudsize, hudpos 
        self.draw_board()   
        return

    def load_sun_and_arrows(self):
        self.sun_and_arrows = pg.image.load(self.image_dir+'sun_and_arrows_90.png').convert_alpha()
        self.arrows = pg.image.load(self.image_dir+'arrow_90.png').convert_alpha()
        self.sun_and_arrows_rotated = {}; self.arrows_rotated = {}
        # pre-rotate and store copies in a dictionary for quick access
        # sun can be at 30, 90, 150, 210, 270 and 330 degrees
        angle_offset = 180
        for i,angle in enumerate([30, 90, 150, 210, 270, 330]):
            self.arrows_rotated[angle] = pygame.transform.rotate(self.arrows, -angle+angle_offset)
            self.sun_and_arrows_rotated[angle] = pygame.transform.rotate(self.sun_and_arrows, -angle+angle_offset)


    def load_tree_images(self):
        self.seedling = pg.image.load(self.image_dir+'tree0_90.png').convert_alpha()
        self.smalltree = pg.image.load(self.image_dir+'tree1_90.png').convert_alpha()
        self.mediumtree = pg.image.load(self.image_dir+'tree2_90.png').convert_alpha()
        self.largetree = pg.image.load(self.image_dir+'tree3_90.png').convert_alpha()
        self.seedlings = {i:util.colorize(self.seedling,PLAYER_COLORS[i]) for i in range(len(self.board.players))}
        self.smalltrees = {i:util.colorize(self.smalltree,PLAYER_COLORS[i]) for i in range(len(self.board.players))}
        self.mediumtrees = {i:util.colorize(self.mediumtree,PLAYER_COLORS[i]) for i in range(len(self.board.players))}
        self.largetrees = {i:util.colorize(self.largetree,PLAYER_COLORS[i]) for i in range(len(self.board.players))}
        self.usertrees = {0:self.seedlings,
                          1:self.smalltrees,
                          2:self.mediumtrees,
                          3:self.largetrees}

    def create_window(self):
        self.screen = pygame.display.set_mode(self.res)
        self.font = pg.font.SysFont("monospace", 12, True)
        self.font_medium = pg.font.SysFont("monospace", 18, True)
        self.font_large = pg.font.SysFont("monospace", 24, True)
        self.font_xlarge = pg.font.SysFont("monospace", 32, True)
        pygame.display.set_caption(" ### treegame ### ")
        pygame.mouse.set_visible(1)
        self.fieldwidth = (self.woods[1] - 2*HORIZONTAL_MARGIN ) / (self.board.field_range*2) #integer division

    def draw(self):
        self.draw_board()
        self.draw_hud()
        self.draw_sun()
        self.draw_draw_queue()

    def draw_board(self):
        self.screen.fill(BACKGROUND)
        self.board.field.draw(self.screen,self.font)
        return

    def draw_hud(self):
        self.hud.draw()
        return

    def draw_sun(self):
        #sun 
        sun_angle = self.main.logic.sunpos
        sun = self.sun_and_arrows_rotated[sun_angle]
        sunpos = util.get_lt_coords(sun,settings.board_sun_positions[sun_angle])
        self.screen.blit(sun, sunpos)
        for arpos in settings.board_arrow_positions[sun_angle]:
            self.screen.blit(self.arrows_rotated[sun_angle],util.get_lt_coords(self.arrows_rotated[sun_angle],arpos))

    def draw_draw_queue(self):
        for qitem in self.draw_queue:
            qitem.draw()
        self.draw_queue = []

        for qkey,qitem in self.permanent_draw_queue.items():
            qitem.draw()

    def render(self):
        pygame.display.flip()
        return


    ##### draw helpers #####

    def draw_field(self,f):
        center = f
        return




class HexField(object):
    def __init__(self,main,size=(800,800),hex_radius=56,caption = 'treegame',gui=None):
        self.main = main
        self.gui = gui
        self.caption = caption
        self.size = np.array(size)
        self.width, self.height = self.size
        self.center = self.size / 2
        self.hex_radius = hex_radius
        self.hex_map = hx.HexMap()
        self.max_coord = 3

        self.rad = ClampedInteger(3, 1, 5) #not yet sure what this does.

        self.selected_hex_image = make_hex_surface(
                (128, 128, 128, 160), 
                self.hex_radius, 
                (255, 255, 255), 
                hollow=True)
        self.selection_type = CyclicInteger(3, 0, 3)

        # Get all possible coordinates within `self.max_coord` as radius.
        self.cube_coordinates = numpy.array(hx.get_spiral(np.array((0, 0, 0)), 1, self.max_coord),dtype='int')
        self.axial_coordinates = hx.cube_to_axial(self.cube_coordinates)
        self.ntiles = self.cube_coordinates.shape[0]
        hex_tiles = []
        for i,axial in enumerate(self.axial_coordinates):
            hex_tiles.append(HexTile(axial,GREEN2+[255],hex_radius))
        self.hex_tiles = hex_tiles      
        self.hex_map[np.array(self.axial_coordinates)] = hex_tiles  
        self.cube_indices = {tuple(x):i for i,x in enumerate(self.cube_coordinates)}
        self._tile_occupation = {i:None for i in range(self.ntiles)}
        return

    def get_tile_occupation(self,pos):
        if type(pos) == type(tuple):
            return self._tile_occupation[self.cube_indices(pos)]
        else: 
            return self._tile_occupation[self.get_cube_index(pos)]

    def get_cube_index(self,pos):
        pos_tupl = tuple(pos)
        return self.cube_indices[pos_tupl]

    def get_hex_point(self,pos):
        cubepos =hx.pixel_to_cube(np.array([pos - self.center]),self.hex_radius)
        #import pdb; pdb.set_trace()
        return numpy.array(cubepos[0],dtype='int')

    def get_cartesian_point(self,cubepos):
        return hx.cube_to_pixel(cubepos.reshape((1,3)),self.hex_radius)[0]

    def draw(self,main_surf,font):
        # show all hexes
        hexagons = list(self.hex_map.values())
        hex_positions = np.array([hexagon.get_draw_position() for hexagon in hexagons])
        sorted_indexes = np.argsort(hex_positions[:, 1])
        for index in sorted_indexes:
            main_surf.blit(hexagons[index].image, hex_positions[index] + self.center)
        
        for hexagon in list(self.hex_map.values()):
            #text= '%5.2f %5.2f\n' % tuple(hexagon.get_position().tolist())
            #print(hexagon.axial_coordinates.tolist())
            text = '%d %d %d' % tuple(hexagon.cube_coordinates[0].tolist())
            text = font.render(text, False, (0, 0, 0))
            text.set_alpha(160)
            text_pos = hexagon.get_position() + self.center
            text_pos -= (text.get_width() / 2, text.get_height() / 2 + 33)
            idx = self.cube_indices[tuple(hexagon.cube_coordinates[0])]

            main_surf.blit(text, text_pos)
        for idx in range(self.ntiles):
            if self._tile_occupation[idx] is not None:
                self._tile_occupation[idx].draw()















