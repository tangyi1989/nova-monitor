
"""
Reporter just send report_data to server and I think reporter 
should read configuration by itself. 
"""
class Reporter():
    def __init__(self, *args, **kargs):
        pass
    
    def report(self, data):
        pass

"""
Zeromq Reporter report data by zeromq.
"""
class ZeromqReporter(Reporter):
    pass

"""
Http Reporter
"""
class HttpReporter(Reporter):
    pass

"""
FakeReporter fakes feed data to wleed instead, for test wleed.
"""
class FakeReporter(Reporter):
    def __init__(self, *args, **kargs):
        from openwlee.wleed import WleedManager
        self.wleed_manager = WleedManager()
    
    def report(self, data):
        self.wleed_manager.handle_data(data)

"""
For debug, print data on screen.
"""
class DisplayReporter(Reporter):
    def report(self, data):
        print data