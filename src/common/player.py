import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite, Group, spritecollide
from pygame import Rect
from consts import *


class Player(Sprite):
    def __init__(self, color):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((40, 40), pg.SRCALPHA)
        pg.draw.circle(self.image, color, (20, 20), 20)
        pg.draw.circle(self.image, BLACK, (20, 20), 21, 2)
        self.rect = self.image.get_rect()
        self.speed = T_P / 2
        self.respawn()

    def respawn(self):
        self.dx = 0
        self.dy = 0
        self.walking_left = False
        self.walking_right = False
        self.rect.x = self.rect.y = 0

    def update(self, world):
        self.dy += GRAVITY
        if self.dy > T_P:
            self.dy = T_P
        x_update = self.dx + self.speed*(self.walking_right - self.walking_left)
        y_update = self.dy

        self.rect.move_ip(x_update, y_update)

        collisions = pg.sprite.spritecollide(self, world, False)

        stuck = False

        out_of_bounds = (self.rect.bottom > WORLD_HEIGHT or self.rect.top < 0)
        out_of_bounds |= (self.rect.right > WORLD_WIDTH or self.rect.left < 0)

        if out_of_bounds:
            self.die()
            return

        for block in collisions:
            if block.deadly:
                self.die()
                return
            if block.solid:
                stuck = True

        if stuck:
            # We hit something. Let's undo and move a pixel at a time
            # in each direction until we're stuck
            self.rect.move_ip(-x_update, -y_update)
            x_direction = 1 if x_update > 0 else -1
            y_direction = 1 if y_update > 0 else -1

            while x_update != 0 or y_update != 0:
                if y_update != 0:
                    self.rect.move_ip(0, y_direction)
                    if any(i.solid for i in pg.sprite.spritecollide(self, world, False)):
                        y_update = 0
                        self.dy = 0
                        self.rect.move_ip(0, -y_direction)
                    else:
                        y_update -= y_direction
                if x_update != 0:
                    self.rect.move_ip(x_direction, 0)

                    if any(i.solid for i in pg.sprite.spritecollide(self, world, False)):
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

    def die(self):
        self.respawn()
