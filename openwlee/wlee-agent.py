#*_* coding=utf8 *_*

import time
from datetime import datetime
from openwlee.collect.collector import CollectorManager
from openwlee.collect.instance import InstanceStatCollector

"""
Agent : collect data from this node, and send it to server
"""
class WleeAgentManager:
    
    def __init__(self):
        instance_collector = InstanceStatCollector()
        self.collector_manager = CollectorManager()
        self.collector_manager.append(instance_collector)
    
    def periodic_task(self):
        data = self.collector_manager.render_monitor_data()
        self.display(data['vm_perf_data'])
        self.send()
    
    def send(self):
        pass
    
    """A method for display vm info for people see"""
    def display(self, vm_data):
        import pprint
        pprint.pprint(vm_data)
    
if __name__ == "__main__":
    client = WleeAgentManager()
    while True:
        time.sleep(1)
        client.periodic_task()