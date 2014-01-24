import sys, os
print __file__
__file_dir__ = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(__file_dir__, '..')))

import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite, Group, spritecollide

from common.player import Player
from common.consts import *
from common.world import *

pg.init()

class Camera(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def to_local(self, pos):
        return (pos[0] - self.x, pos[1] - self.y)

    def to_global(self, pos):
        return (pos[0] + self.x, pos[1] + self.y)

class Game(object):
    def __init__(self):
        self.player = Player()
        self.world = World(WIDTH/T_P, HEIGHT/T_P)
        self.camera = Camera(0, 0, WIDTH, HEIGHT)
        self.screen = pg.display.set_mode(SIZE)
        self.mouse_button_pressed = False
        self.mouse_pos = (0, 0)

    def run(self):
        while True:
            CLOCK.tick(FPS)
            self.handle_events()

            if self.mouse_button_pressed:
                self.handle_mouse_press()

            pressed = pg.key.get_pressed()
            self.player.walking_left = pressed[K_LEFT]
            self.player.walking_right = pressed[K_RIGHT]
            if pressed[K_UP] and self.player.on_ground(self.world):
                self.player.jump()

            self.player.update(self.world)
            self.screen.fill(BLACK)
            self.screen.blit(self.player.image,
                    self.camera.to_local(self.player.rect))
            self.world.draw(self.screen, self.camera)
            pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                self.mouse_pos = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                self.mouse_button_pressed = True
                self.mouse_pos = event.pos
            elif event.type == MOUSEBUTTONUP:
                self.mouse_button_pressed = False

    def handle_mouse_press(self):
        x, y = self.camera.to_global(self.mouse_pos)
        self.world.add_tile(x / T_P, y / T_P)

if __name__ == "__main__":
    Game().run()
