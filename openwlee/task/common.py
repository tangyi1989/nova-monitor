
from openwlee.task import base

class HeartbeatTask(base.Task):
    def execute(self):
        self.report('heartbeat', None)
