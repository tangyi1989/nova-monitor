

'''
#File Name: _SocketUDP.py
#Version : v1.0
#Author : Li Desheng
#Time : 2012-10-30
#Usage : About eventlet socket
'''

import eventlet
from eventlet.green import socket

class UDPSocket(object):
    def __init__(self,TAddress,MaxLen,TimeOut=500):
        self.Flag,self.mySocket=self.__Socket_Init(TAddress)
        self.MaxLen=MaxLen
        self.TimeOut=TimeOut
        
    def Socket_Read(self,TimeOut):
        try:
            self.mySocket.settimeout(TimeOut)
            data, addr = self.mySocket.recvfrom(self.MaxLen)
            #print "%s Recv:%s" %(addr,data)
            return True,data,addr
        
        except socket.error as e:
            #print "Read erro:%s" %e
            return False,e,0

    def Socket_Read_(self,TimeOut):
        self.mySocket.settimeout(TimeOut)
        data, addr = self.mySocket.recvfrom(self.MaxLen)
        return data,addr
      

    def Socket_Send(self,PackInfo,TDestAddr,TimeOut):
        try:
            self.mySocket.settimeout(TimeOut)
            self.mySocket.sendto(PackInfo,TDestAddr)
            #print "Send to %s:%s" %(TDestAddr,PackInfo)
            return True,data
        
        except socket.error as e:
            print "Read erro:%s" %e
            return False,e
        
    def __Socket_Init(self,TAddress):
        try:
            mySocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            mySocket.bind(TAddress)
            #print "Bind OK!"
            return True,mySocket
        
        except socket.error as e:
            #print 'Socket Error : %s' % e
            return False,e




'''
#Just for test
mSocket=UDPSocket(('0.0.0.0',7100),512,5)
'''

