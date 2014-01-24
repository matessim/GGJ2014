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
        ul_t = self.pixel_to_tile(camera.x, camera.y)
        rect = surface.get_rect()
        dr_t = self.pixel_to_tile(camera.x + rect[2], camera.y + rect[3])
        for tile_x in xrange(ul_t[0], dr_t[0]+1):
            for tile_y in xrange(ul_t[1], dr_t[1]+1):
                if self.tiles.has_key((tile_x, tile_y)):
                    tile = self.tiles[(tile_x, tile_y)]
                    surface.blit(tile.image, camera.to_local(tile.rect))

    def pixel_to_tile(self, p_x, p_y):
        return (p_x / T_P, p_y / T_P)

    def add_tile(self, t_x, t_y):
        self.tiles[(t_x, t_y)] = Ground(t_x, t_y)

    def __iter__(self):
        return self.tiles.itervalues()
