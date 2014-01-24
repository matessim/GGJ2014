import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite, Group, spritecollide
from pygame import Rect
from consts import *

class Player(Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((40, 40))
        pg.draw.circle(self.image, RED, (20, 20), 20)
        self.rect = self.image.get_rect()
        self.dx = 0
        self.dy = 0
        self.speed = T_P / 2
        self.walking_left = False
        self.walking_right = False

    def update(self, world):
        self.dy += GRAVITY
        x_update = self.dx + self.speed*(self.walking_right - self.walking_left)
        y_update = self.dy

        self.rect.move_ip(x_update, y_update)
        col = pg.sprite.spritecollide(self, world, False)
        if (col or self.rect.bottom >= HEIGHT or self.rect.top < 0 or
                self.rect.right >= WIDTH or self.rect.left < 0):
            # We hit something. Let's undo and move a pixel at a time
            # in each direction until we're stuck
            self.rect.move_ip(-x_update, -y_update)
            x_direction = 1 if x_update > 0 else -1
            y_direction = 1 if y_update > 0 else -1

            while x_update != 0 or y_update != 0:
                if y_update != 0:
                    self.rect.move_ip(0, y_direction)
                    col = pg.sprite.spritecollide(self, world, False)
                    if col or self.rect.bottom >= HEIGHT or self.rect.top < 0:
                        y_update = 0
                        self.dy = 0
                        self.rect.move_ip(0, -y_direction)
                    else:
                        y_update -= y_direction
                if x_update != 0:
                    self.rect.move_ip(x_direction, 0)
                    col = pg.sprite.spritecollide(self, world, False)
                    if col or self.rect.right >= WIDTH or self.rect.left < 0:
                        x_update = 0
                        self.dx = 0
                        self.rect.move_ip(-x_direction, 0)
                    else:
                        x_update -= x_direction

    def on_ground(self, world):
        self.rect.move_ip(0, 1)
        on = bool(pg.sprite.spritecollide(self, world, False))
        self.rect.move_ip(0, -1)
        return on

    def jump(self):
        self.dy = -20
