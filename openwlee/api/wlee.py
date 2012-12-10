
import webob
from openwlee import utils
from openwlee.openstack.common import wsgi
from openwlee.openstack.common import log as logging

LOG = logging.getLogger('openwlee.api.wlee')

class APIRouter():
    def __init__(self, conf, **global_conf):
        pass
    
    @webob.dec.wsgify(RequestClass=wsgi.Request)
    def __call__(self, req):
        return "Hello, World"
        

class Versions():
    def __init__(self, conf, **global_conf):
        pass
    
    @webob.dec.wsgify(RequestClass=wsgi.Request)
    def __call__(self, req):
        return "v1.0"
