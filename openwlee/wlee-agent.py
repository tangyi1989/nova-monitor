
import time
import json
from datetime import datetime

from openwlee import utils
from openwlee import exchange
from openwlee.openstack.common import timeutils
from openwlee.openstack.common import jsonutils
from openwlee.monitor.monitor import MonitorManager
from openwlee.monitor.instance_monitor import InstancePerfMonitor

class WleeAgentManager:
    """
    Agent : collect data from this node, and report it to server
    """
    def __init__(self):
        inst_perf_monitor = InstancePerfMonitor()
        
        self.hostname = utils.hostname()
        self.reporter = exchange.Reporter()
        self.monitor_manager = MonitorManager()
        self.monitor_manager.append(inst_perf_monitor)
    
    def report_monitor_data(self):
        data_list = self.monitor_manager.collect_data()
        for data in data_list:
            self.report(data)
    
    def report_alive(self):
        heartbeat = dict(type='heartbeat', data = {})
        self.report(heartbeat)
        
    def report(self, data):
        if not data.has_key('hostname'):
            data['host'] = self.hostname
            
        if not data.has_key('datetime'):
            data['datetime'] = timeutils.utcnow()
            
        report_data = jsonutils.dumps(data)
        self.reporter.report(report_data)
        
    def start(self):
        while True:
            time.sleep(1)
            self.report_monitor_data()
            self.report_alive()
            
if __name__ == "__main__":
    agent = WleeAgentManager()
    agent.start()