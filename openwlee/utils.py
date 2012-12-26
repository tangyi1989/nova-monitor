import os
import re
import time
import json
import socket
import signal
import inspect
import traceback

from eventlet import greenthread
from eventlet.green import subprocess

from openwlee import exception
from openwlee.openstack.common import cfg
from openwlee.openstack.common import log as logging
from openwlee.openstack.common.jsonutils import to_primitive

CONF = cfg.CONF
LOG = logging.getLogger('openwlee.utils')

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

def walk_class_hierarchy(clazz, encountered=None):
    """Walk class hierarchy, yielding most derived classes first"""
    if not encountered:
        encountered = []
    for subclass in clazz.__subclasses__():
        if subclass not in encountered:
            encountered.append(subclass)
            # drill down to leaves first
            for subsubclass in walk_class_hierarchy(subclass, encountered):
                yield subsubclass
            yield subclass

def instance_id_to_name(id):
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

def debug(func):
    """ A decorator used to debug a function """
    def invoke_with_debug(*args, **kargs):
        
        print ""
        print "Invoking Function : %s.%s" % (func.__module__, func.__name__) 
        print "With args : %s kargs : %s" % (to_primitive(args), 
                                             to_primitive(kargs))
        start = time.time()
        try:
            ret = func(*args, **kargs)
        except Exception as e:
            print "Caught exception : %s" % str(e)
            print traceback.format_exc()
            raise e
        print "Function returns : %s" % to_primitive(ret)
        print "Cost %f seconds" % (time.time() - start)
        print ""
        return ret
    
    return invoke_with_debug


def _subprocess_setup():
    # Python installs a SIGPIPE handler by default. This is usually not what
    # non-Python subprocesses expect.
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

def execute(*cmd, **kwargs):
    """Helper method to execute command with optional retry.

    If you add a run_as_root=True command, don't forget to add the
    corresponding filter to etc/nova/rootwrap.d !
    
    :param cmd: Passed to subprocess.Popen.
    :param process_input: Send to opened process.
    :param check_exit_code: Single bool, int, or list of allowed exit
    codes. Defaults to [0]. Raise
    exception.ProcessExecutionError unless
    program exits with one of these code.
    :param delay_on_retry: True | False. Defaults to True. If set to
    True, wait a short amount of time
    before retrying.
    :param attempts: How many times to retry cmd.
    :param run_as_root: True | False. Defaults to False. If set to True,
    the command is run with rootwrap.
    
    :raises exception.NovaException: on receiving unknown arguments
    :raises exception.ProcessExecutionError:

    :returns: a tuple, (stdout, stderr) from the spawned process, or None if
    the command fails.
    """
    process_input = kwargs.pop('process_input', None)
    check_exit_code = kwargs.pop('check_exit_code', [0])
    ignore_exit_code = False
    if isinstance(check_exit_code, bool):
        ignore_exit_code = not check_exit_code
        check_exit_code = [0]
    elif isinstance(check_exit_code, int):
        check_exit_code = [check_exit_code]
    delay_on_retry = kwargs.pop('delay_on_retry', True)
    attempts = kwargs.pop('attempts', 1)
    run_as_root = kwargs.pop('run_as_root', False)
    shell = kwargs.pop('shell', False)

    if len(kwargs):
        raise exception.NovaException(_('Got unknown keyword args '
                                        'to utils.execute: %r') % kwargs)

    if run_as_root and os.geteuid() != 0:
        #FIXME : there need more process.
        cmd = ['sudo'] + list(cmd)

    cmd = map(str, cmd)

    while attempts > 0:
        attempts -= 1
        try:
            LOG.debug(_('Running cmd (subprocess): %s'), ' '.join(cmd))
            _PIPE = subprocess.PIPE # pylint: disable=E1101

            if os.name == 'nt':
                preexec_fn = None
                close_fds = False
            else:
                preexec_fn = _subprocess_setup
                close_fds = True

            obj = subprocess.Popen(cmd,
                                   stdin=_PIPE,
                                   stdout=_PIPE,
                                   stderr=_PIPE,
                                   close_fds=close_fds,
                                   preexec_fn=preexec_fn,
                                   shell=shell)
            result = None
            if process_input is not None:
                result = obj.communicate(process_input)
            else:
                result = obj.communicate()
            obj.stdin.close() # pylint: disable=E1101
            _returncode = obj.returncode # pylint: disable=E1101
            LOG.debug(_('Result was %s') % _returncode)
            if not ignore_exit_code and _returncode not in check_exit_code:
                (stdout, stderr) = result
                raise exception.ProcessExecutionError(
                        exit_code=_returncode,
                        stdout=stdout,
                        stderr=stderr,
                        cmd=' '.join(cmd))
            return result
        except exception.ProcessExecutionError:
            if not attempts:
                raise
            else:
                LOG.debug(_('%r failed. Retrying.'), cmd)
                if delay_on_retry:
                    greenthread.sleep(random.randint(20, 200) / 100.0)
        finally:
            # NOTE(termie): this appears to be necessary to let the subprocess
            # call clean something up in between calls, without
            # it two execute calls in a row hangs the second one
            greenthread.sleep(0)

class LazyPluggable(object):
    """ A pluggable backend loaded lazily based on some value. """

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
    
    