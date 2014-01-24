# Author : MM
# Purpose: Run the game server

import sys
import socket
import threading

from client import *

# Listen on all connections
SERVER_IP   = '0.0.0.0'
SERVER_PORT = 1337
SERVER_ADDR = (SERVER_IP, SERVER_PORT)

MAX_BACKLOG = 4

g_connections = []

def main():
	connection_thread = threading.Thread(target=connection_loop)
	print "Starting server accept thread"
	connection_thread.run()


def connection_loop():
	sock = socket.socket()
	sock.bind(SERVER_ADDR)
	sock.listen(MAX_BACKLOG)
	while True:
		host, endpoint = sock.accept()
		new_client = NetworkClient(host, endpoint)
		print "Accepted new client:", repr(new_client)
		g_connections.append(new_client)

if __name__ == '__main__':
	sys.exit(main())