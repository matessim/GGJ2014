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
        self.player = Player()
        self.world = World(WIDTH/T_P, HEIGHT/T_P)
        self.clients = []
        self.updates = []

    def run(self):
        self.connect_players()
        while True:
            CLOCK.tick(FPS)
            self.get_actions()
            self.player.update(self.world)
            self.update_clients()

    def connect_players(self):
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(SERVER_ADDR)
        sock.listen(MAX_CLIENTS)
        while len(self.clients) < MAX_CLIENTS:
            host, endpoint = sock.accept()
            # TODO: Change 0 to role
            new_client = ClientConnection(host, endpoint, 0)
            print "Accepted new client:", repr(new_client)
            self.clients.append(new_client)

    def get_actions(self):
        clients_with_actions = select.select(self.clients, [], [], 0)
        for client in clients_with_actions[0]:
            for event in client.get_data():
                try:
                    if event['type'] == MOVE:
                        self.handle_move(client, event)
                    elif event['type'] == ADD_ITEM:
                        self.handle_add_item(client, event)
                except Exception as e:
                    print "Error handling", event, "from", client
                    raise e

    def handle_move(self, client, event):
        if event['direction'] == LEFT:
            self.player.walking_left = event['pressed']
        elif event['direction'] == RIGHT:
            self.player.walking_right = event['pressed']
        elif event['direction'] == JUMP:
            if event['pressed'] and self.player.on_ground(self.world):
                self.player.jump()

    def handle_add_item(self, client, event):
        x = event['x']
        y = event['y']
        self.world.add_tile(x, y)
        self.updates.append((x,y))

    def update_clients(self):
        player_rect = self.player.rect
        for client in self.clients:
            client.send_data({'player': {'x': player_rect.x, 'y': player_rect.y},
                'updates': self.updates})
        self.updates = []

if __name__ == '__main__':
    ServerGame().run()
