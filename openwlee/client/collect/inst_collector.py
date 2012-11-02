#*_* coding=utf8 *_*

from openwlee import utils

import time
from datetime import datetime
from openwlee.client.collect.collector import Collector
from openwlee.client.utils.libvirt_monitor import LibvirtMonitor

class InstStatCollector(Collector):
    def __init__(self):
        self.libvirt_monitor = LibvirtMonitor()
        self.last_stat_time = utils.utc_now()
        self.last_inst_stat = self.libvirt_monitor.get_all_doms_stats()
        
        self.set_tag("vm_info")
    
    def collect(self):
        current_time = utils.utc_now()
        vm_stats = self.libvirt_monitor.get_all_doms_stats()
        inst_stats = vm_stats.copy()
        
        #NOTE 这个循环里面的代码看起来真的不好，谁有什么办法能让这个代码好看点
        for inst_name in vm_stats.keys():
            
            inst_stat = vm_stats[inst_name]
            inst_last_stat = self.last_inst_stat[inst_name]
            collect_inst = inst_stats[inst_name]
            
            #NIC IO speed
            for nic in inst_stat['nic_stats'].keys():
                nic_stat = inst_stat['nic_stats'][nic]
                last_nic_stat = inst_last_stat['nic_stats'][nic]
                
                collect_inst['nic_stats'][nic]['rx_bytes_speed'] = \
                    utils.io_bytes_speed(last_nic_stat['rx_bytes'], 
                                         nic_stat['rx_bytes'],
                                         self.last_stat_time, current_time)
                    
                collect_inst['nic_stats'][nic]['tx_bytes_speed'] = \
                    utils.io_bytes_speed(last_nic_stat['tx_bytes'], 
                                         nic_stat['tx_bytes'],
                                         self.last_stat_time, current_time)
                    
            #DISK IO speed        
            for disk in inst_stat['disk_stats'].keys():
                disk_stat = inst_stat['disk_stats'][disk]
                last_disk_stat = inst_last_stat['disk_stats'][disk]
                
                collect_inst['disk_stats'][disk]['wr_bytes_speed'] = \
                    utils.io_bytes_speed(last_disk_stat['wr_bytes'], 
                                         disk_stat['wr_bytes'],
                                         self.last_stat_time, current_time)
                    
                collect_inst['disk_stats'][disk]['rd_bytes_speed'] = \
                    utils.io_bytes_speed(last_disk_stat['rd_bytes'], 
                                         disk_stat['rd_bytes'],
                                         self.last_stat_time, current_time)
                    
            #CPU percent
            last_cputime = inst_last_stat['overview']['cputime']
            cputime = inst_stat['overview']['cputime']
            ncpus = inst_stat['overview']['ncpus']
            collect_inst['overview']['cpu_percent'] = \
                utils.cpu_percent(last_cputime, cputime, self.last_stat_time, 
                                  current_time, ncpus)
                    
        self.last_inst_stat = vm_stats
        self.last_stat_time = current_time
        
        return inst_stats
