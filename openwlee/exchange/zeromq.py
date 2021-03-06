
import zmq
from openwlee.exchange import base
from openwlee.openstack.common import cfg
from openwlee.openstack.common import log as logging

AGENT_TOPIC = "wlee.agent"
LOG = logging.getLogger('openwlee.exchange.zeromq')

"""
WARNING : THIS CAANOT BE USED NOW! THIS IS BAD!
"""

class ZeromqReceiver(base.Receiver):
    def __init__(self, *args, **kargs):
        super(ZeromqReceiver, self).__init__(*args, **kargs)
        
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
    
    def start_event_loop(self):
        LOG.info("ZeromqReceiver would connect to tcp://localhost:9779")
        
        self.socket.connect("tcp://localhost:9779")
        self.socket.setsockopt(zmq.SUBSCRIBE, '')  
        while True:
            data = self.receive()
            self.handle_receive_data(data)
    
    def receive(self):
        
        topic, msg = self.socket.recv_pyobj()
        LOG.info("ZeromqReceiver received topic : %s , message %s" %\
                  (topic, msg))
        return msg

class ZeromqReporter(base.Reporter):
    def __init__(self, *args, **kargs):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:9779")
    
    def report(self, data):
        LOG.info("ZeromqReporter send topic message (%s) to receiver"\
                  % data)
        
        self.socket.send_pyobj([AGENT_TOPIC, data])
        
Reporter = ZeromqReporter
Receiver = ZeromqReceiver