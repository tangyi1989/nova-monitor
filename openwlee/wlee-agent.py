#*_* coding=utf8 *_*

import time
from datetime import datetime
from openwlee.collect.collector import CollectorManager
from openwlee.collect.instance import InstancePerfCollector

"""
Agent : collect data from this node, and send it to server
"""
class WleeAgentManager:
    
    def __init__(self):
        inst_perf_collector = InstancePerfCollector()
        
        self.collector_manager = CollectorManager()
        self.collector_manager.append(inst_perf_collector)
    
    def periodic_task(self):
        data = self.collector_manager.collect_data()
        self.display(data)
        self.send()
    
    def send(self):
        pass
    
    """A method for display vm info for people see"""
    def display(self, data):
        import pprint
        pprint.pprint(data)
    
if __name__ == "__main__":
    client = WleeAgentManager()
    while True:
        time.sleep(1)
        client.periodic_task()