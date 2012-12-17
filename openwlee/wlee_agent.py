
import eventlet
import datetime

from openwlee import task
from openwlee import exchange
from openwlee.openstack.common import log as logging
from openwlee.openstack.common import timeutils
from openwlee.openstack.common import cfg

LOG = logging.getLogger('openwlee.wlee_agent')

class WleeAgentManager:
    """ Wlee Agent :  """
    def __init__(self):
        self.reporter = exchange.Reporter()
        self.hostname = cfg.CONF.host
        self._tasks = {}
        self._schedulers = []
        self.green_pool = eventlet.GreenPool()
        self.running = False
        self.setup_tasks()
    
    def setup_tasks(self):
        self.add_agent_task(task.common.HeartbeatTask, 5)
        self.add_agent_task(task.instance.InstancePerformanceTask, 10)
    
    def add_agent_task(self, task_cls, interval=0):
        """ Add a agent task that would run every interval seconds, 
        if interval is zero, task only execute once. """
        
        self._tasks[task_cls] = interval
        if self.running:
            self.add_agent_task(task_cls, interval)
        
    def _add_to_scheduler(self, task_cls, interval):
        task = task_cls(self)
        task_inst = {"task" : task, 
                     "last_schedule_time" : None, 
                     "interval" : interval}
        
        self._schedulers.append(task_inst)
    
    def run(self):
        if self.running:
            raise exception.WleeException("Can't run agent twice.")
        
        self.running = True
        for task_cls, interval in self._tasks.iteritems():
            self._add_to_scheduler(task_cls, interval)
        
        self.green_pool.spawn(self._task_loop)
        self.green_pool.waitall()
    
    def _task_loop(self):
        while self.running:
            current_time = timeutils.utcnow()
            
            for task_inst in self._schedulers:
                if task_inst['last_schedule_time'] == None:
                    next_schedule_time = current_time
                else:
                    next_schedule_time = task_inst['last_schedule_time'] \
                                            + datetime.timedelta(seconds = task_inst['interval'])
                
                if next_schedule_time > current_time:
                    continue
                
                self.green_pool.spawn(task_inst['task'].execute)
                task_inst['last_schedule_time'] = current_time
                
                if task_inst['interval'] <= 0:
                    self._schedulers.remove(task_inst)
            
            eventlet.sleep(0.5)
    
    def stop(self):
        self.running = False
        
def tests():
    pass

if __name__ == "__main__":
    tests()    