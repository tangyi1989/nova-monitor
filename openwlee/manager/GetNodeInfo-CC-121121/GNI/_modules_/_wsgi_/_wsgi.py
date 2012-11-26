
'''
#File Name: _wsgi.py
#Version : v1.0
#Author : Li Desheng
#Time : 2012-11-21
#Usage : 
'''

#!/usr/bin/env python
import os
import eventlet
from eventlet import wsgi

def hello_world(env, start_response):
    #print 'this:%s,Content-Type=%s' %(env['PATH_INFO'],env['CONTENT_TYPE'])
    print env
    postdata=env['wsgi.input'].read() #it can be read only one time!!
    start_response('200 OK', [('Content-Type', 'text/plain')])
    print postdata
    return 'I have get your words:"%s"' %postdata

        
wsgi.server(eventlet.listen(('', 9092)), hello_world)

