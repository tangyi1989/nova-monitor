
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

######################## agent status section #######################

def update_agent_status(host, datetime):
    return IMPL.update_agent_status(host, datetime)

###################### instance monitor section #####################

def save_instance_perf_data(perf_data):
    return IMPL.save_instance_perf_data(perf_data)

def get_instance_recently_perf(instance_name, seconds = 60):
    return IMPL.get_instance_recently_perf(instance_name, seconds)

def update_instance_statistic_data(statistic_data, datetime):
    """ statistic_data include instance's name. """
    return IMPL.update_instance_statistic_data(statistic_data, datetime)

def get_instance_statistic(instance_name):
    return IMPL.get_instance_statistic(instance_name)
