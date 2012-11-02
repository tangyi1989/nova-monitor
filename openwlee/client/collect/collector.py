#*_* coding=utf8 *_*

from openwlee import utils

import time
from datetime import datetime

#把此类写成单例模式或许会不错
class Collector():
    def __new__(cls):
        pass
    
    def __init__(self):
        self._tag = None
        
    def set_tag(self, tag):
        self._tag = tag
    
    def collect(self):
        return {}
    
class CollectorManager():
    def __init__(self):
        self._collectors = []
        
    def append_collector(self, collector):
        #Should check collector here
        self._collectors.append(collector)
    
    def render_infos(self):
        infos = dict()
        
        for collector in self._collectors:
            tag = collector._tag
            info = collector.collect()
            
            infos[tag] = info
            
        return infos
