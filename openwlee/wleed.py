
from openwlee import utils
from openwlee.db import base as db_base
from openwlee.openstack.common import jsonutils
from openwlee.openstack.common import timeutils

class WleedDispatcher():
    """
    Wlee Dispatcher : dispatch message
    """
    def __init__(self, manager):
        self.manager = manager
        self.db = manager.db
        
    def dispatch(self, host, type, data, datetime):
        if type == "instance_perf":
            self.handle_instance_perf_data(data, datetime)
    
    def handle_instance_perf_data(self, inst_perf_list, datetime):
        for inst_perf in inst_perf_list:
            inst_perf['timestamp']= utils.datetime_to_timestamp(datetime)
            self.db.save_instance_perf_data(inst_perf)
        
class WleedManager(db_base.Base):
    """
    Wlee Deamon : used to collect info from agent and saved to database.
    """
    def __init__(self):
        super(WleedManager, self).__init__()
        self.receiver = None
        self.dispatcher = WleedDispatcher(self)
    
    def handle_data(self, data):
        msg = jsonutils.loads(data)
        
        host = msg['host']
        type = msg['type']
        data = msg['data']
        datetime = timeutils.parse_strtime(msg['datetime'])
        self.dispatcher.dispatch(host, type, data, datetime)
    
    def start(self):
        pass