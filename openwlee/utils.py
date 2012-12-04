import re
import json
import socket
import inspect

from openwlee import exception
from openwlee.openstack.common import cfg
from openwlee.openstack.common.jsonutils import to_primitive

CONF = cfg.CONF

def methods_with_decorator(cls, decorator_name):
    """ A method that find all functions with the given decorator_name """
    
    method_names = []
    sourcelines = inspect.getsourcelines(cls)[0]
    
    for i,line in enumerate(sourcelines):
        line = line.strip()
        if line.split('(')[0].strip() == '@'+decorator_name: # leaving a bit out
            nextLine = sourcelines[i+1]
            name = nextLine.split('def')[1].split('(')[0].strip()
            method_names.append(name)
            
    return method_names

def singleton(class_):
    """ A decorator that makes a class singleton. """
    
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    
    return getinstance

def instance_id_to_time(id):
    return 'instance-%08x' % id

def instance_name_to_id(name):
    """ Convert nova instance name to integer id. """
    
    match = re.match('instance-([a-f0-9]+)', name)
    if match != None:
        return int(match.groups()[0])
    else:
        return None

def datetime_to_timestamp(date):
    return int(date.strftime('%s'))

def hostname():
    return socket.gethostname()

def debug(func):
    """
    A decorator used to debug a function
    """
    def invoke_with_debug(*args, **kargs):
        
        print ""
        print "Invoking Function : %s.%s" % (func.__module__, func.__name__) 
        print "With args : %s kargs : %s" % (to_primitive(args), 
                                             to_primitive(kargs))
        ret = func(*args, **kargs)
        print "Function returns : %s" % to_primitive(ret)
        print ""
        return ret
    
    return invoke_with_debug
        

class LazyPluggable(object):
    """A pluggable backend loaded lazily based on some value."""

    def __init__(self, pivot, **backends):
        self.__backends = backends
        self.__pivot = pivot
        self.__backend = None

    def __get_backend(self):
        if not self.__backend:
            backend_name = CONF[self.__pivot]
            if backend_name not in self.__backends:
                msg = _('Invalid backend: %s') % backend_name
                raise exception.WleeException(msg)

            backend = self.__backends[backend_name]
            if isinstance(backend, tuple):
                name = backend[0]
                fromlist = backend[1]
            else:
                name = backend
                fromlist = backend

            self.__backend = __import__(name, None, None, fromlist)
        return self.__backend

    def __getattr__(self, key):
        backend = self.__get_backend()
        return getattr(backend, key)
    
    