# Author : MM


# Class representing a (network) client for the server
class NetworkClient(obejct):
	def __init__(self, client_host, client_socket):
		self._host = client_host
		self._client_socket = client_socket


	@property
	def client_socket(self):
		return self._client_socket


