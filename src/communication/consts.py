class CommandCode(object):
    # Messages Server -> Client

    # Data that needs to be sent at game start is what kind of player the client is
    START_GAME      = 1
    END_GAME        = 2
    RESTART_GAME    = 3

    # Messages Client -> Server

    MOVE_REQUEST    = 1001
    MAP_UPDATE      = 1002


# Class with codes for each unique Player type
class PlayerCodes(object):
    DISRUPTOR_TEAM_A    = 0
    RUNNER_TEAM_A       = 1
    DISRUPTOR_TEAM_B    = 2
    RUNNER_TEAMB        = 3


