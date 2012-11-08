'''
#File Name: GNI_CCMain.py
#Version : v1.0
#Author : Li Desheng
#Time : 2012-10-31
#Usage : The project main file for the CC
'''

#!/usr/bin/python


def main():

    if GNI_MainOpt.ConFlag:
        print "Connet OK! "
        
        GNI_SendQueue.Run_DealQueue()
        GNI_DealConDat.Run_DealConDat()
        GNI_PushNodeInfo.Run_PushInfo()
        print "Run sucessfully!"
      
if __name__ == "__main__":
main()
