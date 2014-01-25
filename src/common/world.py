import sys
import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite, Group
from consts import *
from tile import *
from random import random, randrange

class World(Group):
    def __init__(self, w, h):
        Group.__init__(self)
        self.w = w
        self.h = h

    def randomize_start(self):
        updates = []
        for x in xrange(self.w):
            if random() < 0.3:
                self.add(Ground(x, self.h-1))
                updates.append((x, self.h-1, Ground.index))

        for x in xrange(self.w):
            self.add(Ground(x, 0))
            updates.append((x, 0, Ground.index))

        for y in xrange(self.h):
            self.add(Ground(0, y))
            self.add(Ground(self.w-1, y))
            updates.append((0, y, Ground.index))
            updates.append((self.w-1, y, Ground.index))

        x_win = randrange(1, self.w-1)
        y_win = randrange(1, self.h / 2)
        self.add(Gold(x_win, y_win))
        updates.append((x_win, y_win, Gold.index))
        return updates

    def draw(self, surface, camera):
        for tile in self:
            surface.blit(tile.image, camera.to_local(tile.rect))

    def add_tile(self, t_x, t_y, t):
        tile_type = Tile.tile_types[t]
        tile = tile_type(t_x, t_y)
        collisions = pg.sprite.spritecollide(tile, self, False)
        if tile_type == Clear:
            if len(collisions) != 1:
                return False
            if isinstance(collisions[0], Gold):
                return False
            self.remove(collisions[0])
            return True

        elif collisions:
            return False

        self.add(tile)
        return True
