import time
from openwlee.openstack.common import timeutils
from openwlee.openstack.common import jsonutils
from openwlee.openstack.common import log as logging

LOG = logging.getLogger('openwlee.wlee_agent')

class Task(object):
    """ The base class of Task """
    def __init__(self, manager):
        self.manager = manager
        self.host = self.manager.hostname
        self.initialize()
        
    def initialize(self):
        pass
    
    def start(self):
        task_name = self.__class__
        LOG.info('Start executing task : %s' % task_name) 
        start_time = time.time()
        try:
            self.execute()
        except Exception as e:
            # Nothing todo here or send a report to server?
            raise e
        LOG.info('Complete task %s , cost %fms' % (task_name, time.time() - start_time))
    
    def execute(self):
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