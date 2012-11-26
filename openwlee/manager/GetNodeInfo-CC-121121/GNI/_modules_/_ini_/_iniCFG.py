

'''
#File Name: _iniCFG.py
#Version : v1.0
#Author : Li Desheng
#Time : 2012-10-30
#Usage :
'''
# -*- coding:gbk -*-
import ConfigParser, os
class INIFILE:
    def __init__(self, filename):
        self.filename = filename
        self.initflag = False
        self.cfg = None
        self.inihandle = None
        self.inihandle = None
    def Init(self,rw='r'):
        self.cfg = ConfigParser.ConfigParser()
        try:
            self.inihandle = open(self.filename, rw)
            self.cfg.readfp(self.inihandle)
            self.initflag = True
        except:
            self.initflag = False
        return self.initflag
    
    def UnInit(self):
        if self.initflag:
            self.inihandle.close()
            
    def GetValue(self, Section, Key, Type,Default = ""):
        try:
            value = self.cfg.get(Section, Key)
            if Type=='INT':
                value=int(value)
            elif Type=='FLOAT':
                value=float(value)
        except:
            value = Default
        return value

        
    def SetValue(self, Section, Key, Value):
        try:
            self.cfg.set(Section, Key, Value)
        except:
            self.cfg.add_section(Section)
            self.cfg.set(Section, Key, Value)
            self.cfg.write(self.inihandle)
     
            
def GetValue(FileName,Section,Key,Type,Default):
    myini=INIFILE(FileName)
    myini.Init()
    Value=myini.GetValue(Section,Key,Type,Default)
    myini.UnInit()
    return Value

#print 'get:%s' %GetValue(os.getcwd() +'/config.ini','config','name4','FLOAT',"....")

