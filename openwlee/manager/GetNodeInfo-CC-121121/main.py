'''
#File Name: GNI_CCMain.py
#Version : v1.0
#Author : Li Desheng
#Time : 2012-10-31
#Usage : The project main file for the CC
'''

#!/usr/bin/env python
import os
import eventlet
from eventlet import wsgi

'''
Set the options
'''
import GNI.GNI_Conf as conf
conf.get_conf_opts()

import GNI.GNI_Services as services

def service_handle(env, start_response):
    #print 'this:%s,Content-Type=%s' %(env['PATH_INFO'],env['CONTENT_TYPE'])
    back=services.dispatcher(env)
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return back
    
        
def main():  
    print '-----------------------------------------------------\n'
    print 'Hello!This is the collector manager for nova-monitor.\nIt gets information from all the nodes in the cloud,and push it into the database.' 
    print '-----------------------------------------------------\n' 
    wsgi.server(eventlet.listen(('', conf.confopts['CollectorSvr']['CSPort']['Value'])), service_handle)

if __name__ == "__main__":
    main()
