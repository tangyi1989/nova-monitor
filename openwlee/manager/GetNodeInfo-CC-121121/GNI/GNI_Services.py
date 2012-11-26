
'''
#File Name: GNI_Service.py
#Version : v1.0
#Author : Li Desheng
#Time : 2012-10-30
#Usage :
'''
# -*- coding:gbk -*-
import os
import time
import Queue
import threading
import sys
import urllib2
import pickle
import json

import GNI_Conf as conf
import GNI_Logs as logging
import GNI_ConDatDef as datadef

mlog=logging.GNILog(conf.confopts['LogConf']['LogConfFile']['Value'],'GNI_Services')


def store2db(data):
    print 'saved:%s' %data

def hello(data):
    print 'hello'

controllers={} 
cmds=[]
funcs=[store2db,hello]
i=0
for cmd in datadef.datapack:
    controllers[cmd]=funcs[i]
    i=i+1

print controllers

   

'''
Map the cmd to the service
'''
def dispatcher(env):
    try:
        print env
        postdata=env['wsgi.input'].read()
        print 'type:',type(postdata),',data:',postdata
        data=json.loads(postdata)   #notice:it's [loads] ,not [load]!!!!
        print data['cmd']
        func=controllers.get(data['cmd'])
        func(data['data'])
        data='tmd'
        return 'I get your words:%s' %data
    except:
        print 'err!!'
        return 'Get No data~'
      

