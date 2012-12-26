
import webob
import routes
from openwlee import utils
from openwlee.api import instance
from openwlee.openstack.common import wsgi
from openwlee.openstack.common import log as logging

LOG = logging.getLogger('openwlee.api')

class APIRouter(wsgi.Router):
    def __init__(self, conf, **global_conf):
        self.conf = conf
        mapper = self.setup_mapper()
        super(APIRouter, self).__init__(mapper)
    
    def setup_mapper(self):
        mapper = routes.Mapper()
        
        instance_resource = instance.create_resource(self.conf)
        mapper.connect(None, "/instance/{instance_id}/performance", 
                       controller=instance_resource, action="performance",
                       conditions={'method': 'GET'})
        mapper.connect(None, "/instance/{instance_id}/statistic", 
                       controller=instance_resource, action="statistic",
                       conditions={'method': 'GET'})
        
        return mapper

class Versions():
    def __init__(self, conf, **global_conf):
        self.conf = conf
    
    @webob.dec.wsgify(RequestClass=wsgi.Request)
    def __call__(self, req):
        return '{"version" : "v1.0"}'
