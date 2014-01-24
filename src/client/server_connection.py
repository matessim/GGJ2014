import sys, os
__file_dir__ = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(__file_dir__, '..')))

from common.connection import Connection
from common.consts import *

class ServerConnection(Connection):
    def __init__(self, server_socket):
        self._socket = server_socket

    def __repr__(self):
        return "<Server>"

    def move(self, pressed, direction):
        self.send_data({'type': MOVE, 'direction': direction, 'pressed': pressed})

    def add_tile(self, x, y):
        self.send_data({'type': ADD_ITEM, 'x': x, 'y': y})

    def get_update(self, players, world):
        player_a, player_b = players
        for event in self.get_events():
            player_a.rect.x = event['player_one']['x']
            player_a.rect.y = event['player_one']['y']
            player_b.rect.x = event['player_two']['x']
            player_b.rect.y = event['player_two']['y']
            for x, y in event['updates']:
                world.add_tile(x,y)
