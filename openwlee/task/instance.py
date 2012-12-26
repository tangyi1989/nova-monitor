
from openwlee.task import base
from openwlee.tools.libvirt import LibvirtUtil

class InstancePerformanceTask(base.Task):
    """
    This task is responsible for collect instances' performance data. 
    """
    
    def initialize(self):
        self.libvirt_util = LibvirtUtil()
        
    def get_perf_data(self, inst_stats):
        instance_data_list = []
        
        #Convert dict to list and merge multiple items 
        for inst_name, stat in inst_stats.items():
            instance_data = dict()
            instance_data['name'] = inst_name
            
            #Hard disk data merge
            instance_data['hd_wr_bytes_rate'] = 0
            instance_data['hd_rd_bytes_rate'] = 0
            for disk, disk_stat in stat['disk_stats'].items():
                instance_data['hd_wr_bytes_rate'] += disk_stat['wr_bytes_rate']
                instance_data['hd_rd_bytes_rate'] += disk_stat['rd_bytes_rate']
                
            #Network card data merge
            instance_data['nic_rx_bytes_rate'] = 0
            instance_data['nic_tx_bytes_rate'] = 0
            for nic, nic_stat in stat['nic_stats'].items():
                instance_data['nic_rx_bytes_rate'] += nic_stat['rx_bytes_rate']
                instance_data['nic_tx_bytes_rate'] += nic_stat['tx_bytes_rate']
            
            #Other statistic
            instance_data['cpu_used_percent'] = stat['overview']['cpu_percent']
            instance_data['ram_mb_used'] = stat['overview']['mem_kb'] / 1024
            
            instance_data_list.append(instance_data)
        
        return instance_data_list
        
    def execute(self):
        inst_stats, date = self.libvirt_util.get_all_instance_info()
        perf_data = self.get_perf_data(inst_stats)
        self.report('instance_perf', perf_data, date)

class InstanceStatisticTask(base.Task):
    """
    This task is responsible for collect instances' statistic data, like disk used, 
    network traffic info.
    """
    def initialize(self):
        self.libvirt_util = LibvirtUtil()
    
    def get_statistic_data(self, inst_stats):
        instance_data_list = []
        
        #Convert dict to list and merge multiple items 
        for inst_name, stat in inst_stats.items():
            instance_data = dict()
            instance_data['name'] = inst_name
            instance_data['disk_stats'] = {}
            
            for dev, disk_stat in stat['disk_stats'].items():
                instance_data['disk_stats'][dev] = {}
                instance_data['disk_stats'][dev]['total'] = disk_stat['total']
                instance_data['disk_stats'][dev]['used'] = disk_stat['used']
                
            instance_data_list.append(instance_data)
            
        return instance_data_list
    
    def execute(self):
        inst_stats, date = self.libvirt_util.get_all_instance_info()
        statistic_data = self.get_statistic_data(inst_stats)
        self.report('instance_statistic', statistic_data, date)