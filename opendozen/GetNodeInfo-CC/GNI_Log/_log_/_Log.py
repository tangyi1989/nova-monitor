'''
#File Name: _Log.py
#Version : v1.0
#Author : Li Desheng
#Time : 2012-10-31
#Usage : log class
'''

#!/usr/bin/env python

import logging
import logging.config

class LogCtls(object):
    def __init__(self,ConfigFile,Name):
        logging.config.fileConfig(ConfigFile)
        self.logger = logging.getLogger(Name)

    def WriteLog(self,Level,Msg):
        if Level=='DEBUG':
            self.logger.debug(Msg)
        elif Level=='INFO':
            self.logger.info(Msg)
        elif Level=='WARN':
            self.logger.warn(Msg)
        elif Level=='ERR':
            self.logger.warn(Msg)
        elif Level=='CRIT':
            self.logger.critical(Msg)
        else:
            self.logger.info('Sorry,your level is wrong.Please use "DEBUG","INFO","WARN","ERR" or "CRIT".')
            print 'Sorry,your level is wrong.Please use "DEBUG","INFO","WARN","ERR" or "CRIT".'

    def SetLoggerName(self,Name):
        self.logger = logging.getLogger(Name)
        
'''
#Just for a test
mylog=LogCtls('logging.conf','test')
mylog.WriteLog('DEBUG','ok')
mylog.WriteLog('DEBU','ok')
mylog.SetLoggerName('hloo')
mylog.WriteLog('CRIT','err')

'''
