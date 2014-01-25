import pygame as pg
import os

# Enum colors:
WHITE  = pg.Color(255, 255, 255)
RED    = pg.Color(255, 0, 0)
GREEN  = pg.Color(0, 255, 0)
BLUE   = pg.Color(0, 0, 255)
BLACK  = pg.Color(0, 0, 0)
YELLOW = pg.Color(255, 255, 0)

# Enum roles:
MOVER  = 0
DRAWER = 1

# Enum directions
LEFT  = 0
RIGHT = 1
JUMP  = 2

# Size of screen and tiles
SIZE = WIDTH, HEIGHT = 640, 480
WORLD_WIDTH, WORLD_HEIGHT = 2000, 1200
T_P = 10

CLOCK = pg.time.Clock()

FPS               = 60
FRAMES_PER_CREDIT = 2 * FPS
GRAVITY           = 1

# Messages Server -> Client

# Data that needs to be sent at game start is what kind of player the client is
START_GAME   = 1
END_GAME     = 2
RESTART_GAME = 3

# Messages Client -> Server

MOVE     = 1001
ADD_ITEM = 1002
SUICIDE  = 1003
DEVMODE  = 1004

# Player update return values

WIN = 0
LOSS = 0

# Enum with codes for each unique Player type
DISRUPTOR_TEAM_A = 0
RUNNER_TEAM_A    = 1
DISRUPTOR_TEAM_B = 2
RUNNER_TEAM_B    = 3

PLAYER_DESC = {DISRUPTOR_TEAM_B : "Team B Disruptor",
			   DISRUPTOR_TEAM_A : "Team A Disruptor",
			   RUNNER_TEAM_B : "Team B Runner",
			   RUNNER_TEAM_A : "Team A Runner"}

LENGTH_FORMAT = "<I"
UINT_LEN_BYTES = 4

# Listen on all connections
SERVER_IP   = '0.0.0.0'
SERVER_PORT = 1337
SERVER_ADDR = (SERVER_IP, SERVER_PORT)
MAX_CLIENTS = 4

CAMERA_SPEED = T_P

END_GAME = 0

SAVE_FILE_FORMAT = r".." + os.sep +'good-levels' + os.sep + 'savegame'

