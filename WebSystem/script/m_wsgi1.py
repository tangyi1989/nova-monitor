#!/usr/bin/env python
import os
import eventlet
from eventlet import wsgi

webpath='/home/lidesheng/MyWorks/nginx/web'

def hadle(ws):
    print ws

def hello_world(env, start_response):
    #print 'this:%s,Content-Type=%s' %(env['PATH_INFO'],env['CONTENT_TYPE'])
    print env
    postdata=env['wsgi.input'].read() #it can be read only one time!!
    start_response('200 OK', [('Content-Type', 'text/plain')])
    print postdata
    return 'I have get your words:"%s"' %postdata

    if env['REQUEST_METHOD']=='POST':  
        #print env['CONTENT_LENGTH'] 
        postdata=env['wsgi.input'].read() #it can be read only one time!!
        start_response('200 OK', [('Content-Type', 'text/plain')])
        print postdata
        return 'I have get your words:"%s"' %postdata
    else:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        print 'ERR:no postdata'
        return ['ERR:404 Not Found']
        
wsgi.server(eventlet.listen(('', 9091)), hello_world)

