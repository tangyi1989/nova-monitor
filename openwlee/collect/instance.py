#*_* coding=utf8 *_*

import time
from datetime import datetime
from openwlee.collect.collector import Collector
from openwlee.collect import utils
from openwlee import utils as openwlee_utils

from openwlee.peek.libvirt_monitor import LibvirtMonitor

class InstanceStatCollector(Collector):
    def __init__(self):
        self.libvirt_monitor = LibvirtMonitor()
        self.last_stat_time = openwlee_utils.utc_now()
        self.last_inst_stat = self.libvirt_monitor.get_all_doms_stats()
        
        self.set_tag("vm_perf_data")
    
    def stat_vm_info(self):
        current_time = openwlee_utils.utc_now()
        vm_stats = self.libvirt_monitor.get_all_doms_stats()
        inst_stats = vm_stats.copy()
        
        #NOTE 这个循环里面的代码看起来真的不好，谁有什么办法能让这个代码好看点
        for inst_name in vm_stats.keys():
            
            inst_stat = vm_stats[inst_name]
            inst_last_stat = self.last_inst_stat[inst_name]
            collect_inst = inst_stats[inst_name]
            
            #NIC IO rate
            for nic in inst_stat['nic_stats'].keys():
                nic_stat = inst_stat['nic_stats'][nic]
                last_nic_stat = inst_last_stat['nic_stats'][nic]
                
                collect_inst['nic_stats'][nic]['rx_bytes_rate'] = \
                    utils.io_bytes_rate(last_nic_stat['rx_bytes'], 
                                         nic_stat['rx_bytes'],
                                         self.last_stat_time, current_time)
                    
                collect_inst['nic_stats'][nic]['tx_bytes_rate'] = \
                    utils.io_bytes_rate(last_nic_stat['tx_bytes'], 
                                         nic_stat['tx_bytes'],
                                         self.last_stat_time, current_time)
                    
            #DISK IO rate        
            for disk in inst_stat['disk_stats'].keys():
                disk_stat = inst_stat['disk_stats'][disk]
                last_disk_stat = inst_last_stat['disk_stats'][disk]
                
                collect_inst['disk_stats'][disk]['wr_bytes_rate'] = \
                    utils.io_bytes_rate(last_disk_stat['wr_bytes'], 
                                         disk_stat['wr_bytes'],
                                         self.last_stat_time, current_time)
                    
                collect_inst['disk_stats'][disk]['rd_bytes_rate'] = \
                    utils.io_bytes_rate(last_disk_stat['rd_bytes'], 
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
    
    def collect(self):
        inst_stats = self.stat_vm_info()
        vm_data = []
        
        #Convert dict to list and merge multiple items 
        for inst, stat in inst_stats.items():
            vm_item = dict()
            vm_item['name'] = inst
            
            #Hard disk data merge
            vm_item['hd_wr_bytes_rate'] = 0
            vm_item['hd_rd_bytes_rate'] = 0
            for disk, disk_stat in stat['disk_stats'].items():
                vm_item['hd_wr_bytes_rate'] += disk_stat['wr_bytes_rate']
                vm_item['hd_rd_bytes_rate'] += disk_stat['rd_bytes_rate']
                
            #Network card data merge
            vm_item['nic_rx_bytes_rate'] = 0
            vm_item['nic_tx_bytes_rate'] = 0
            for nic, nic_stat in stat['nic_stats'].items():
                vm_item['nic_rx_bytes_rate'] += nic_stat['rx_bytes_rate']
                vm_item['nic_tx_bytes_rate'] += nic_stat['tx_bytes_rate']
            
            #Other statistic
            vm_item['cpu_used_percent'] = stat['overview']['cpu_percent']
            vm_item['ram_mb_used'] = stat['overview']['mem_kb'] / 1024
            
            vm_data.append(vm_item)
        
        return vm_data
