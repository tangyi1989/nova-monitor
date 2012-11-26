#*_* coding=utf8 *_*

from openwlee import utils

import time
from datetime import datetime

class Collector():
    def __new__(cls):
        pass
    
    def __init__(self):
        self._type = None
        self.timestamp = None
        
    def set_type(self, type):
        self._type = type
        
    def get_timestamp(self):
        if self.timestamp:
            timestamp = self.timestamp
        else:
            timestamp = utils.utc_now()
            
        return timestamp
    
    def collect(self):
        return {}

class CollectorManager():
    def __init__(self):
        self._collectors = []
        
    def append(self, collector):
        #Should check collector here
        self._collectors.append(collector)
    
    """
    Return data like this:
    [{"type" : "xxx", "timestamp" : "xxx", "data" : "xxx"}, ...]
    """
    def collect_data(self):
        data_list = []
        
        for collector in self._collectors:
            collect_dict = dict()
            
            info = collector.collect()
            collect_dict['data'] = info
            collect_dict['timestamp'] = collector.get_timestamp()
            collect_dict['type'] = collector._type
            
            data_list.append(collect_dict) 
            
        return data_list
