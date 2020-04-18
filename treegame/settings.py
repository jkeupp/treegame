import numpy; np=numpy
import hexy; hx=hexy

# layout settings

nx = 800
ny = 1200


hex_radius = 56

board_center = numpy.array([nx/2,nx/2],dtype='int')
gamelength = {'default':(4,0),
              'long': (5,0)} # those are termination criteria (epoch,tick)
# console settings

console_text_maxlen = 250 # px 
console_pos_lt      = numpy.array([108+nx,8],dtype='int')
console_pos_rb      = numpy.array([392+nx,192],dtype='int')
console_line_offset = 8


hudpos = numpy.array([800,0],dtype='int')
board_size_radius = 3

axepos = numpy.array([750,750],dtype='int')
epochpos1 = numpy.array([690,10],dtype='int')
epochpos2 = numpy.array([690,30],dtype='int')
initphase_labelpos = numpy.array([690,50],dtype='int')

tree_imgpos_offset   =  numpy.array([50,275],dtype='int') 
tree_row_height      =  numpy.array([0,150],dtype='int')

hud_tree_seedpos   = tree_imgpos_offset
hud_tree_smallpos  = tree_imgpos_offset + tree_row_height
hud_tree_mediumpos = tree_imgpos_offset + tree_row_height * 2
hud_tree_largepos  = tree_imgpos_offset + tree_row_height * 3

hud_tree_partitioning = [0.25,0.25,0.25,0.25] # tree img, avilable, stack, graveyard

hud_done_btn_pos = numpy.array([nx+50,175],dtype='int') 
hud_buy_btn_offset = numpy.array([0,50],dtype='int') 
hud_buy_btn_pos = [
    hud_tree_seedpos   + hud_buy_btn_offset + hudpos,
    hud_tree_smallpos  + hud_buy_btn_offset + hudpos,
    hud_tree_mediumpos + hud_buy_btn_offset + hudpos,
    hud_tree_largepos  + hud_buy_btn_offset + hudpos,
]

# dont't change, computed positions
hud_tree_labels = numpy.array([
                  [
                   numpy.array([150,225],dtype='int'),
                   numpy.array([150,225],dtype='int') + tree_row_height,
                   numpy.array([150,225],dtype='int') + tree_row_height*2,
                   numpy.array([150,225],dtype='int') + tree_row_height*3,
                  ],[
                   numpy.array([250,225],dtype='int'),
                   numpy.array([250,225],dtype='int') + tree_row_height,
                   numpy.array([250,225],dtype='int') + tree_row_height*2,
                   numpy.array([250,225],dtype='int') + tree_row_height*3,
                  ],[
                   numpy.array([350,225],dtype='int'),
                   numpy.array([350,225],dtype='int') + tree_row_height,
                   numpy.array([350,225],dtype='int') + tree_row_height*2,
                   numpy.array([350,225],dtype='int') + tree_row_height*3,
                  ]
                ],dtype='int') + hudpos
hud_tree_labels_player_offset = numpy.array(
    [
        [-25, 33],
        [ 25, 33],
        [-25, 83],
        [ 25, 83],
    ],dtype='int')

def rotate(vec,degrees):
    rad =numpy.deg2rad(degrees)
    rotmat = numpy.array([[numpy.cos(rad),numpy.sin(rad)],[-numpy.sin(rad), numpy.cos(rad)]])
    return numpy.dot(rotmat,vec.T).T

def npa(x):
    xx = numpy.array(x,dtype='int').reshape(1,3)
    xy = hx.cube_to_pixel(xx,hex_radius)[0]
    return xy

def ht(a,b,c):
    return numpy.array([a,b,c],dtype='int').reshape(1,3)

# sun and arrow positions
board_sun_positions={ 30:npa([ 4, 0,-4])+ board_center,
                      90:npa([ 4,-4,0])+ board_center,
                     150:npa([ 0,-4, 4])+ board_center,
                     210:npa([-4, 0, 4])+ board_center,
                     270:npa([-4, 4, 0])+ board_center,
                     330:npa([ 0, 4,-4])+ board_center}

# [npa([]), npa([]), npa([]), npa([]), npa([]), npa([])]
# 

