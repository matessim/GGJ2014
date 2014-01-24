import sys, os
__file_dir__ = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(__file_dir__, '..')))

import socket
import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite, Group, spritecollide

from common.player import Player
from common.consts import *
from common.world import *
from server_connection import *

pg.init()

keyboard_actions = {K_LEFT: LEFT, K_RIGHT: RIGHT, K_UP: JUMP}

class Camera(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_local(self, pos):
        return (pos[0] - self.x, pos[1] - self.y)

    def to_global(self, pos):
        return (pos[0] + self.x, pos[1] + self.y)

class ClientGame(object):
    def __init__(self, ip):
        self.player = Player()
        self.world = World(WIDTH/T_P, HEIGHT/T_P)
        self.camera = Camera(0, 0)
        self.screen = pg.display.set_mode(SIZE)
        self.mouse_button_pressed = False
        self.mouse_pos = (0, 0)
        self.connect_to_server(ip)

    def connect_to_server(self, ip):
        s = socket.socket()
        s.connect((ip, SERVER_PORT))
        self.server = ServerConnection(s)

    def run(self):
        while True:
            CLOCK.tick(FPS)
            self.handle_events()

            if self.mouse_button_pressed:
                self.handle_mouse_press()

            pressed = pg.key.get_pressed()

            for key, action in keyboard_actions.items():
                self.server.move(pressed[key], action)

            self.server.get_update(self.player, self.world)
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
        self.server.add_tile(x / T_P, y / T_P)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s <server_ip>" % sys.argv[0]
        sys.exit(1)
    ClientGame(sys.argv[1]).run()
