import pygame as pg
from pygame.sprite import Sprite
from consts import *

class TileMeta(type):
    def __new__(mcs, name, bases, d):
        new_tile_type = type.__new__(mcs, name, bases, d)
        if not hasattr(new_tile_type, '_tile_types'):
            new_tile_type._tile_types = []
        for attr in ['solid', 'deadly', 'win']:
            if not hasattr(new_tile_type, attr):
                setattr(new_tile_type, attr, False)
        new_tile_type._tile_types.append(new_tile_type)
        new_tile_type._ind = len(new_tile_type._tile_types) - 1
        return new_tile_type

class Tile(Sprite):

    __metaclass__ = TileMeta

    def __init__(self, x, y, color):
        Sprite.__init__(self)

        self.image = pg.Surface([T_P*self.w, T_P*self.h])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.move_ip(x*T_P, y*T_P)

class Ground(Tile):
    w = 1
    h = 1
    solid = True
    cost = 1
    def __init__(self, x, y):
        Tile.__init__(self, x, y, _rand_nearby_color(GREEN))

class Bomb(Tile):
    w = 2
    h = 2
    deadly = True
    cost = 3
    def __init__(self, x, y):
        Tile.__init__(self, x, y, _rand_nearby_color(RED))

class Gold(Tile):
    w = 2
    h = 2
    win = True
    def __init__(self, x, y):
        Tile.__init__(self, x, y, YELLOW)

from random import randrange

def _rand_nearby_color(color):
    c = color.r, color.g, color.b
    c = [min(max(i + randrange(-40, 41), 0), 255) for i in c]
    return pg.Color(*c)
