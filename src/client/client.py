import sys, os
__file_dir__ = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(__file_dir__, '..')))

import socket
import time
import json
import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite, Group, spritecollide

from screen_log import *
from common.player import Player
from common.consts import *
from common.world import *
from server_connection import *

pg.init()
# Needs pg to be initialized before declaring
FONT = pg.font.SysFont('monospace', 15)


keyboard_actions = {K_LEFT: LEFT, K_RIGHT: RIGHT, K_UP: JUMP}

class Camera(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_local(self, pos):
        return (pos[0] - self.x, pos[1] - self.y)

    def to_global(self, pos):
        return (pos[0] + self.x, pos[1] + self.y)

    def set_x_y(self, x, y):
        self.x = x
        self.y = y
        if self.x < 0:
            self.x = 0
        elif self.x > WORLD_WIDTH - WIDTH:
            self.x = WORLD_WIDTH - WIDTH
        if self.y < 0:
            self.y = 0
        elif self.y > WORLD_HEIGHT - HEIGHT:
            self.y = WORLD_HEIGHT - HEIGHT

    def add_x_offset(self, off):
        self.set_x_y(self.x + off, self.y)

    def add_y_offset(self, off):
        self.set_x_y(self.x, self.y + off)

class ClientGame(object):
    def __init__(self, ip):
        self.player_a = Player(RED, (1, 1))
        self.player_b = Player(BLUE, (1, 1))
        self.wins_a = 0
        self.wins_b = 0
        self.screen_log = ScreenLog(8)
        self.world = World(WORLD_WIDTH/T_P, WORLD_HEIGHT/T_P)
        self.camera = Camera(0, 0)
        self.screen = pg.display.set_mode(SIZE)
        self.mouse_button_pressed = False
        self.mouse_pos = (0, 0)
        self.connect_to_server(ip)
        self.cur_tile = Ground.index
        self.last_keys = { key: False for key in keyboard_actions}

    def connect_to_server(self, ip):
        s = socket.socket()
        s.connect((ip, SERVER_PORT))
        self.server = ServerConnection(s)
        self.role = self.server.wait_for_role()
        pg.display.set_caption(PLAYER_DESC[self.role])
        self.screen_log.log(PLAYER_DESC[self.role])
        print "Connected!"

    def run(self):
        while True:
            CLOCK.tick(FPS)
            self.handle_events()

            if self.mouse_button_pressed:
                self.handle_mouse_press()

            pressed = pg.key.get_pressed()
            my_keys = { key: pressed[key] for key in keyboard_actions}

            if my_keys != self.last_keys:
                for key, action in keyboard_actions.items():
                    if self.last_keys[key] != my_keys[key]:
                        self.server.move(my_keys[key], action)
                self.last_keys = my_keys

            update = self.server.get_update([self.player_a, self.player_b], self.world)
            if update and update[0] == END_GAME:
                self.wins_a = update[1]
                self.wins_b = update[2]
                self.world = World(WORLD_WIDTH/T_P, WORLD_HEIGHT/T_P)
                self.camera = Camera(0, 0)

            self.update_camera()
            self.screen.fill(WHITE)
            self.screen.blit(self.player_a.image,
                    self.camera.to_local(self.player_a.rect))
            self.screen.blit(self.player_b.image,
                    self.camera.to_local(self.player_b.rect))
            self.world.draw(self.screen, self.camera)
            self.draw_fps()
            self.draw_scores()
            if self.role == DISRUPTOR_TEAM_A:
                self.screen.blit(FONT.render("%d credits" % self.player_a.credits,
                    1, BLACK), (WIDTH - 250, 30))
            if self.role == DISRUPTOR_TEAM_B:
                self.screen.blit(FONT.render("%d credits" % self.player_b.credits,
                    1, BLACK), (WIDTH - 250, 30))
            if self.role == DISRUPTOR_TEAM_A or self.role == DISRUPTOR_TEAM_B:
                self.screen.blit(FONT.render("Current Tile: %s" % Tile.tile_types[self.cur_tile].__name__,
                    1, BLACK), (WIDTH - 250, 50))
                self.screen.blit(FONT.render("Tile Cost: %d" % Tile.tile_types[self.cur_tile].cost,
                    1, BLACK), (WIDTH - 250, 70))


            self.refresh_log()
            pg.display.flip()

    def refresh_log(self):
        init_y = 30
        for line in self.screen_log.get_logs():
            self.screen.blit(FONT.render(line, 1,  BLACK), (15, 20 + init_y))
            init_y += 15

    def draw_fps(self):
        self.screen.blit(FONT.render("FPS: %f" % CLOCK.get_fps(), 1,
            BLACK), (WIDTH - 100, HEIGHT - 30))

    def draw_scores(self):
        self.screen.blit(FONT.render(repr(self.wins_a), 1,
            RED), ((WIDTH / 2) - 20, 30))  
        self.screen.blit(FONT.render(repr(self.wins_b), 1,
            BLUE), ((WIDTH / 2) + 20, 30))

    def update_camera(self):
        if self.role in [DISRUPTOR_TEAM_A, DISRUPTOR_TEAM_B]:
            pressed = pg.key.get_pressed()
            if pressed[K_a]:
                self.camera.add_x_offset(-CAMERA_SPEED)
            if pressed[K_d]:
                self.camera.add_x_offset(CAMERA_SPEED)
            if pressed[K_w]:
                self.camera.add_y_offset(-CAMERA_SPEED)
            if pressed[K_s]:
                self.camera.add_y_offset(CAMERA_SPEED)
        else:
            if self.role == RUNNER_TEAM_A:
                center = self.player_a.rect.center
            else:
                center = self.player_b.rect.center

            self.camera.set_x_y(center[0] - (WIDTH / 2), center[1] - (WIDTH / 2))


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
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    self.cur_tile = Ground.index
                
                elif event.key == K_2:
                    self.cur_tile = Spike.index
                
                elif event.key == K_3:
                    self.cur_tile = Clear.index
                
                # Restart game
                elif event.key == KMOD_LCTRL | K_r:
                    self.suicide()
                
                # Save game
                elif event.key == KMOD_LCTRL | K_p:
                    self.save_now()

                # Toggle Debug/Developer
                elif event.key == KMOD_LCTRL | K_i:
                    print "Toggle devmode"
                    self.toggle_devmode()

    def toggle_devmode(self):
        self.server.send_data({'type' : DEVMODE})

    def suicide(self):
        self.server.send_data({'type' : SUICIDE})

    # Format: [Tiles] - Tile -> (index (type), x, y)
    def save_now(self):
        print "Saving world..."
        fname = SAVE_FILE_FORMAT + str(int(time.time())) + '.bin'
        f = open(fname, 'wb')
        f.write(json.dumps([(t.index ,t.rect.x, t.rect.y) for t in self.world if isinstance(t, Tile)]))
        f.close()
        print "World saved to ", fname

    def handle_mouse_press(self):
        x, y = self.camera.to_global(self.mouse_pos)
        self.server.add_tile(x / T_P, y / T_P, self.cur_tile)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s <server_ip>" % sys.argv[0]
        sys.exit(1)
    ClientGame(sys.argv[1]).run()

