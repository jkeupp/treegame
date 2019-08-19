import hexy as hx
import numpy; np = numpy
import pygame; pg=pygame




def get_lt_coords(surf,pos):
    width,height = surf.get_size()
    x = pos[0]-int(numpy.round(width/2))
    y = pos[1]-int(numpy.round(height/2))
    return numpy.array([x,y],dtype='int')

def colorize(image, newColor):
    """
    Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
    original).
    :param image: Surface to create a colorized copy of
    :param newColor: RGB color to use (original alpha values are preserved)
    :return: New colorized Surface instance
    """
    image = image.copy()

    # zero out RGB values
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(newColor[0:3] + [0,], None, pygame.BLEND_RGBA_ADD)

    return image

def get_pos_to_center_text(text,center):
    pos = numpy.array([int(numpy.round(center[0]-text.get_width()/2.0)), 
            int(numpy.round(center[1] - text.get_height()/2.0))],dtype='int')
    return pos