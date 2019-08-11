import pygame; pg = pygame
import numpy; np = numpy
import collections
import hexy as hx
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

RED   = (255,0,0)
GREEN = (0,255,0)
BLUE  =  (0,0,255)
BACKGROUND = (188,238,104)

GREEN2 = [141, 207, 104]

P1= (61,89,171)
P2= (238,154,0)
P3= (0,238,118)
P4= (69,139,0)

Point = collections.namedtuple("Point", ["x", "y"])
#Orientation = collections.namedtuple("Orientation", ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])
#layout = Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0, math.sqrt(3.0) / 3.0, -1.0 / 3.0, 0.0, 2.0 / 3.0, 0.5)

class board(object):
    def __init__(self,n=3):
        self.create_board(n=n)
        return

    def create_board(self,n=3):
        self.field_range=n
        self.field = HexField()
        return

class HUD(object):
    def __init__(self,):
        return

    def draw(self):
        #



class GUI(object):
    def __init__(self,uboard,nx=1200, ny=800):
        self.board = uboard
        self.res   = (nx,ny)
        self.woods = (ny,ny)
        self.woods_center = (ny/2,ny/2)
        self.hudpos   = (nx-ny,ny)
        self.create_window()     
        self.draw_board()   
        return

    def create_window(self):
        self.screen = pygame.display.set_mode(self.res)
        self.font = pg.font.SysFont("monospace", 12, True)
        pygame.display.set_caption(" ### treegame ### ")
        pygame.mouse.set_visible(1)
        self.fieldwidth = (self.woods[1] - 2*HORIZONTAL_MARGIN ) / (self.board.field_range*2) #integer division

    def draw_board(self):
        self.screen.fill(BACKGROUND)
        self.board.field.draw(self.screen,self.font)
        return

    def draw_hud()

    def render(self):
        pygame.display.flip()
        return


    ##### draw helpers #####

    def draw_field(self,f):
        center = f
        return




class HexField(object):
    def __init__(self,size=(800,800),hex_radius=56,caption = 'treegame'):
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
        self.clicked_hex = np.array([0, 0, 0])

        # Get all possible coordinates within `self.max_coord` as radius.
        self.spiral_coordinates = hx.get_spiral(np.array((0, 0, 0)), 1, self.max_coord)
        self.axial_coordinates = hx.cube_to_axial(self.spiral_coordinates)

        hex_tiles = []
        for i,axial in enumerate(self.axial_coordinates):
            hex_tiles.append(HexTile(axial,GREEN2+[255],hex_radius))
        self.hex_tiles = hex_tiles      
        self.hex_map[np.array(self.axial_coordinates)] = hex_tiles  
        return

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
            text_pos -= (text.get_width() / 2, text.get_height() / 2)
            main_surf.blit(text, text_pos)
        
        
        


### draw routines
# using axial coordinates!
class field(object):
    def __init__(self,x,y,obj=None,belongs=None):
        self.pos = (x,y)
        self.x,self.y = x,y
        self.obj = obj
        self.belongs=belongs
        return

    def dist(self,other):
        return geo.hex_distance()
        #return abs(self.x-other.x) + abs(self.y - other.y) + abs(self.z - other.z) / 2
    
    def distvec():
        pass