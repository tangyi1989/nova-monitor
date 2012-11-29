
import json

class MongodbUtil():
    def get_connection(self):
        pass

class InstancePerfData():
    def save_data(self, inst_perf, timestamp):
        pass
    
    def get_data(self, start_timestamp, stop_timestamp):
        pass
    
    def handle_message(self, type, data, timestamp):
        inst_perf_list = data
        for inst_perf in inst_perf_list:
            self.save_data(inst_perf, timestamp)

class WleedManager():
    def __init__(self):
        pass
    
    def handle_data(self, data):
        msgs = json.loads(data)
        for msg in msgs:
            type = msg['type']
            data = msg['data']
            timestamp = msg['timestamp']
            self.dispatch_message(type, data, timestamp)
    
    def dispatch_message(self, type, data, timestamp):
        pass
