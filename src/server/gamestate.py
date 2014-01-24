
def GameState(object):
    def __init__(self, clients):
        self._clients = clients
        self._running = True


    # Is the game still running?
    def running(self):
        return self._running

    # Perform server tick
    def tick(self):
        for client in clients:
            clent.tick()

        # Check if the game is still running/over/stuff like that.
        # TODO: Update all players with the new game state.

