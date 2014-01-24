
class ScreenLog(object):
    def __init__(self, max_backlog):
        self._log = ""
        self._max_backlog = max_backlog

    def log(self, msg):
        self._log += msg.replace('\n', ' ') + '\n'
        splitted = self._log.split('\n')
        if len(splitted) > self._max_backlog:
            self._log = '\n'.join(splitted[:self._max_backlog])

    def get_logs(self):
        return self._log.split('\n')

