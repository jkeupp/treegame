import numpy; np=numpy


# layout settings

nx = 800
ny = 1200




# console settings

console_text_maxlen = 250 # px 
console_pos_lt      = numpy.array([108+nx,8],dtype='int')
console_pos_rb      = numpy.array([392+nx,192],dtype='int')
console_line_offset = 8


hudpos = numpy.array([800,0],dtype='int')
board_size_radius = 3



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


sun_box_size         =  100

# game settings

tree_costs = {0:1, 1:2, 2:3, 3:4, -1:4}

tree_costs_fromstack={   
     0:{4:1, 3:1, 2:2, 1:2},
     1:{8:2, 7:2, 6:2, 5:2, 4:2, 3:2, 2:3, 1:3},
     2:{4:3, 3:3, 2:4, 1:4},
     3:{2:4, 1:5}
} # check if that's right!


num_sunpoints = 100

num_start_seedlings   = 2
num_start_smalltrees  = 4 
num_start_mediumtrees = 1
num_start_largetrees  = 0

num_seedlings   = 6
num_smalltrees  = 8
num_mediumtrees = 4
num_largetrees  = 2

