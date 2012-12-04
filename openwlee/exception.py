
class WleeException(Exception):
    """Base Nova Exception

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.

    """
    message = _("An unknown exception occurred.")
    code = 500
    headers = {}
    safe = False

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        if not message:
            try:
                message = self.message % kwargs

            except Exception as e:
                # kwargs doesn't match a variable in the message
                # log the issue and the kwargs
                
                # TODO release this code
                #LOG.exception(_('Exception in string format operation'))
                #for name, value in kwargs.iteritems():
                #    LOG.error("%s: %s" % (name, value))
                
                # at least get the core message out if something happened
                message = self.message

        super(WleeException, self).__init__(message)

