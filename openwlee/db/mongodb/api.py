
import pymongo

from openwlee import utils as openwlee_utils
from openwlee.db.mongodb import utils
from openwlee.db.mongodb.utils import ensure_collction, get_database

INST_RECENTLY_PERF_SIZE = 1000 * 24 * 60 * 6
ensure_collction('instance_recently_perf', db_name = 'wlee_db',
                 indexes = [('name', pymongo.ASCENDING), ('timestamp', pymongo.DESCENDING)], 
                 options = {"capped" : True, "size" : INST_RECENTLY_PERF_SIZE, 
                            "max" : INST_RECENTLY_PERF_SIZE})
ensure_collction('instance_statistic', db_name = 'wlee_db')
ensure_collction('agent_status', db_name = 'wlee_db')

def update_agent_status(host, datetime):
    db = get_database()
    return db.agent_status.update({'host' : host}, 
                                  {'$set' : {'last_updated_at' : datetime}}, True)
    
def save_instance_perf_data(perf_data):
    db = get_database()
    perf_recently = db.instance_perf_recently
    return perf_recently.insert(perf_data)

@utils.wrap_mongo_query_result
def get_instance_recently_perf(instance_name, seconds):
    db = get_database()
    perf_recently = db.instance_perf_recently
    
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

def update_instance_statistic_data(statistic_data, datetime):
    db = get_database()
    statistic_data['last_updated_at'] = datetime
    return db.instance_statistic.update({'host' : statistic_data['name']}, 
                                        {'$set' : statistic_data}, True)

@utils.wrap_mongo_query_result
def get_instance_statistic(instance_name):
    db = get_database()
    return db.instance_statistic.find_one({'name' : instance_name})
