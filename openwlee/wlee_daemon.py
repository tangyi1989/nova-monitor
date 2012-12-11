
from openwlee import utils
from openwlee import exchange
from openwlee.db import base as db_base
from openwlee.openstack.common import jsonutils
from openwlee.openstack.common import timeutils
from openwlee.openstack.common import log as logging

LOG = logging.getLogger("openwlee.wlee_daemon")

class EventDispatcher():
    """
    Event Dispatcher : dispatch message
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
        
class WleeDaemonManager(db_base.Base):
    """
    Wlee Deamon : used to collect info from agent and saved to database.
    """
    def __init__(self):
        super(WleeDaemonManager, self).__init__()
        self.receiver = exchange.Receiver(self.handle_data)
        self.dispatcher = EventDispatcher(self)
    
    def handle_data(self, data):
        try:
            msg = jsonutils.loads(data)
            host = msg['host']
            type = msg['type']
            data_body = msg['data']
            datetime = timeutils.parse_strtime(msg['datetime'])
        except ValueError as e:
            LOG.error("Parse agent data error. Data : %s" % data)
            return
        
        self.dispatcher.dispatch(host, type, data_body, datetime)
    
    def start(self):
        self.receiver.start_event_loop()