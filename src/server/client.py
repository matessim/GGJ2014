# Author : MM

from actions import *

# Class representing a (network) client for the server
class GameClient(object):
	def __init__(self, client_socket, client_host):
		self._host = client_host
		self._client_socket = client_socket
		self._next_action = doNothing()

	@property
	def client_socket(self):
		return self._client_socket

	# Perform the action in the next action queue for the player
	def tick(self):
		pass

	def __repr__(self):
		return "<Client %s:%d>" % (self._host[0], self._host[1])

