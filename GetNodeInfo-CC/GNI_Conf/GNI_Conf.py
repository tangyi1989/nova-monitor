

'''
#File Name: GNI_conf.py
#Version : v1.0
#Author : Li Desheng
#Time : 2012-10-30
#Usage :
'''
# -*- coding:gbk -*-
import os
from _ini_ import _iniCFG


confopts={
    'CollectorSvr':{
        'CSIP':{
            'Value':'',
            'Type':'STRING',
            'default':'127.0.0.1',
            'help':'The IP of the CollectorSvr.'
        },
        'CSPort':{
            'Value':'',
            'Type':'INT',
            'default':7100,
            'help':'The server port of the CollectorSvr.'
        }
        
    },
    'ConDat':{
        'CDVersion':{
            'Value':'',
            'Type':'STRING',
            'default':'V1.0',
            'help':'The version of the communicate data.'
        },
        'CDSmarKey':{
            'Value':'',
            'Type':'STRING',
            'default':'cloud',
            'help':'Use this key to make a sequence for communication.'
        },
        'CDMaxLen':{
            'Value':'',
            'Type':'INT',
            'default':513,
            'help':'The maximum length of the conmunicate data package.'
        },
        'CDDefinationFile':{
            'Value':'',
            'Type':'DTRING',
            'default':'E:\My_Works\Python\GetNodeInfo\GetNodeInfo-120827\GetNodeInfo-CC\GNIConfLog\ConDatDef.ini',
            'help':'The configuration file for UDP conmmunication.'
        }
    },
    'db':{
        'sqlConnection':{
            'Value':'',
            'Type':'STRING',
            'default':'sqlite:///$state_path/$sqlite_db',
            'help':'The connection string to the database.'
        }
    },
    'LogConf':{
        'LogConfFile':{
            'Value':'',
            'Type':'STRING',
            'default':'E:\My_Works\Python\GetNodeInfo\GetNodeInfo-120827\GetNodeInfo-CC\GNIConfLog\logging.conf',
            'help':'Tell the file for log config.'
        }
    }
}

#Notice:Use the real path!
confPath='E:\My_Works\Python\GetNodeInfo\GetNodeInfo-121106\GetNodeInfo-CC\GNIConfLog\config.ini'#os.getcwd()+'/config.ini'

'''
With this class initial,the "Value" in "confopts" will be set.
'''
class ConfOpts:
    def __init__(self,m_confopts,m_confPath):
        ini=_iniCFG.INIFILE(m_confPath)
        ini.Init()
        for session in m_confopts:
            for key in m_confopts[session]:
                m_confopts[session][key]['Value']=ini.GetValue(session,
                                                               key,
                                                               m_confopts[session][key]['Type'],
                                                               m_confopts[session][key]['default'])
                
        ini.UnInit()
        
def __GetConfOpts(m_confopts,m_confPath):
    ini=_iniCFG.INIFILE(m_confPath)
    ini.Init()
    for session in m_confopts:
        for key in m_confopts[session]:
            m_confopts[session][key]['Value']=ini.GetValue(session,
                                                            key,
                                                            m_confopts[session][key]['Type'],
                                                            m_confopts[session][key]['default'])
                
    ini.UnInit()
    
            
def GetConfOpts(m_confopts,m_confPath):
    __GetConfOpts(m_confopts,m_confPath)


#Get conf value now
GetConfOpts(confopts,confPath)

