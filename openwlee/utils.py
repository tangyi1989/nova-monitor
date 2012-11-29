
import re
import json
import socket
import inspect
import datetime

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


def instance_name_to_id(name):
    """ Convert nova instance name to integer id. """
    match = re.match('instance-([a-f0-9]+)', name)
    if match != None:
        return int(match.groups()[0])
    else:
        return None

def utc_now():
    return datetime.datetime.utcnow()

def hostname():
    return socket.gethostname()

def to_primitive(value, convert_instances=False, level=0):
    """ Fine, I copied it from nova utils. 
        Convert a complex object intoprimitives.
    """
    
    try:
        if type(value) is type([]) or type(value) is type((None,)):
            o = []
            for v in value:
                o.append(to_primitive(v, convert_instances=convert_instances,
                                      level=level))
            return o
        elif type(value) is type({}):
            o = {}
            for k, v in value.iteritems():
                o[k] = to_primitive(v, convert_instances=convert_instances,
                                    level=level)
            return o
        elif isinstance(value, datetime.datetime):
            return str(value)
            
        return value
    
    except TypeError, e:
        # Class objects are tricky since they may define something like
        # __iter__ defined but it isn't callable as list().
        return unicode(value)

def json_dumps(value):
    try:
        return json.dumps(value)
    except TypeError:
        pass
    
    return json.dumps(to_primitive(value))

def json_loads(s):
    return json.loads(s)
