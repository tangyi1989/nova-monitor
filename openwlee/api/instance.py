
from openwlee import db
from openwlee import utils
from openwlee.openstack.common import wsgi


class InstanceController():
    """ Instance information controller. """
    def __init__(self, options):
        self.conf = options
    
    def performance(self, req, instance_id):
        instance_id = int(instance_id)
        instance_name = utils.instance_id_to_time(instance_id)
        instance_perf_list = db.get_instance_recently_perf(instance_name)
        return instance_perf_list

def create_resource(options):
    """ Instance resource factory method. """
    deserializer = wsgi.RequestDeserializer()
    serializer = wsgi.ResponseSerializer()
    return wsgi.Resource(InstanceController(options), 
                         deserializer, serializer)

