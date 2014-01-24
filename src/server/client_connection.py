import sys, os
__file_dir__ = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(__file_dir__, '..')))

from common.connection import Connection

class GameClient(Connection):
    def __init__(self, client_socket, client_host, role):
        self._host = client_host
        self._socket = client_socket
        self._role = role
 	
    def __repr__(self):
        return "<Client %s:%d>" % (self._host[0], self._host[1])

    @property
    def role(self):
    	return self._role

