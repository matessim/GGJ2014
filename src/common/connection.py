import json
import pygame as pg
import select
import struct
import sys
from consts import *

# Class representing a (network) client for the server
class Connection(object):
    def __init__(self, client_socket):
        self._socket = client_socket

    def send_data(self, obj):
        data = json.dumps(obj)
        return self._send_frame(data)

    def get_data(self):
        """
        This function returns an iterator of parsed data that has
        been received on the socket until the call to next.
        """
        while select.select([self], [], [], 0)[0]:
            yield json.loads(self._get_frame())

    def _get_frame(self):
        try:
            read_len = struct.unpack(LENGTH_FORMAT, self._socket.recv(UINT_LEN_BYTES))[0]
            data = ""
            while len(data) < read_len:
                data += self._socket.recv(read_len - len(data))
            return data
        except:
            # The other side hung up. Let's just quit.
            pg.quit()
            sys.exit()

    def _send_frame(self, data):
        try:
            length = struct.pack(LENGTH_FORMAT, len(data))
            self._socket.send(length + data)
        except:
            return False
        return True

    # So we can select on the object
    def fileno(self):
        return self._socket.fileno()

