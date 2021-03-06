import sys, os
__file_dir__ = os.path.dirname(os.path.realpath(__file__))

import pygame as pg
from pygame.sprite import Sprite, Rect
from consts import *
from random import randrange

class TileMeta(type):
    def __new__(mcs, name, bases, d):
        new_tile_type = type.__new__(mcs, name, bases, d)
        if not hasattr(new_tile_type, 'tile_types'):
            new_tile_type.tile_types = []
        for attr in ['solid', 'deadly', 'win']:
            if not hasattr(new_tile_type, attr):
                setattr(new_tile_type, attr, False)
        new_tile_type.tile_types.append(new_tile_type)
        new_tile_type.index = len(new_tile_type.tile_types) - 1
        return new_tile_type

class Tile(Sprite):
    "Basic Tile"

    __metaclass__ = TileMeta


    def __init__(self, x, y, fill, load_image = False):
        """
        If load_image is false then fill is a color
        that is filled in
        Otherwise it is the image that should be loaded
        """
        Sprite.__init__(self)

        if load_image:
            image = pg.image.load(fill)
            self.image = pg.transform.scale(image.convert_alpha(),
                    (T_P*self.w, T_P*self.h))
            self.rect = self.image.get_rect()
            self.rect.move_ip(x * T_P, y * T_P)
        else:
            self.image = pg.Surface([T_P*self.w, T_P*self.h])
            self.image.fill(fill)

            self.rect = self.image.get_rect()
            self.rect.move_ip(x*T_P, y*T_P)

class Ground(Tile):
    "Ground Tile"
    w = 1
    h = 1
    solid = True
    cost = 1
    def __init__(self, x, y, load_image = False):
        Tile.__init__(self, x, y, _rand_nearby_color(GREEN))

class Spike(Tile):
    "Spike Tile"
    w = 3
    h = 3
    deadly = True
    cost = 3
    def __init__(self, x, y, load_image = False):
        if load_image:
            image = os.path.join(__file_dir__, "..", "..", "assets", "crusher.png")
            Tile.__init__(self, x, y, image, True)
        else:
            Tile.__init__(self, x, y, _rand_nearby_color(RED))



class Gold(Tile):
    "Gold Tile"
    w = 2
    h = 2
    win = True
    def __init__(self, x, y, load_image = False):
        Tile.__init__(self, x, y, YELLOW)

class Clear(Tile):
    "This is a pseudo tile used for removing other tiles"
    w = 1
    h = 1
    cost = 4
    def __init__(self, x, y, load_image = False):
        Tile.__init__(self, x, y, WHITE)

def _rand_nearby_color(color):
    c = color.r, color.g, color.b
    c = [min(max(i + randrange(-40, 41), 0), 255) for i in c]
    return pg.Color(*c)
