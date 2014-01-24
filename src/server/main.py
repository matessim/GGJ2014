# Author : MM
# Purpose: Run the game server

import sys
import socket
import threading
import time

from client import *

# Listen on all connections
SERVER_IP   = '0.0.0.0'
SERVER_PORT = 1337
SERVER_ADDR = (SERVER_IP, SERVER_PORT)

MAX_CLIENTS = 4

g_connections = []

g_server_enabled = False

def main():
    connection_thread = threading.Thread(target=connection_loop)
    connection_status = threading.Thread(target=sample_connection_count)
    print "Starting server accept thread"
    connection_thread.start()
    connection_status.start()
    connect_players()
    print "4 Players connected! game loop!"
    g_server_enabled = True
    game_loop()

def game_loop():
    while g_server_enabled:
        tick_players(g_connections)
        
def tick_players(players):
    for player in players:
        player.tick()

def sample_connection_count():
    while len(g_connections) < MAX_CLIENTS:
        print "Connected clients: " + str(len(g_connections)) + ", waiting for further connections..."
        time.sleep(10)

def connect_players():
    while len(g_connections) < MAX_CLIENTS:
        time.sleep(0.25)    
    return True


def connection_loop():
    sock = socket.socket()
    sock.bind(SERVER_ADDR)
    sock.listen(MAX_CLIENTS)
    while True:
        host, endpoint = sock.accept()
        new_client = GameClient(host, endpoint)
        print "Accepted new client:", repr(new_client)
        g_connections.append(new_client)

if __name__ == '__main__':
    sys.exit(main())