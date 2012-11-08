#!/usr/bin/env python
import os
import eventlet
from eventlet import wsgi

webpath='/home/lidesheng/MyWorks/nginx/web'
def hello_world(env, start_response):
    print os.path.dirname(__file__)
    print 'this:%s' %env['PATH_INFO']
    print env

    if env['PATH_INFO'] != '/':
        start_response('200 OK', [('Content-Type', env['CONTENT_TYPE'])])
        return [open('%s%s' %(webpath,env['PATH_INFO'])).read()]
        
        #return '404 not found'
    start_response('200 OK', [('Content-Type', 'text/html')])    
    return [open('%s/index.html' %webpath).read()] 

        
wsgi.server(eventlet.listen(('', 9091)), hello_world)

