
'''
#File Name: GNI_Excutes.py
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
import socket
sys.path.append('..')
import GNI_Socket.GNI_Socket as Socket
import GNI_Conf.GNI_conf as Conf
import GNI_Log.GNI_Logs as Log

TEXEConf={
    'EXE1':{
        'ID':1,
        'CMD':'',
        'Queue':0,
        'JobMaxSize':200
    },
    'EXE2':{
        'ID':2,
        'CMD':'',
        'Queue':0,
        'JobMaxSize':200
    },
    'EXE3':{
        'ID':3,
        'CMD':'',
        'Queue':0,
        'JobMaxSize':200
    },
    'EXE4':{
        'ID':4,
        'CMD':'',
        'Queue':0,
        'JobMaxSize':200
    },
    'EXEMapReduce':{
        'ID':0,
        'CMDs':'',
        'Exes':[],
        'RecvMaxLen':1000,
        'Socket':''
    }
}

mlog=Log.GNILog(Conf.confopts['LogConf']['LogConfFile']['Value'],'GNI_Excutes')
try:
    mGNISocket=Socket.GNISocket()
except:
    mlog.WriteLog('CRIT','NANI~~Bind the port failed!Exit now!')
    exit()

class ExcuteFactory:
    def factory(self, which,mTEXEOpts):
        if which == "EXE1":
            return EXE1(mTEXEOpts)
        if which == "EXE2":
            return EXE2(mTEXEOpts)
        if which == "EXE3":
            return EXE3(mTEXEOpts)
        if which == "EXE4":
            return EXE4(mTEXEOpts)
        if which == "EXEMapReduce":
            mTEXEOpts['Socket']=mGNISocket
            
            return EXEMapReduce(mTEXEOpts)
        else:
            return None

class Excutes(threading.Thread):
    def __init__(self,mTEXEOpts):
        super(Excutes,self).__init__()
        self.__JobQueue=Queue.PriorityQueue(mTEXEOpts['JobMaxSize'])
        self.__ID=mTEXEOpts['ID']
        self.__CMD=mTEXEOpts['CMD']
        self.__lock = threading.Lock()
        self.__QEvent = threading.Event()
        
    def AppendJob(self,TJob):
        self.__lock.acquire ()
        self.__JobQueue.put(TJob)
        self.__lock.release ()
        Self.__QEvent.set()
        
    def GetJob(self):
        try:
            job = self.__JobQueue.get_nowait()
            print "ding job:%s;left:%d" %(job,self.__JobQueue.qsize())
            print job
        except Queue.Empty:
            self.__QEvent.clear()
            self.__QEvent.wait()
            job=False
        return job
        
    def run(self):
        pass


class EXEMapReduce(threading.Thread):
    def __init__(self,mTEXEOpts):
        super(EXEMapReduce,self).__init__()
        self.__Socket=mTEXEOpts['Socket']
        self.__TEXEs=mTEXEOpts['Exes']
        
    def AppendEXEQues(self,TEXEQueue):
        self.__TEXEQueues.append(TEXEQueue)
    def DeleteEXEQue(self,EXEName):
        pass
    def run(self):
        print "\ndo EXEMapReduce"
        print self.__TEXEs
        while True:
            try:
                info,addr=self.__Socket.Socket_Read_(5)
            except socket.timeout as e:
                pass
            except Exception,ec:
                print 'nn'
            
            
    
class EXE1(Excutes):
    def __init__(self,mTEXEOpts):
        super(EXE1,self).__init__(mTEXEOpts)
        
    def run(self):
        while True:
            print "\ndo exe1"
            time.sleep(2)

class EXE2(Excutes):
    def __init__(self,mTEXEOpts):
        super(EXE2,self).__init__(mTEXEOpts)
        
    def run(self):
        while True:
            print "\ndo exe2"
            time.sleep(2)

class EXE3(Excutes):
    def __init__(self,mTEXEOpts):
        super(EXE3,self).__init__(mTEXEOpts)
        
    def run(self):
        print "\ndo exe3"

class EXE4(Excutes):
    def __init__(self,mTEXEOpts):
        super(EXE4,self).__init__(mTEXEOpts)
        
    def run(self):
        print "\ndo exe4"


#Just for a test
#exelist=[('EXEMapReduce',0),('EXE1',100),('EXE2',100),('EXE3',100),('EXE4',200)]
fac=ExcuteFactory()
for exename in TEXEConf:
    exe=fac.factory(exename,TEXEConf[exename])
    #print "%s,%s" %(exename[0],exename[1])
    if exename!='EXEMapReduce':
        TEXEConf['EXEMapReduce']['Exes'].append((exe,TEXEConf[exename]['CMD']))
    exe.start()

