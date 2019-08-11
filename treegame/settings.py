import numpy; np=numpy


# layout settings
board_size_radius = 3

tree_imgpos_offset   =  numpy.array([50,275],dtype='int') 
tree_row_height      =  numpy.array([0,150],dtype='int')

hud_tree_seedpos   = tree_imgpos_offset
hud_tree_smallpos  = tree_imgpos_offset + tree_row_height
hud_tree_mediumpos = tree_imgpos_offset + tree_row_height * 2
hud_tree_largepos  = tree_imgpos_offset + tree_row_height * 3

sun_box_size         =  100



