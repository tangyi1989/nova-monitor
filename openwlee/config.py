import os
import socket

from openwlee.openstack.common import cfg

global_opts = [
    cfg.StrOpt('host',
               default=socket.getfqdn(),
               help='Name of this node. This can be an opaque identifier. '
                    'It is not necessarily a hostname, FQDN, or IP address. '
                    'and if using ZeroMQ, a valid hostname, FQDN, or IP '
                    'address'),
]

cfg.CONF.register_opts(global_opts)

def parse_args(argv, default_config_files=None):
    cfg.CONF(argv[1:], project='openwlee', 
             default_config_files = default_config_files)
