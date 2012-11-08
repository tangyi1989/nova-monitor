'''
#File Name: GNI_Logs.py
#Version : v1.0
#Author : Li Desheng
#Time : 2012-10-31
#Usage :
'''
# -*- coding:gbk -*-
import os

from _log_ import _Log as log

class GNILog(log.LogCtls):
    def __init__(self,ConfigFile,Name):
        super(GNILog,self).__init__(ConfigFile,Name)


'''
#Just for a test
mylog=GNILog('E:\My_Works\Python\GetNodeInfo\GetNodeInfo-121006\GetNodeInfo-CC\GNIConfLog\logging.conf','lds')
mylog.WriteLog('DEBUG','ok')
mylog.WriteLog('DEBU','ok')
mylog.SetName('hloo')
mylog.WriteLog('CRIT','err')
'''

