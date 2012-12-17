
from openwlee.openstack.common import log as logging

LOG = logging.getLogger("openwlee.exchange")

class Reporter(object):
    """ Reporter worked in wlee agent to send message to receiver 
    which in wlee daemon. """
    def __init__(self, *args, **kargs):
        pass
    
    def report(self, data):
        """ Block or not, guarantee or not, that's a question."""
        raise NotImplementedError
    
class Receiver(object):
    """ A receiver worked in wlee daemon to receive from wlee agent. 
     """
    def __init__(self, receive_handler, *args, **kargs):
        """ receive_handler : would be invoked when receive report data 
        from agent. """
        self.receive_handler = receive_handler
        
    def handle_receive_data(self, data):
        """ subclass would call this function when receive data. """
        try:
            self.receive_handler(data)
        except Exception as e:
            LOG.error("Caught an exception when handle receive reporter's "
                      "report data. Exception : %s" % str(e))
    
    def start_event_loop(self):
        """ start receiver's event loop , invoke handle_receive_data when
        receive agent's data. """
        raise NotImplementedError