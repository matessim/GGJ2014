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

import socket
import threading
import time
import select

from client_connection import *

pg.init()

# Listen on all connections
SERVER_IP   = '0.0.0.0'
SERVER_PORT = 1337
SERVER_ADDR = (SERVER_IP, SERVER_PORT)
MAX_CLIENTS = 4

class ServerGame(object):
    def __init__(self):
        self.player_a = Player()
        self.player_b = Player()
        self.world = World(WIDTH/T_P, HEIGHT/T_P)
        self.clients = []
        self.updates = []

    def run(self):
        self.connect_players()
        while True:
            CLOCK.tick(FPS)
            self.get_actions()
            self.player_a.update(self.world)
            self.player_b.update(self.world)
            self.update_clients()
        

    def connect_players(self):
        role_giver = self.role_distributor()
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(SERVER_ADDR)
        sock.listen(MAX_CLIENTS)
        while len(self.clients) < MAX_CLIENTS:
            host, endpoint = sock.accept()
            # TODO: Change 0 to role
            new_client = GameClient(host, endpoint, role_giver.next())
            print "Accepted new client:", repr(new_client)
            self.clients.append(new_client)

    def get_actions(self):
        clients_with_actions = select.select(self.clients, [], [], 0)
        for client in clients_with_actions[0]:
            for event in client.get_events():
                try:
                    if event['type'] == MOVE:
                        self.handle_move(client, event)
                    elif event['type'] == ADD_ITEM:
                        self.handle_add_item(client, event)
                except Exception as e:
                    print "Error handling", event, "from", client
                    raise e

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
        if client.role != DISRUPTOR_TEAM_A and client.role != DISRUPTOR_TEAM_B:
            return
        x = event['x']
        y = event['y']
        self.world.add_tile(x, y)
        self.updates.append((x,y))

    def update_clients(self):
        for client in self.clients:
            client.send_data({'player_one': {'x': self.player_a.rect.x, 'y': self.player_a.rect.y},
                'player_two' : {'x': self.player_b.rect.x, 'y': self.player_b.rect.y}, 'updates': self.updates})
        self.updates = []

    def role_distributor(self):
        yield DISRUPTOR_TEAM_A
        yield RUNNER_TEAM_A
        yield DISRUPTOR_TEAM_B
        yield RUNNER_TEAM_A


if __name__ == '__main__':
    ServerGame().run()
