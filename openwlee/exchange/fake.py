
from openwlee.exchange import base

class FakeReceiver(base.Receiver):
    """ Fake, fake, fake. """
    pass

class FakeReporter(base.Reporter):
    """ FakeReporter fakes feed data to wleed instead, 
    for test wleed. """
    def __init__(self, *args, **kargs):
        from openwlee.wlee_daemon import WleeDaemonManager
        self.wleed_manager = WleeDaemonManager()
    
    def report(self, data):
        self.wleed_manager.handle_data(data)
        
Receiver = FakeReceiver        
Reporter = FakeReporter