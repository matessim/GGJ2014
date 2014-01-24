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

    def wait_begin(self):
        while True:
            begin_message = self.get_data()
            for m in begin_message:
                if m['type'] == START_GAME:
                    self._role = m['role']
                    return

    def move(self, pressed, direction):
        self.send_data({'type': MOVE, 'direction': direction,
            'pressed': pressed})

    def add_tile(self, x, y, t):
        self.send_data({'type': ADD_ITEM, 'x': x, 'y': y, 't': t})

    def get_update(self, players, world):
        player_a, player_b = players
        for state in self.get_data():
            player_a.rect.x = state['player_one']['x']
            player_a.rect.y = state['player_one']['y']
            player_b.rect.x = state['player_two']['x']
            player_b.rect.y = state['player_two']['y']
            for x, y, t in state['updates']:
                world.add_tile(x, y, t)
