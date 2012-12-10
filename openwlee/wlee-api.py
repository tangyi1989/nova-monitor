
import sys

from openwlee import wsgi
from openwlee import utils
from openwlee import config
from openwlee.common import wsgi as wsgi_utils
from openwlee.openstack.common import cfg
from openwlee.openstack.common import wsgi
from openwlee.openstack.common import log as logging

LOG = logging.getLogger('wlee-api')

if __name__ == "__main__":
    config.parse_args(sys.argv)
    logging.setup("openwlee")
    
    app = wsgi_utils.paste_deploy_app(cfg.CONF.api_paste_file, 'wlee', cfg)
    port = cfg.CONF.bind_port
    host = cfg.CONF.bind_host
    
    LOG.info('Starting Openwlee ReST API on %s:%s' % (host, port))
    wsgi_service = wsgi.Service()
    wsgi_service.start(app, port, host)
    wsgi_service.wait()
    