#!/usr/bin/env python
import os
import eventlet
from eventlet import wsgi

webpath='/home/lidesheng/MyWorks/nginx/web'

def hadle(ws):
    print ws

def hello_world(env, start_response):
    print 'this:%s,Content-Type=%s' %(env['PATH_INFO'],env['CONTENT_TYPE'])
    print env
    if env['PATH_INFO'] != '/':
        start_response('200 OK',[('Content-Type', env['CONTENT_TYPE'])])
        return [open('%s%s' %(webpath,env['PATH_INFO'])).read()]
    elif env['REQUEST_METHOD']=='POST':  
        print env['CONTENT_LENGTH'] 
        postdata=env['wsgi.input'].read() #it can be read only one time!!
        start_response('200 OK', [('Content-Type', env['CONTENT_TYPE'])])
        print postdata
        return 'I have get your words:"%s"' %postdata
        
    start_response('200 OK', [('Content-Type', 'text/html')])  
    return [open('%s/index.html' %webpath).read()] 

        
wsgi.server(eventlet.listen(('', 9090)), hello_world)

