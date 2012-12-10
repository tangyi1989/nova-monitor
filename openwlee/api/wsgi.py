
import webob
from openwlee import utils
from openwlee.openstack.common import wsgi
from openwlee.openstack.common import log as logging

LOG = logging.getLogger('openwlee.api.wsgi')

class FaultWrapper(wsgi.Middleware):
    """Calls down the middleware stack, making exceptions into faults."""
    
    def __init__(self, app, conf, **local_conf):
        super(FaultWrapper, self).__init__(app)

    _status_to_type = {}

    @staticmethod
    def status_to_type(status):
        if not FaultWrapper._status_to_type:
            for clazz in utils.walk_class_hierarchy(webob.exc.HTTPError):
                FaultWrapper._status_to_type[clazz.code] = clazz
        return FaultWrapper._status_to_type.get(
                                  status, webob.exc.HTTPInternalServerError)()

    def _error(self, inner, req):
        LOG.exception(_("Caught error: %s"), unicode(inner))

        safe = getattr(inner, 'safe', False)
        headers = getattr(inner, 'headers', None)
        status = getattr(inner, 'code', 500)
        if status is None:
            status = 500

        msg_dict = dict(url=req.url, status=status)
        LOG.info(_("%(url)s returned with HTTP %(status)d") % msg_dict)
        outer = self.status_to_type(status)
        if headers:
            outer.headers = headers
        # NOTE(johannes): We leave the explanation empty here on
        # purpose. It could possibly have sensitive information
        # that should not be returned back to the user. See
        # bugs 868360 and 874472
        # NOTE(eglynn): However, it would be over-conservative and
        # inconsistent with the EC2 API to hide every exception,
        # including those that are safe to expose, see bug 1021373
        if safe:
            outer.explanation = '%s: %s' % (inner.__class__.__name__,
                                            unicode(inner))

        #notifications.send_api_fault(req.url, status, inner)
        return Fault(outer)

    @webob.dec.wsgify(RequestClass=wsgi.Request)
    def __call__(self, req):
        try:
            LOG.info(_("Fault wrapper invoke next application from %s" % self.application))
            return req.get_response(self.application)
        except Exception as ex:
            return self._error(ex, req)

class Fault(webob.exc.HTTPException):
    """Wrap webob.exc.HTTPException to provide API friendly response."""

    _fault_names = {
            400: "badRequest",
            401: "unauthorized",
            403: "forbidden",
            404: "itemNotFound",
            405: "badMethod",
            409: "conflictingRequest",
            413: "overLimit",
            415: "badMediaType",
            501: "notImplemented",
            503: "serviceUnavailable"}

    def __init__(self, exception):
        """Create a Fault for the given webob.exc.exception."""
        self.wrapped_exc = exception
        self.status_int = exception.status_int

    @webob.dec.wsgify(RequestClass=wsgi.Request)
    def __call__(self, req):
        """Generate a WSGI response based on the exception passed to ctor."""
        # Replace the body with fault details.
        code = self.wrapped_exc.status_int
        fault_name = self._fault_names.get(code, "openwleeFault")
        fault_data = {
            fault_name: {
                'code': code,
                'message': self.wrapped_exc.explanation}}
        if code == 413:
            retry = self.wrapped_exc.headers.get('Retry-After', None)
            if retry:
                fault_data[fault_name]['retryAfter'] = retry

        # 'code' is an attribute on the fault tag itself
        metadata = {'attributes': {fault_name: 'code'}}

        xml_serializer = wsgi.XMLDictSerializer(metadata)

        content_type = req.best_match_content_type()
        serializer = {
            'application/xml': xml_serializer,
            'application/json': wsgi.JSONDictSerializer(),
        }[content_type]

        self.wrapped_exc.body = serializer.serialize(fault_data)
        self.wrapped_exc.content_type = content_type
        _set_request_id_header(req, self.wrapped_exc.headers)

        return self.wrapped_exc

    def __str__(self):
        return self.wrapped_exc.__str__()
    
def _set_request_id_header(req, headers):
    context = req.environ.get('openwlee.context')
    if context:
        headers['openwlee-request-id'] = context.request_id