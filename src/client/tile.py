import pygame as pg
from pygame.sprite import Sprite
from consts import *

class Tile(Sprite):

    def __init__(self, x, y, color):
        Sprite.__init__(self)

        self.image = pg.Surface([T_P, T_P])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.move_ip(x*T_P, y*T_P)

class Ground(Tile):

    def __init__(self, x, y):
        Tile.__init__(self, x, y, GREEN)
        self.solid = True


