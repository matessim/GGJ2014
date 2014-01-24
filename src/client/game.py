import sys
import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite, Group, spritecollide
from player import Player
from consts import *
from world import *

pg.init()

class Camera(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_local(self, pos):
        return (pos[0] - self.x, pos[1] - self.y)

    def to_global(self, pos):
        return (pos[0] + self.x, pos[1] + self.y)

class Game(object):
    def __init__(self):
        self.player = Player()
        self.world = World(WIDTH/T_P, HEIGHT/T_P)
        self.camera = Camera(0, 0)
        self.screen = pg.display.set_mode(SIZE)
        self.mouse_button_pressed = False
        self.mouse_pos = (0, 0)

    def run(self):
        while True:
            CLOCK.tick(FPS)
            self.handle_events()

            if self.mouse_button_pressed:
                self.handle_pressed()

            self.player.update()
            self.screen.fill(BLACK)
            self.screen.blit(self.player.image,
                    self.camera.to_local(self.player.rect))
            self.world.draw(self.screen, self.camera)
            pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEMOTION:
                self.mouse_pos = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                self.mouse_button_pressed = True
                self.mouse_pos = event.pos
            elif event.type == MOUSEBUTTONUP:
                self.mouse_button_pressed = False
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    self.player.jump()
                elif event.key == K_LEFT:
                    self.player.dx = -5
                elif event.key == K_RIGHT:
                    self.player.dx = 5
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    if (self.player.dx < 0):
                        self.player.dx = 0
                elif event.key == K_RIGHT:
                    if (self.player.dx > 0):
                        self.player.dx = 0
    def handle_pressed(self):
        x, y = self.camera.to_global(self.mouse_pos)
        self.world.add_tile(x / T_P, y / T_P)

if __name__ == "__main__":
    Game().run()
