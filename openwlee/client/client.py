#*_* coding=utf8 *_*

"""
描述：没有分离的美感，只有简洁的代码，能用再说代码美丑。
"""

import time
from datetime import datetime
from openwlee.client.collect.collector import CollectorManager
from openwlee.client.collect.inst_collector import InstStatCollector

class Client:
    def __init__(self):
        self.collector_manager = CollectorManager()
        self.collector_manager.append_collector(InstStatCollector())
    
    def periodic_task(self):
        infos = self.collector_manager.render_infos()
        print infos
    
    def send(self):
        pass
    
    """A method for display vm info for people see"""
    def display(self):
        pass
    
if __name__ == "__main__":
    client = Client()
    while True:
        time.sleep(1)
        client.periodic_task()

