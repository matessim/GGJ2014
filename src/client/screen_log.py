
class ScreenLog(object):
    def __init__(self, max_backlog):
        self._log = []
        self.max_backlog = max_backlog

    def log(self, msg):
        self._log.append(msg)
        if len(self._log) > self.max_backlog:
            self._log = self._log[1:]

    def get_logs(self):
        return self._log

