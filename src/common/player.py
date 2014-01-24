import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite, Group, spritecollide
from pygame import Rect
from consts import *

any = __builtins__.any

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
        ac_dx = self.dx + self.speed*(self.walking_right - self.walking_left)
        ac_dy = self.dy

        sign_x = 2*(ac_dx > 0) - 1
        sign_y = 2*(ac_dy > 0) - 1

        continue_x = abs(ac_dx)
        continue_y = abs(ac_dy)

        while continue_x or continue_y:
            if continue_y != 0:
                self.rect.move_ip(0, sign_y)
                col = pg.sprite.spritecollide(self, world, False)
                if any(t.solid in col) or self.rect.bottom >= HEIGHT or self.rect.top < 0:
                    self.dy = 0
                    continue_y = 0
                    self.rect.move_ip(0, -sign_y)
                else:
                    continue_y -= 1
            if continue_x != 0:
                self.rect.move_ip(sign_x, 0)
                col = pg.sprite.spritecollide(self, world, False)
                if any(t.solid in col) or self.rect.right >= WIDTH or self.rect.left < 0:
                    self.dx = 0
                    continue_x = 0
                    self.rect.move_ip(-sign_x, 0)
                else:
                    continue_x -= 1

    def on_ground(self, world):
        self.rect.move_ip(0, 1)
        on = bool(pg.sprite.spritecollide(self, world, False))
        self.rect.move_ip(0, -1)
        return on

    def jump(self):
        self.dy = -20
