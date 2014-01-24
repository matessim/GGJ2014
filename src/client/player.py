import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite, Group, spritecollide
from consts import *

class Player(Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((40, 40))
        pg.draw.circle(self.image, RED, (20, 20), 20)
        self.rect = self.image.get_rect()
        self.dx = 0
        self.dy = 0
        self.speed = 5

    def update(self):
        self.dy += GRAVITY

        self.rect.move_ip(self.dx, self.dy)
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.dx = 0
        if self.rect.left < 0:
            self.rect.left = 0
            self.dx = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.dy = 0

    def jump(self):
        if self.dy == 0:
            self.dy = -20


