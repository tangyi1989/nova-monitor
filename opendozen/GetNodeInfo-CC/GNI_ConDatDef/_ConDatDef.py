

'''
#File Name: GNI_Libs.py
#Version : v1.0
#Author : Li Desheng
#Time : 2012-10-30
#Usage :
'''
# -*- coding:gbk -*-
from ctypes import *
import os
from _log_ import _Log as Log
from _lib_ import _lib as Libs

class ConDatDef(Log.LogCtls,Libs._lib_):
    def __init__(self,
                 LogConfigFile="E:\My_Works\Python\GetNodeInfo\GetNodeInfo-120827\GetNodeInfo-CC\GNIConfLog\logging.conf",
                 LoggerName='ConDatDef',
                 libfile="E:\My_Works\Python\GetNodeInfo\GetNodeInfo-120827\GetNodeInfo-CC\GNILibs\ConDatDef.dll"):
        try:
            Log.LogCtls.__init__(self,LogConfigFile,LoggerName)
            Libs._lib_.__init__(self,libfile)
            print self.logger
        except Exception,e:
            self.WriteLog('CRIT',e)

    def MakSendPack(self,job):
        #make a pointer to a (job[0]-1) dimenssion arry
        pAddList = (c_char_p * job[0])()
        
        i=0
        while i<job[0]:
            pAddList[i]=job[i+1]
            i+=1
        DestAddr=(c_char*500)()
        SendLen=self.lib.MakeConPack(byref(DestAddr),job[0],pointer(pAddList),0xa0,49)
        
        return DestAddr[0:SendLen]

#Just for a test
mcondef=ConDatDef()
print mcondef.MakSendPack((2,'458\0','adb\0'))

