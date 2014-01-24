import sys
import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite
from consts import *
from tile import *

class World(object):
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.tiles = {}
        for x in xrange(w):
            self.tiles[(x, h-1)] = Ground(x, h-1)

    def draw(self, surface, camera):
        for tile in self.iter_visible(camera):
            surface.blit(tile.image, camera.to_local(tile.rect))

    def add_tile(self, t_x, t_y):
        self.tiles[(t_x, t_y)] = Ground(t_x, t_y)

    def __iter__(self):
        return self.tiles.itervalues()

    def iter_visible(self, camera):
        ul_t = (camera.x / T_P, camera.y / T_P)
        dr_t = ((camera.x + camera.w) / T_P, (camera.y + camera.h) / T_P)
        for tile_x in xrange(ul_t[0], dr_t[0]+1):
            for tile_y in xrange(ul_t[1], dr_t[1]+1):
                if self.tiles.has_key((tile_x, tile_y)):
                    yield self.tiles[(tile_x, tile_y)]


