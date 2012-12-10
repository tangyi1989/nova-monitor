
from openwlee.exchange import base

class DisplayRecevier(base.Receiver):
    """ This would be never implement. """
    pass

class DisplayReporter(base.Reporter):
    """ For debug, print data on screen. """
    def report(self, data):
        print data

Receiver = DisplayRecevier        
Reporter = DisplayReporter