arrow_positions_30 = numpy.array([npa([1,3,-4]), npa([2,2,-4]), npa([3,1,-4]), 
                                  npa([4,-3,-1]), npa([4,-2,-2]), npa([4,-1,-3])])

board_arrow_positions={ 30: arrow_positions_30+ board_center,
                        90: rotate(arrow_positions_30,-60)+ board_center,
                        150:rotate(arrow_positions_30,-120)+ board_center,
                        210:rotate(arrow_positions_30,180)+ board_center,
                        270:rotate(arrow_positions_30,120)+ board_center,
                        330:rotate(arrow_positions_30,60)+ board_center}

sun_box_size         =  100

n_line = hexy.get_hex_line(ht(0,3,-3),ht(3,0,-3)); n_line_rev = n_line[::-1]
ne_line = hexy.get_hex_line(ht(3,0,-3),ht(3,-3,0)); ne_line_rev = ne_line[::-1]
se_line = hexy.get_hex_line(ht(3,-3,0),ht(0,-3,3)); se_line_rev = se_line[::-1]
s_line = hexy.get_hex_line(ht(0,-3,3),ht(-3,0,3)); s_line_rev = s_line[::-1]
sw_line = hexy.get_hex_line(ht(-3,0,3),ht(-3,3,0)); sw_line_rev = sw_line[::-1]
nw_line = hexy.get_hex_line(ht(-3,3,0),ht(0,3,-3)); nw_line_rev = nw_line[::-1]

rays = {30:
            [numpy.array(hx.get_hex_line(x,y),dtype='int') for x,y in zip(n_line,sw_line_rev)] + 
            [numpy.array(hx.get_hex_line(x,y),dtype='int') for x,y in zip(ne_line[1:],s_line_rev[1:])],
        90:
            [numpy.array(hx.get_hex_line(x,y),dtype='int') for x,y in zip(ne_line,s_line_rev)] + 
            [numpy.array(hx.get_hex_line(x,y),dtype='int') for x,y in zip(se_line[1:],sw_line[1:])],
        150:
            [numpy.array(hx.get_hex_line(x,y),dtype='int') for x,y in zip(s_line_rev,nw_line)] + 
            [numpy.array(hx.get_hex_line(x,y),dtype='int') for x,y in zip(se_line_rev[1:],n_line[1:])],
        210:
            [numpy.array(hx.get_hex_line(x,y),dtype='int') for x,y in zip(sw_line_rev,n_line)] + 
            [numpy.array(hx.get_hex_line(x,y),dtype='int') for x,y in zip(s_line_rev[1:],ne_line[1:])],
        270:
            [numpy.array(hx.get_hex_line(x,y),dtype='int') for x,y in zip(nw_line_rev,ne_line)] + 
            [numpy.array(hx.get_hex_line(x,y),dtype='int') for x,y in zip(sw_line_rev[1:],se_line[1:])],
        330:
            [numpy.array(hx.get_hex_line(x,y),dtype='int') for x,y in zip(n_line_rev,se_line)] + 
            [numpy.array(hx.get_hex_line(x,y),dtype='int') for x,y in zip(nw_line_rev[1:],s_line[1:])]
        }

# game settings

tree_costs = {0:1, 1:1, 2:2, 3:3, -1:4}

tree_costs_fromstack={   
     0:{4:1, 3:1, 2:2, 1:2},
     1:{8:2, 7:2, 6:2, 5:2, 4:2, 3:2, 2:3, 1:3},
     2:{4:3, 3:3, 2:3, 1:4},
     3:{2:4, 1:5}
} # check if that's right!

tree_chop_gain = {3:[17,16,16,15,15,14,14],
                  2:[19,18,18,17,17],
                  1:[21,20,19,19],
                  0:[24,23,22],
                  }

tree_max_stack = {0:4,1:4,2:3,3:2}

num_sunpoints = 0

num_start_seedlings   = 2
num_start_smalltrees  = 4 
num_start_mediumtrees = 1
num_start_largetrees  = 0

num_seedlings   = 6
num_smalltrees  = 8
num_mediumtrees = 4
num_largetrees  = 2


def endgame_sunpoints2points(sunpoints):
    if sunpoints == 0:
        return 0
    elif [1,2].count(sunpoints) != 0: 
        return 1
    else:
        return numpy.min([7,int(numpy.floor((sunpoints+3)/3))])
    return
