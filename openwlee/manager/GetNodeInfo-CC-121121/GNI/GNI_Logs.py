'''
#File Name: GNI_Logs.py
#Version : v1.0
#Author : Li Desheng
#Time : 2012-10-31
#Usage :
'''
# -*- coding:gbk -*-
import os

from _modules_._log_ import _Log as log

class GNILog(log.LogCtls):
    def __init__(self,ConfigFile='./GNI/GNIConfLog/logging.conf',Name='nova-monitor'):
        super(GNILog,self).__init__(ConfigFile, Name)


'''
#Just for a test
mylog=GNILog(Name='lds')
mylog.WriteLog('DEBUG','ok')
mylog.WriteLog('DEBU','ok')
mylog.SetLoggerName('hloo')
mylog.WriteLog('CRIT','err')
'''

