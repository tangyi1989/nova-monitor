
from openwlee import utils
from openwlee.openstack.common import cfg

exchange_opts = [
    cfg.StrOpt('exchage_method', default='display',
               help='The way the wlee agent report to wlee api.')
           ]

CONF = cfg.CONF
CONF.register_opts(exchange_opts)

IMPL = utils.LazyPluggable('exchage_method',
                           fake='openwlee.exchange.fake',
                           display='openwlee.exchange.display',)

Reporter = IMPL.Reporter
Receiver = IMPL.Receiver
