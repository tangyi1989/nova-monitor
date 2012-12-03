#*_* coding=utf8 *_*

from openwlee import utils

import time
from datetime import datetime

class Monitor():
    def __new__(cls):
        pass
    
    def __init__(self):
        self._type = None
        self.monitor_date = None
        
    def set_type(self, type):
        self._type = type
        
    def get_monitor_date(self):
        if self.monitor_date:
            monitor_date = self.monitor_date
        else:
            monitor_date = utils.utc_now()
            
        return monitor_date
    
    def collect(self):
        return {}

class MonitorManager():
    def __init__(self):
        self._collectors = []
        
    def append(self, collector):
        #Should check collector here
        self._collectors.append(collector)
    
    """
    Return data like this:
    [{"type" : "xxx", "datetime" : "xxx", "data" : "xxx"}, ...]
    """
    def collect_data(self):
        data_list = []
        
        for collector in self._collectors:
            collect_dict = dict()
            
            info = collector.collect()
            collect_dict['data'] = info
            collect_dict['datetime'] = collector.get_monitor_date()
            collect_dict['type'] = collector._type
            
            data_list.append(collect_dict) 
            
        return data_list
