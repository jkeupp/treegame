import numpy; np=numpy


# layout settings

nx = 800
ny = 1200

hudpos = numpy.array([800,0],dtype='int')


board_size_radius = 3

tree_imgpos_offset   =  numpy.array([50,275],dtype='int') 
tree_row_height      =  numpy.array([0,150],dtype='int')

hud_tree_seedpos   = tree_imgpos_offset
hud_tree_smallpos  = tree_imgpos_offset + tree_row_height
hud_tree_mediumpos = tree_imgpos_offset + tree_row_height * 2
hud_tree_largepos  = tree_imgpos_offset + tree_row_height * 3

hud_tree_partitioning = [0.25,0.25,0.25,0.25] # tree img, avilable, stack, graveyard

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

num_sunpoints = 100

num_start_seedlings   = 2
num_start_smalltrees  = 4 
num_start_mediumtrees = 1
num_start_largetrees  = 0

num_seedlings   = 6
num_smalltrees  = 8
num_mediumtrees = 4
num_largetrees  = 2

