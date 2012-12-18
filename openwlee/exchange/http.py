
import sys
import eventlet
import httplib2
from eventlet import wsgi

from openwlee import utils
from openwlee.exchange import base
from openwlee.openstack.common import cfg
from openwlee.openstack.common import log as logging

http_exchange_opts = [
    cfg.StrOpt('http_receiver_listen_host', default="0.0.0.0", 
               help="HTTPReceiver listen bind host"),
    cfg.IntOpt('http_receiver_listen_port', default=9778, 
               help="HTTPReceiver listen port"),
    cfg.StrOpt('http_receiver_address', default='localhost',
               help='HTTP receiver address.'),
    cfg.StrOpt('http_report_path', default='/report',
               help='The absolute path of http report address')
           ]

CONF = cfg.CONF
CONF.register_opts(http_exchange_opts)

LOG = logging.getLogger('openwlee.exchange.http')

class HTTPReceiver(base.Receiver):
    def __init__(self, *args, **kargs):
        super(HTTPReceiver, self).__init__(*args, **kargs)
        self.listener = eventlet.listen((cfg.CONF.http_receiver_listen_host, 
                                       cfg.CONF.http_receiver_listen_port))
        self.report_path = cfg.CONF.http_report_path
        
    def start_event_loop(self):
        def on_request(env, start_response):
            if env['PATH_INFO'] != self.report_path:
                start_response('404 Not Found', [('Content-Type', 'text/plain')])
                return ['Not Found\r\n']
            response_data = 'OK\r\n'
            start_response('200 OK', [('Content-Type', 'text/plain'),
                                      ('Content-Length', len(response_data)),])
            
            try:
                content_length = int(env.get('CONTENT_LENGTH', 0))
            except (ValueError):
                content_length = 0
            wsgi_input = env['wsgi.input']
            body = wsgi_input.read(content_length)
            
            LOG.info("Receive data : %s Length : %d" % (body, content_length))
            
            self.handle_receive_data(body)
            
            return [response_data]
        
        #Do not log wsgi info
        try:
            log_dev = file('/dev/zero', 'w')
        except:
            log_dev = None
            
        wsgi.server(self.listener, on_request, log_dev, debug=False)


class HTTPReporter(base.Reporter):
    def __init__(self, *args, **kargs):
        super(HTTPReporter, self).__init__(*args, **kargs)
        self.report_url = "http://%s:%d%s" % (cfg.CONF.http_receiver_address,
                                              cfg.CONF.http_receiver_listen_port,
                                              cfg.CONF.http_report_path)
        
    def report(self, data):
        http = httplib2.Http()
        try:
            response, body = http.request(self.report_url, "POST", data)
            LOG.info("HTTPRepoter request response : %d, Content : %s" % (response.status, body))
        except Exception as e:
            LOG.error("HTTPReporter request error Exception %s" % e)

Reporter = HTTPReporter
Receiver = HTTPReceiver 
