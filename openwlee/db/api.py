
from openwlee import utils
from openwlee.openstack.common import cfg

db_opts = [
    cfg.StrOpt('db_backend',
               default='mongodb',
               help='The backend to use for db')
           ]

CONF = cfg.CONF
CONF.register_opts(db_opts)

IMPL = utils.LazyPluggable('db_backend',
                           mongodb='openwlee.db.mongodb.api')

def update_agent_status():
    return IMPL.update_agent_status()

def save_instance_perf_data(perf_data):
    return IMPL.save_instance_perf_data(perf_data)

def get_instance_recently_perf(instance_name, seconds = 60):
    return IMPL.get_instance_recently_perf(instance_name, seconds)
