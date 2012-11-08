#!/usr/bin/env python
import os
import eventlet
from eventlet import wsgi

def hello_world(env, start_response):
    if env['PATH_INFO'] != '/':
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return ['Not Found\r\n']
    start_response('200 OK', [('Content-Type', 'text/plain')])
    print env     
    return ['Hello, World!I am the cgi!\r\n']

print 'nani~~~'        
wsgi.server(eventlet.listen(('', 9090)), hello_world)

