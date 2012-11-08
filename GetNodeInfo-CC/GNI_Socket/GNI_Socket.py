

'''
#File Name: GNI_Socket.py
#Version : v1.0
#Author : Li Desheng
#Time : 2012-10-30
#Usage : About eventlet socket
'''

import time
from _UDPSocket_ import _SocketUDP
import GNI_Opt

class GNISocket(_SocketUDP.UDPSocket):
    def __init__(self):
        super(GNISocket,self).__init__(('0.0.0.0',GNI_Opt.conf_Port),GNI_Opt.conf_MaxLen,5)
        if(self.Flag==False):
            #print 'Socket initial failed! Now exit!'
            #exit()
            #return False
            raise
    

#mGNISocket=GNISocket(('0.0.0.0',GNI_Opt.conf_Port),GNI_Opt.conf_MaxLen,5)

'''
#Just for test
i=0
while i<3:
i=i+1
print i
time.sleep(10)
print mSocket.Socket_Read(500)
print mSocket.Socket_Read(500)
#Socket_Read(5,mSocket,GNI_Opt.ReadLen)
'''

