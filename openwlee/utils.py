from datetime import datetime
import inspect

import re

"""
Get utc datetime.
"""
def utc_now():
    return datetime.utcnow()

"""
Convert nova instance name to integer id.
"""
def instance_name_to_id(name):
    match = re.match('instance-([a-f0-9]+)', name)
    if match != None:
        return int(match.groups()[0])
    else:
        return None

"""
A method that find all functions with the given decorator_name
"""
def methods_with_decorator(cls, decorator_name):
    method_names = []
    sourcelines = inspect.getsourcelines(cls)[0]
    
    for i,line in enumerate(sourcelines):
        line = line.strip()
        if line.split('(')[0].strip() == '@'+decorator_name: # leaving a bit out
            nextLine = sourcelines[i+1]
            name = nextLine.split('def')[1].split('(')[0].strip()
            method_names.append(name)
            
    return method_names

"""
A decorator that makes a class singleton.
"""
def singleton(class_):
  instances = {}
  def getinstance(*args, **kwargs):
    if class_ not in instances:
        instances[class_] = class_(*args, **kwargs)
    return instances[class_]
  return getinstance
