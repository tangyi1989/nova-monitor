#*_* coding=utf *_*

"""
Description : This file is used to get information from libvirt.

Note : The code in this file is ugly, who want refactor it.

Author : Tang Yi
EMAIL:tang_yi_1989@qq.com
"""

import time
from eventlet import tpool
from datetime import datetime, timedelta
from xml.etree import ElementTree

from openwlee.tools import utils
from openwlee import utils as openwlee_utils
from openwlee.openstack.common import cfg
from openwlee.openstack.common import timeutils
from openwlee.openstack.common import log as logging

libvirt_opts = [
    cfg.BoolOpt('libvirt_nonblocking',
                default=True,
                help='Use a separated OS thread pool to realize non-blocking'
                     ' libvirt calls'),
]

cfg.CONF.register_opts(libvirt_opts)
LOG = logging.getLogger("openwlee.tools.libvirt")

libvirt = None

class DomainInfo():
    """ Get domain info from libvirt, just support simple statistic info. """
    def __init__(self, dom, libvirt_con):
        self.__dom = dom
        self.__conn = libvirt_con
        
    @classmethod
    def __all_properties(cls):
        if not hasattr(cls, "_properties"):    
            cls._properties = openwlee_utils.methods_with_decorator(
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

class LibvirtManager():
    def __init__(self):
        
        global libvirt
        if libvirt is None:
            libvirt = __import__('libvirt')
        
        self.uri = "qemu:///system"
        self._wrapped_conn = None
        
    def _test_connection(self):
        try:
            self._wrapped_conn.getCapabilities()
            return True
        except libvirt.libvirtError as e:
            if (e.get_error_code() == libvirt.VIR_ERR_SYSTEM_ERROR and
                e.get_error_domain() in (libvirt.VIR_FROM_REMOTE,
                                         libvirt.VIR_FROM_RPC)):
                LOG.debug(_('Connection to libvirt broke'))
                return False
            raise
    
    def _get_connection(self):
        if not self._wrapped_conn or not self._test_connection():
            LOG.debug(_('Connecting to libvirt: %s'), self.uri)
            if not cfg.CONF.libvirt_nonblocking:
                self._wrapped_conn = self._connect(self.uri)
            else:
                self._wrapped_conn = tpool.proxy_call(
                    (libvirt.virDomain, libvirt.virConnect),
                    self._connect, self.uri)

        return self._wrapped_conn
    
    _conn = property(_get_connection)
    
    def _connect(self, uri):
        try:
            return libvirt.openReadOnly(uri)
        except libvirt.libvirtError as ex:
            LOG.exception(_("Connection to libvirt failed: %s"), ex)
            pass
        
    def get_all_doms_stats(self):
        dom_stats = {}
        
        for id in self._conn.listDomainsID():
            dom = self._conn.lookupByID(id)
            dom_stats[dom.name()] = DomainInfo(dom, self._conn).get_dom_stat()
            
        return dom_stats
    
@openwlee_utils.singleton
class LibvirtUtil():
    """
    It would be used by many monitor, this class is designed use singleton 
    pattern for performance reason. If it is used several times recently, it 
    would use cached data.
    """
    def __init__(self, expired_seconds=5):
        self.libvirt_manager = LibvirtManager()
        self.last_stat_time = timeutils.utcnow()
        self.last_inst_stat = self.libvirt_manager.get_all_doms_stats()
        self.expired_seconds = expired_seconds
        self.cached_stats = None
    
    """
    Get vm_info(statistic and performance info).
    If cached data is not expired, return cached data,
    otherwise get the lasted data from libvirt and return.
    """
    def get_all_instance_info(self):
        stat_date = self.last_stat_time
        now_date = timeutils.utcnow()
        exipred_date = stat_date + timedelta(seconds = self.expired_seconds)
        expired = now_date > exipred_date
        
        if self.cached_stats == None or expired:
            self.cached_stats = self.stat_vm_info_from_libvirt()
            stat_date = self.last_stat_time
        
        return (self.cached_stats, stat_date)
    
    """
    Get instance statistic info from libvirtd then calculate 
    performance info by passed time.
    """
    def stat_vm_info_from_libvirt(self):
        current_time = timeutils.utcnow()
        vm_stats = self.libvirt_manager.get_all_doms_stats()
        inst_stats = vm_stats.copy()
        
        #NOTE 
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