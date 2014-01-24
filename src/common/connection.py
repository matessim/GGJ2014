import select
import json
import struct
from consts import *

# Class representing a (network) client for the server
class Connection(object):
    def __init__(self, client_socket):
        self._socket = client_socket

    def send_data(self, obj):
        data = json.dumps(obj)
        return self._send_frame(data)

    def get_events(self):
        events = []
        while select.select([self], [], [], 0)[0]:
            events.append(json.loads(self._get_frame()))
        return events

    def _get_frame(self):
        read_len = struct.unpack(LENGTH_FORMAT, self._socket.recv(UINT_LEN_BYTES))[0]
        data = ""
        while len(data) < read_len:
            data += self._socket.recv(read_len - len(data))
        return data

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

