#*_* coding=utf8 *_*

"""
描述：此文件用于通过libvirt的接口采集虚拟机的指标。
作者：唐万万

EMAIL:tang_yi_1989@qq.com
"""

import libvirt
from xml.etree import ElementTree

class DomainInfo():
    def __init__(self, dom, libvirt_con):
        self.__dom = dom
        self.__conn = libvirt_con
        
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
    
    @property
    def disk_io_stats(self):
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
    
    def to_dict(self):
        pass

class LibvirtMonitor():
    def __init__(self):
        self._conn = libvirt.open("qemu:///system")
        
    def list_domains(self):
        doms = {}
        for id in self._conn.listDomainsID():
            dom = self._conn.lookupByID(id)
            doms[dom.name()] = DomainInfo(dom, self._conn)
            
        return doms
    

def test():
    libvirt_monitor = LibvirtMonitor()
    doms = libvirt_monitor.list_domains()
    for (dom_name, dom) in doms.iteritems():
        print dom_name
        print dom.nic_stats
        print dom.disk_io_stats
        print dom.cpu_time
        
if __name__ == "__main__":
    test()