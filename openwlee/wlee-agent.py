#*_* coding=utf8 *_*

import time
import json
from datetime import datetime

from openwlee import utils
from openwlee.common.reporter import FakeReporter, DisplayReporter
from openwlee.monitor.monitor import MonitorManager
from openwlee.monitor.instance_monitor import InstancePerfMonitor

"""
Agent : collect data from this node, and report it to server
"""
class WleeAgentManager:
    def __init__(self):
        inst_perf_monitor = InstancePerfMonitor()
        
        self.hostname = utils.hostname()
        self.reporter = DisplayReporter()
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
            data['hostname'] = self.hostname
            
        if not data.has_key('timestamp'):
            data['timestamp'] = utils.utc_now()
            
        report_data = utils.json_dumps(data)
        self.reporter.report(report_data)
    
if __name__ == "__main__":
    agent = WleeAgentManager()
    while True:
        time.sleep(1)
        agent.report_monitor_data()
        agent.report_alive()