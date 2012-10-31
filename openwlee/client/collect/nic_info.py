#*_* coding=utf8 *_*
#!/usr/bin/env python

import time
from datetime import datetime

"""
It would return a dict of network traffic info like this:
{'    ...
 '  eth0': {'recv_bytes': '34084530',
            'recv_compressed': '0',
            'recv_drop': '0',
            'recv_errs': '0',
            'recv_fifo': '0',
            'recv_frame': '0',
            'recv_multicast': '0',
            'recv_packets': '30599',
            'trans_bytes': '6170441',
            'trans_carrier': '0',
            'trans_colls': '0',
            'trans_compressed': '0',
            'trans_drop': '0',
            'trans_errs': '0',
            'trans_fifo': '0',
            'trans_packets': '32377'}}
            ...
"""
def nic_traffic_info_read():
    lines = open("/proc/net/dev", "r").readlines()
    
    columnLine = lines[1]
    _, receiveCols , transmitCols = columnLine.split("|")
    receiveCols = map(lambda a:"recv_"+a, receiveCols.split())
    transmitCols = map(lambda a:"trans_"+a, transmitCols.split())

    cols = receiveCols+transmitCols

    faces = {}
    for line in lines[2:]:
        if line.find(":") < 0: continue
        face, data = line.split(":")
        face = ''.join(face.split())
        faceData = dict(zip(cols, data.split()))
        faces[face] = faceData
        
    return faces

"""
负责收集所有的网卡信息
仅仅收集网卡流量的信息，但是无法区分内外网流量，可以在交给上层区分？

iface_stat 是网卡信息，一个字典，记录字段如下：
recv_bytes_speed, trans_bytes_speed, start_utcdate, end_utcdate
recv_bytes_delta, trans_bytes_delta

这两个字段是在起始时间和终止时间之间流量的增量，用于做流量统计
"""
#DELETE?
class NicInfo():
    def __init__(self):
        self.last_stat_time = datetime.utcnow()
        self.last_stat_ifaces = nic_traffic_info_read()
        self.ifaces_stat = dict()
        
        """
        一个内部调用的方法，每次调用都会重新收集并统计下
        新的统计信息将放到self.ifaces_stat中
        """
    def stat(self):
        self.ifaces_stat.clear()
        current_time = datetime.utcnow()
        current_stat_ifaces = nic_traffic_info_read()
        
        for iface_name in current_stat_ifaces:
            current_iface = current_stat_ifaces[iface_name]
            
            if self.last_stat_ifaces.has_key(iface_name):
                last_iface_stat = self.last_stat_ifaces[iface_name]
                last_recv_bytes = int(last_iface_stat['recv_bytes'])
                last_trans_bytes = int(last_iface_stat['trans_bytes'])
            else:
                #A new nic was up
                last_recv_bytes = 0
                last_trans_bytes = 0
            
            recv_bytes_delta = int(current_iface['recv_bytes']) - last_recv_bytes
            trans_bytes_delta = int(current_iface['trans_bytes']) - last_trans_bytes
            
            #Nic down, then up
            if recv_bytes_delta < 0 : recv_bytes_delta = int(current_iface['recv_bytes'])
            if trans_bytes_delta < 0 : trans_bytes_delta =  int(current_iface['trans_bytes'])
            
            #Nic traffic speed
            time_delta = current_time - self.last_stat_time
            recv_bytes_per_second = recv_bytes_delta * 1000 / time_delta.microseconds
            trans_bytes_per_second = trans_bytes_delta * 1000 / time_delta.microseconds
            
            iface_stat = {}
            iface_stat['recv_bytes_speed'] = recv_bytes_per_second
            iface_stat['trans_bytes_speed'] = trans_bytes_per_second
            iface_stat['recv_bytes_delta'] = recv_bytes_delta
            iface_stat['trans_bytes_delta'] = trans_bytes_delta
            iface_stat['start_utcdate'] = self.last_stat_time
            iface_stat['end_utcdate'] = current_time
            
            self.ifaces_stat[iface_name] = iface_stat
        
        self.last_stat_ifaces = current_stat_ifaces
        self.last_stat_time = current_time
        

"""
TODO : 暂时没有考虑网卡DOWN掉之后起来的情况
这个只是测试，简单取的网卡的速度。
"""
def test():
    nic_info = NicInfo()
    
    while True:
        time.sleep(1)
        nic_info.stat()
        print nic_info.ifaces_stat['wlan0']
       
if __name__ == "__main__":
    test()
    
    