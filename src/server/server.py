# Author : MM
# Purpose: Run the game server

import sys, os
__file_dir__ = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(__file_dir__, '..')))

import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite, Group, spritecollide

from common.player import Player
from common.consts import *
from common.world import *

import select
import socket
import threading
import time

from client_connection import *

pg.init()

class ServerGame(object):
    def __init__(self):
        w_tiles, h_tiles = WORLD_WIDTH/T_P, WORLD_HEIGHT/T_P
        a_spawn = (randrange(T_P, WORLD_WIDTH-4*T_P),
                    randrange((WORLD_HEIGHT / 2) + 2*T_P, WORLD_HEIGHT - 4*T_P))
        b_spawn = (randrange(T_P, WORLD_WIDTH-4*T_P),
                    randrange((WORLD_HEIGHT / 2) + 2*T_P, WORLD_HEIGHT - 4*T_P))
        self.player_a = Player(BLACK, a_spawn)
        self.player_b = Player(BLACK, b_spawn)
        self.world = World(w_tiles, h_tiles)
        self.updates = self.world.randomize_start()
        self.clients = []

    def run(self):
        self.connect_players()
        self.start_game()
        self.update_clients()
        i = 0
        while True:
            CLOCK.tick(FPS)
            self.get_actions()
            a_ret = self.player_a.update(self.world)
            if a_ret == WIN:
                pass
                #TODO
            b_ret = self.player_b.update(self.world)
            if b_ret == WIN:
                pass
                #TODO
            self.update_clients()
            i += 1
            if i % FRAMES_PER_CREDIT == 0:
                i = 0
                self.player_a.credits += 1
                self.player_b.credits += 1

    def start_game(self):
        for client in self.clients:
            print "Sent start game to client!"
            client.send_data({'type' : START_GAME, 'role' : client.role})

    def connect_players(self):
        role_giver = self.role_distributor()
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(SERVER_ADDR)
        sock.listen(MAX_CLIENTS)
        while len(self.clients) < MAX_CLIENTS:
            host, endpoint = sock.accept()
            new_client = ClientConnection(host, endpoint, role_giver.next())
            print "Accepted new client:", repr(new_client)
            self.clients.append(new_client)

    def get_actions(self):
        clients_with_actions = select.select(self.clients, [], [], 0)
        for client in clients_with_actions[0]:
            for event in client.get_data():
                if event['type'] == MOVE:
                    self.handle_move(client, event)
                elif event['type'] == ADD_ITEM:
                    self.handle_add_item(client, event)
                elif event['type'] == SUICIDE:
                    if client.role == RUNNER_TEAM_A:
                        self.player_a.die()
                    elif client.role == RUNNER_TEAM_B:
                        self.player_b.die()

    def handle_move(self, client, event):
        if client.role == RUNNER_TEAM_A:
            player = self.player_a
        elif client.role == RUNNER_TEAM_B:
            player = self.player_b
        else:
            return

        if event['direction'] == LEFT:
            player.walking_left = event['pressed']
        elif event['direction'] == RIGHT:
            player.walking_right = event['pressed']
        elif event['direction'] == JUMP:
            if event['pressed'] and player.on_ground(self.world):
                player.jump()

    def handle_add_item(self, client, event):
        if client.role == DISRUPTOR_TEAM_A:
            player = self.player_a
        elif client.role == DISRUPTOR_TEAM_B:
            player = self.player_b
        else:
            return

        x = event['x']
        y = event['y']
        t = event['t']

        tile_type = Tile.tile_types[t]
        if tile_type.cost > player.credits:
            return

        min_dist = tile_type.w * tile_type.h
        a_x, a_y = self.player_a.rect.center
        b_x, b_y = self.player_b.rect.center
        if (((x+0.5)*T_P - a_x)**2 + ((y+0.5)*T_P - a_y)**2 < 9*T_P*T_P*min_dist  or \
            ((x+0.5)*T_P - b_x)**2 + ((y+0.5)*T_P - b_y)**2 < 9*T_P*T_P*min_dist):
            return
        added = self.world.add_tile(x, y, t)
        if added:
            self.updates.append((x, y, t))
            player.credits -= tile_type.cost

    def update_clients(self):
        p1 = self.player_a.rect
        p2 = self.player_b.rect
        for client in self.clients:
            client.send_data({'player_one': {'x': p1.x, 'y': p1.y,
                'credits': self.player_a.credits},
                'player_two' : {'x': p2.x, 'y': p2.y,
                    'credits': self.player_b.credits},
                'updates': self.updates})
        self.updates = []

    def role_distributor(self):
        yield DISRUPTOR_TEAM_A
        yield RUNNER_TEAM_A
        yield DISRUPTOR_TEAM_B
        yield RUNNER_TEAM_B

if __name__ == '__main__':
    ServerGame().run()
