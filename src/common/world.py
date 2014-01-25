import sys
import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite
from consts import *
from tile import *
from random import random, randrange

class World(object):
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.tiles = {}

    def randomize_start(self):
        updates = []
        for x in xrange(self.w):
            if random() < 0.3:
                self.tiles[(x, self.h-1)] = Ground(x, self.h-1)
                updates.append((x, self.h-1, Ground.index))

        for x in xrange(self.w):
            self.tiles[(x, 0)] = Ground(x, 0)
            updates.append((x, 0, Ground.index))

        for y in xrange(self.h):
            self.tiles[(0, y)] = Ground(0, y)
            self.tiles[(self.w-1, y)] = Ground(self.w-1, y)
            updates.append((0, y, Ground.index))
            updates.append((self.w-1, y, Ground.index))

        x_win = randrange(1, self.w-1)
        y_win = randrange(1, self.h / 2)
        self.tiles[(x_win, y_win)] = Gold(x_win, y_win)
        updates.append((x_win, y_win, Gold.index))
        return updates

    def draw(self, surface, camera):
        for tile in self:
            surface.blit(tile.image, camera.to_local(tile.rect))

    def add_tile(self, t_x, t_y, t):
        tile_type = Tile.tile_types[t]
        tile = tile_type(t_x, t_y)
        if pg.sprite.spritecollide(tile, self, False):
            return False
        self.tiles[(t_x, t_y)] = tile
        return True

    def __iter__(self):
        return self.tiles.itervalues()

    def iter_visible(self, camera):
        # TODO: catch things bigger then 1X1...
        ul_t = (camera.x / T_P, camera.y / T_P)
        dr_t = ((camera.x + WIDTH) / T_P, (camera.y + HEIGHT) / T_P)
        for tile_x in xrange(ul_t[0], dr_t[0]+1):
            for tile_y in xrange(ul_t[1], dr_t[1]+1):
                if self.tiles.has_key((tile_x, tile_y)):
                    yield self.tiles[(tile_x, tile_y)]


