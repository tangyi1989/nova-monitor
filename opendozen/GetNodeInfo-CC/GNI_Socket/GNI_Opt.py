

'''
#File Name: GNI_Opt.py
#Version : v1.0
#Author : Li Desheng
#Time : 2012-7-23
#Usage : Initial the opinions used by GNI_SocketCLit.py
'''
import sys
sys.path.append("..") #to make the system path outside
import GNI_Conf.GNI_conf as Conf

#---The server connect information---
SvrIP='218.192.168.175'
#SvrIP='127.0.0.1'
SvrPort=6000

#---The local infomation---
conf_ClitName='Node1'
conf_Port=Conf.confopts['CollectorSvr']['CSPort']['Value']

conf_MaxLen=Conf.confopts['ConDat']['CDMaxLen']['Value']
print '-----------------------------------------'
print Conf.confopts
print '-----------------------------------------'

