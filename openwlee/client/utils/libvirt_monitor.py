#*_* coding=utf8 *_*

"""
描述：此文件用于通过libvirt的接口采集虚拟机的指标。
作者：唐万万

EMAIL:tang_yi_1989@qq.com
"""

import libvirt

from xml.etree import ElementTree
from openwlee import utils

"""
描述：本类只提供虚拟机的简单的统计信息，并不提供变化率等复杂的东西
"""
class DomainInfo():
    def __init__(self, dom, libvirt_con):
        self.__dom = dom
        self.__conn = libvirt_con
        
    @classmethod
    def __all_properties(cls):
        if not hasattr(cls, "_properties"):    
            cls._properties = utils.methods_with_decorator(
                                DomainInfo, 'property')
            
        return cls._properties 
        
    @staticmethod
    def get_xml_nodes(dom_xml, path):
        nodes = list()
        doc = None
        try:
            doc = ElementTree.fromstring(dom_xml)
        except Exception:
            return nodes
        ret = doc.findall(path)
        for node in ret:
            devdst = None
            for child in list(node):#.children:
                if child.tag == 'target':
                    devdst = child.attrib['dev']
            if devdst is None:
                continue
            nodes.append(devdst)
            
        return nodes

    """
    cpu_percent = (cputime1 - cputime2) / (time_delta * cores)
    """    
    @property
    def overview(self):
        (dom_run_state, dom_max_mem_kb, dom_memory_kb,
         dom_nr_virt_cpu, dom_cpu_time) = self.__dom.info()
         
        return {'cputime' : dom_cpu_time, 
                 'ncpus' : dom_nr_virt_cpu,
                 'mem_kb_mx' : dom_max_mem_kb,
                 'mem_kb' : dom_memory_kb }
    
    @property
    def disk_stats(self):
        disk_io_stats = dict()
        
        dom_xml = self.__dom.XMLDesc(0)
        disks = self.get_xml_nodes(dom_xml, './devices/disk')
        
        for disk in disks:
            (rd_req, rd_bytes, wr_req, 
             wr_bytes, errs) = self.__dom.blockStats(disk)
             
            disk_io_stats[disk] = {'rd_bytes' : rd_bytes,  
                                   'wr_bytes' : wr_bytes}
            
        return disk_io_stats
        
    @property
    def nic_stats(self):
        nic_stats = {}
        
        dom_xml = self.__dom.XMLDesc(0)
        nic_devs = self.get_xml_nodes(dom_xml, './devices/interface')
        
        for nic_dev in nic_devs:
            (rx_bytes, rx_packets, rx_errs, rx_drop, 
             tx_bytes,tx_packets, tx_errs, tx_drop) = self.__dom.interfaceStats(nic_dev)
            
            nic_stats[nic_dev] = {'rx_bytes' : rx_bytes, 
                                  'tx_bytes' : tx_bytes}
            
        return nic_stats
    
    def get_dom_stat(self):
        _dict = dict()
        all_properties = self.__class__.__all_properties()
        
        for attr in all_properties:
            _dict[attr] = getattr(self, attr)
            
        return _dict

class LibvirtMonitor():
    def __init__(self):
        self._conn = libvirt.open("qemu:///system")
        
    def get_all_doms_stats(self):
        dom_stats = {}
        
        for id in self._conn.listDomainsID():
            dom = self._conn.lookupByID(id)
            dom_stats[dom.name()] = DomainInfo(dom, self._conn).get_dom_stat()
            
        return dom_stats
    
def test():
    libvirt_monitor = LibvirtMonitor()
    import pprint
    pprint.pprint(libvirt_monitor.get_all_doms_stats())
        
if __name__ == "__main__":
    test()