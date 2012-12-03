import re
import json
import socket
import inspect

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

def id_to_instance_time(id):
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


