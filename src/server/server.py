#!/usr/bin/python

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
import json

from client_connection import *

pg.init()

class ServerGame(object):
    def __init__(self):
        a_spawn = (randrange(T_P, WORLD_WIDTH-4*T_P),
                    randrange((WORLD_HEIGHT / 2) + 2*T_P, WORLD_HEIGHT - 8*T_P))
        b_spawn = (randrange(T_P, WORLD_WIDTH-4*T_P),
                    randrange((WORLD_HEIGHT / 2) + 2*T_P, WORLD_HEIGHT - 8*T_P))
        self.player_a = Player(BLACK, a_spawn)
        self.player_b = Player(BLACK, b_spawn)
        self.world = World(WORLD_WIDTH/T_P, WORLD_HEIGHT/T_P, True)
        self.updates = self.world.randomize_start()
        self.clients = []
        self.wins_a = 0
        self.wins_b = 0
        self.run_lock = threading.Lock()
        self.repl = threading.Thread(target=self.repl_thread)
        self.repl.daemon = True

    def repl_thread(self):
        while True:
            result = raw_input(">>>")
            letter = result.split(' ')[0].lower()
            if letter == 'h':
                print "h - help, l - load (map), r - restart, g - available savegames"
            if letter == 'l':
                with self.run_lock:
                    self.load_level(result.split(' ')[1])
            if letter == 'r':
                with self.run_lock:
                    self.restart()
            if letter == 'g':
                print ' '.join([x for x in os.listdir('..' + os.sep + 'good-levels') if 'savegame' in x])

    def load_level(self, level_location):
        data = json.loads(open('..' + os.sep + 'good-levels' + os.sep + level_location, 'rb').read().decode('zlib'))
        spawn_a = data[0]
        spawn_b = data[1]
        tiles = data[2:]
        for client in self.clients:
            client.send_data({'type': END_GAME, 'wins_a': self.wins_a, 'wins_b': self.wins_b, 'spawn_a': spawn_a, 'spawn_b': spawn_b})
        # clean world
        self.player_a = Player(RED, spawn_a)
        self.player_b = Player(BLUE, spawn_b)
        self.world.empty()
        self.updates = []
        for tile in tiles:
            x, y, t = tile
            self.world.add_tile(x, y, t)
            self.updates.append((x, y, t))


    def run(self):
        self.connect_players()
        self.start_game()
        self.update_clients()
        self.repl.start()
        i = 0
        while True:
            with self.run_lock:
                CLOCK.tick(FPS)
                self.get_actions()
                a_ret = self.player_a.update(self.world)
                if a_ret == WIN:
                    self.wins_a += 1
                    self.restart()
                b_ret = self.player_b.update(self.world)
                if b_ret == WIN:
                    self.wins_b += 1
                    self.restart()
                self.update_clients()
                i += 1
                if i % FRAMES_PER_CREDIT == 0:
                    i = 0
                    self.player_a.credits += 1
                    self.player_b.credits += 1

    def restart(self):
        spawn_a = (randrange(T_P, WORLD_WIDTH-4*T_P),
                    randrange((WORLD_HEIGHT / 2) + 2*T_P, WORLD_HEIGHT - 4*T_P))
        spawn_b = (randrange(T_P, WORLD_WIDTH-4*T_P),
                    randrange((WORLD_HEIGHT / 2) + 2*T_P, WORLD_HEIGHT - 4*T_P))
        for client in self.clients:
            client.send_data({'type': END_GAME, 'wins_a': self.wins_a, 'wins_b': self.wins_b, 'spawn_a': spawn_a, 'spawn_b': spawn_b})
        self.player_a = Player(RED, spawn_a)
        self.player_b = Player(BLUE, spawn_b)
        self.world.empty()
        self.updates = self.world.randomize_start()

    def start_game(self):
        for client in self.clients:
            client.send_data({'type' : START_GAME, 'role' : client.role, 'spawn_a': self.player_a.spawn_point, 'spawn_b': self.player_b.spawn_point})

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
                elif event['type'] == DEVMODE:
                    if client.role == DISRUPTOR_TEAM_A:
                        self.player_a.toggle_developer()
                    elif client.role == DISRUPTOR_TEAM_B:
                        self.player_b.toggle_developer()


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
        if tile_type.cost > player.credits and not(player.is_developer()):
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
            if not(player.is_developer()):
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
