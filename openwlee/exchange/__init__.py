
from openwlee import utils
from openwlee.openstack.common import cfg

exchange_opts = [
    cfg.StrOpt('exchage_method', default='zeromq',
               help='The way the wlee agent report to wlee daemon.')
           ]

CONF = cfg.CONF
CONF.register_opts(exchange_opts)

IMPL = utils.LazyPluggable('exchage_method',
                           fake='openwlee.exchange.fake',
                           display='openwlee.exchange.display',
                           zeromq='openwlee.exchange.zeromq',)

Reporter = IMPL.Reporter
Receiver = IMPL.Receiver
