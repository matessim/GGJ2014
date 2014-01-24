# Author : MM


# Class representing a (network) client for the server
class NetworkClient(object):
	def __init__(self, client_socket, client_host):
		self._host = client_host
		self._client_socket = client_socket


	@property
	def client_socket(self):
		return self._client_socket

	def __repr__(self):
		print self._host
		return "<Client %s:%d>" % (self._host[0], self._host[1])
