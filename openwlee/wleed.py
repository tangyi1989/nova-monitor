
import pymongo
from openwlee import utils

class MongoUtil():
    def __init__(self, *args, **kargs):
        pass
                   
    def get_connection(self):
         return pymongo.Connection(host='localhost', port=27017)

class WleeMongoBackend():
    def __init__(self):
        self.mongo_util = MongoUtil()
        self.initiliaze_database()
    
    def initiliaze_database(self):
        def create_col_if_not_exist(db, col_name, indexes=[], options=None):
            if col_name not in db.collection_names():
                db.create_collection(col_name, options=options)
                coll = db[col_name]
                for index in indexes:
                    coll.ensure_index(index)
    
        db = self.get_database()
        create_col_if_not_exist(db, 'instance_perf_recently', ['name', "timestamp"])
        
    def get_database(self):
        conn = self.mongo_util.get_connection()
        return conn.wlee_db
     
"""
If I use MongoUtil directly, it would be result high degree of coupling.
I would refactor these code anyway.
"""
class InstancePerfData():
    def __init__(self):
        self.mongo_backend = WleeMongoBackend()
        self.mongo_db = self.mongo_backend.get_database()
    
    def save_instance_perf(self, inst_perf):
        perf_recently = self.mongo_db.vm_perf_recently
        perf_recently.insert(inst_perf)
    
    def get_most_recently_perf(self, instance_name, seconds = 60):
        perf_recently = self.mongo_db.vm_perf_recently
        
        max_timestamp_cursor = perf_recently.find({'name' : instance_name}).\
                    sort([('timestamp', pymongo.DESCENDING)]).limit(1)
        
        max_timestamp_list = [i for i in max_timestamp_cursor]
        if len(max_timestamp_list) == 0:
            return []
        
        max_timestamp = max_timestamp_list[0]['timestamp'] + 1
        min_timestamp = max_timestamp - seconds
        
        recently_perf_cursor = perf_recently.find({'name' : instance_name, 
                'timestamp' : {"$lt" : max_timestamp, "$gt" : min_timestamp}})
        recently_perf_list = [i for i in recently_perf_cursor]
        
        return recently_perf_list

    
    def handle_message(self, type, data, datetime):
        inst_perf_list = data
        for inst_perf in inst_perf_list:
            timestamp = utils.datetime_to_timestamp(datetime)
            inst_perf['timestamp'] = timestamp
            
            self.save_instance_perf(inst_perf)

class WleedManager():
    def __init__(self):
        self.instance_perf_manager = InstancePerfData()
    
    def handle_data(self, data):
        msg = utils.json_loads(data)
        
        type = msg['type']
        data = msg['data']
        datetime = utils.parse_strtime(msg['datetime'])
        self.dispatch_message(type, data, datetime)
    
    def dispatch_message(self, type, data, datetime):
        if type == "instance_perf":
            self.instance_perf_manager.handle_message(type, data, datetime)
        #do nothing else now.

if __name__=="__main__":
    inst_perf = InstancePerfData()
    print inst_perf.get_most_recently_perf('instance-0000023a')