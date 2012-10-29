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
        faceData = dict(zip(cols, data.split()))
        faces[face] = faceData
        
    return faces

"""
负责收集所有的网卡信息
"""
class NicInfo():
    def __init__(self):
        pass

"""
TODO : 暂时没有考虑网卡DOWN掉之后起来的情况
这个只是测试，简单取的网卡的速度。
"""
if __name__ == "__main__":
    stat_ifaces = dict()
    last_stat_ifaces = nic_traffic_info_read()
    last_stat_time = datetime.now()
    
    while True:
        time.sleep(1)
        print '------------------------------------------------'
        current_time = datetime.now()
        current_stat_ifaces = nic_traffic_info_read()
        
        for iface_name in current_stat_ifaces.keys():
            
            if last_stat_ifaces.has_key(iface_name):
                current_iface = current_stat_ifaces[iface_name]
                last_iface = last_stat_ifaces[iface_name]
                
                recv_bytes_delta = int(current_iface['recv_bytes']) - int(last_iface['recv_bytes'])
                trans_bytes_delta = int(current_iface['trans_bytes']) - int(last_iface['trans_bytes'])
                time_delta = current_time - last_stat_time
                
                recv_bytes_per_second = recv_bytes_delta * 1000 / time_delta.microseconds
                trans_bytes_per_second = trans_bytes_delta * 1000 / time_delta.microseconds
                
                print '%s : Recv Speed %d KB/s' % (iface_name, recv_bytes_per_second / 1024)
                print '%s : Trans Speed %d KB/s' % (iface_name, trans_bytes_per_second / 1024)
                
        last_stat_ifaces = current_stat_ifaces
        last_stat_time = current_time
    
    