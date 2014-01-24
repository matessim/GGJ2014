import pygame as pg

# Enum colors:
GREEN = pg.Color(0, 255, 0)
WHITE = pg.Color(255, 255, 255)
RED   = pg.Color(255, 0, 0)
BLACK = pg.Color(0, 0, 0)

# Enum roles:
MOVER  = 0
DRAWER = 1

# Enum directions
LEFT  = 0
RIGHT = 1
JUMP  = 2

# Size of screen and tiles
SIZE = WIDTH, HEIGHT = 640, 480
T_P = 10

CLOCK = pg.time.Clock()

FPS     = 60
GRAVITY = 1

# Messages Server -> Client

# Data that needs to be sent at game start is what kind of player the client is
START_GAME   = 1
END_GAME     = 2
RESTART_GAME = 3

# Messages Client -> Server

MOVE     = 1001
ADD_ITEM = 1002

# Enum with codes for each unique Player type
DISRUPTOR_TEAM_A = 0
RUNNER_TEAM_A    = 1
DISRUPTOR_TEAM_B = 2
RUNNER_TEAM_B    = 3

LENGTH_FORMAT = "<I"
UINT_LEN_BYTES = 4

# Listen on all connections
SERVER_IP   = '0.0.0.0'
SERVER_PORT = 1337
SERVER_ADDR = (SERVER_IP, SERVER_PORT)
MAX_CLIENTS = 1
