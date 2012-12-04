
import sys

from openwlee import wsgi
from openwlee import utils
from openwlee import config
from openwlee.openstack.common import log as logging
from openwlee.openstack.common.wsgi import run_server as wsgi_run_server

from openwlee.openstack.common.jsonutils import to_primitive

if __name__ == "__main__":
    config.parse_args(sys.argv)
    logging.setup("openwlee")
    loader = wsgi.Loader('/etc/openwlee/wlee-api.conf')
    app = loader.load_app('wlee')
    wsgi_run_server(app, 8888)
    