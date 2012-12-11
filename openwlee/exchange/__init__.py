
from openwlee import utils
from openwlee.openstack.common import cfg

exchange_opts = [
    cfg.StrOpt('exchage_method', default='http',
               help='The way the wlee agent report to wlee daemon.')
           ]

CONF = cfg.CONF
CONF.register_opts(exchange_opts)

"""
Note:
    There are four exchange now.
    
    1.fake driver fakes report data, but in fact, it create a WleeDaemonManager,
    and just feed data to manager's handle_data directly.
    
    2.display driver just print report data on screen, is used for debug wlee agent.
    
    3.zeromq use zeromq to receive and report data.
    4.http use HTTP protocol to receive and report data.
"""
IMPL = utils.LazyPluggable('exchage_method',
                           fake='openwlee.exchange.fake',
                           display='openwlee.exchange.display',
                           zeromq='openwlee.exchange.zeromq',
                           http='openwlee.exchange.http')

Reporter = IMPL.Reporter
Receiver = IMPL.Receiver
