#*_* coding=utf8 *_*

"""
描述：没有分离的美感，只有简洁的代码，能用再说代码美丑。
"""

import time
from datetime import datetime
from openwlee.client.collect.libvirt_monitor import LibvirtMonitor

def io_bytes_speed(start_bytes, end_bytes, start_time, end_time):
    delta_time = end_time - start_time
    delta_bytes = end_bytes - start_bytes
    if delta_bytes < 0 :
        delta_bytes = end_bytes
        
    return delta_bytes * 1000000 / delta_time.microseconds

def clear_screen():
    print "\033[2J"

def stat_loops():
    libvirt_monitor = LibvirtMonitor()
    
    last_stat_time = datetime.now()
    last_vm_stats = libvirt_monitor.get_all_doms_stats()
    while True:
        time.sleep(1)
        
        current_time = datetime.now()
        vm_stats = libvirt_monitor.get_all_doms_stats()
        
        clear_screen()
        for (inst, stat) in vm_stats.items():
            if last_vm_stats.has_key(inst):
                print inst
                
                last_nic_stat = last_vm_stats[inst]['nic_stats']
                for (nic, io_stats) in stat['nic_stats'].items():
                    receive_spped = io_bytes_speed(last_nic_stat[nic]['rx_bytes'],
                                                   io_stats['rx_bytes'], last_stat_time, current_time)
                    trans_speed = io_bytes_speed(last_nic_stat[nic]['tx_bytes'], 
                                                 io_stats['tx_bytes'], last_stat_time, current_time)
                    
                    print 'NIC : %s Receive Speed %d bytes/s Transfer Speed %d bytes/s' %\
                                (nic, receive_spped, trans_speed)
                    
                last_disk_stat = last_vm_stats[inst]['disk_stats']
                for (disk, io_stats) in stat['disk_stats'].items():
                    read_speed = io_bytes_speed(last_disk_stat[disk]['rd_bytes'], 
                                                io_stats['rd_bytes'], last_stat_time, current_time)
                    write_speed = io_bytes_speed(last_disk_stat[disk]['wr_bytes'], 
                                                 io_stats['wr_bytes'], last_stat_time, current_time)
                    
                    print 'DISK : %s Read Speed %d bytes/s Write Speed %d bytes/s' % (disk, read_speed, write_speed)
                    
        last_stat_time = current_time
        last_vm_stats = vm_stats 
        
if __name__ == "__main__":
    stat_loops()