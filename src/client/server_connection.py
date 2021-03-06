import sys, os
__file_dir__ = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(__file_dir__, '..')))

from common.connection import Connection
from common.consts import *

import time

class ServerConnection(Connection):
    def __init__(self, server_socket):
        self._socket = server_socket

    def __repr__(self):
        return "<Server>"

    def wait_for_role(self):
        while True:
            begin_message = self.get_data()
            for m in begin_message:
                if m['type'] == START_GAME:
                    return (m['role'], m['spawn_a'], m['spawn_b'])
                else:
                    raise Exception()
            time.sleep(0.25)

    def move(self, pressed, direction):
        self.send_data({'type': MOVE, 'direction': direction,
            'pressed': pressed})

    def add_tile(self, x, y, t):
        self.send_data({'type': ADD_ITEM, 'x': x, 'y': y, 't': t})

    def get_update(self, players, world):
        player_a, player_b = players
        for state in self.get_data():
            if state.get('type', None) == END_GAME:
                return (END_GAME, state['wins_a'], state['wins_b'], state['spawn_a'], state['spawn_b'])
            else:
                player_a.rect.x  = state['player_one']['x']
                player_a.rect.y  = state['player_one']['y']
                player_a.credits = state['player_one']['credits']
                player_b.rect.x  = state['player_two']['x']
                player_b.rect.y  = state['player_two']['y']
                player_b.credits = state['player_two']['credits']
                for x, y, t in state['updates']:
                    world.add_tile(x, y, t)
