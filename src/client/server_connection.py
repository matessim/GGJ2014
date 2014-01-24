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
        self.send_data({'type': MOVE, 'direction': direction,
            'pressed': pressed})

    def add_tile(self, x, y):
        self.send_data({'type': ADD_ITEM, 'x': x, 'y': y})

    def get_update(self, player, world):
        for state in self.get_data():
            player.rect.x = state['player']['x']
            player.rect.y = state['player']['y']
            for x, y in state['updates']:
                world.add_tile(x,y)
