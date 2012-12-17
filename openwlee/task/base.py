from openwlee.openstack.common import timeutils
from openwlee.openstack.common import jsonutils

class Task(object):
    """ The base class of Task """
    def __init__(self, manager):
        self.manager = manager
        self.host = self.manager.hostname
        self.initialize()
        
    def initialize(self):
        pass
    
    def execute(self, *args, **kargs):
        """ Execution body of the task. """
        raise NotImplementedError("This class should implent in subclass")
    
    def report(self, type, data, report_time=None):
        """ Report data to wlee daemon. """
        if report_time == None:
            report_time = timeutils.utcnow()
            
        report_data = {'host' : self.host, 
                       'datetime' : report_time, 
                       'type' : type, 
                       'data' : data}
        
        self.manager.reporter.report(jsonutils.dumps(report_data))