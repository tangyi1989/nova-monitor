#*_* coding=utf8 *_*

"""
描述：此文件用于通过libvirt的接口采集虚拟机的指标。
作者：唐万万
EMAIL:tang_yi_1989@qq.com
"""

import libvirt

class LibvirtDriver():
    def __init__(self):
        self._conn = libvirt.open("qemu:///system")
        
    def get_vm_connections(self):
        pass
        
    def test(self):
        for id in self._conn.listDomainsID():
            dom = self._conn.lookupByID(id)
            infos = dom.info()
            print 'ID = %d' % id
            print 'Name =  %s' % dom.name()
            print 'State = %d' % infos[0]
            print 'Max Memory = %d' % infos[1]
            print 'Number of virt CPUs = %d' % infos[3]
            print 'CPU Time (in ns) = %d' % infos[2]
            print ' '

def test():
    libvirt_driver = LibvirtDriver()
    libvirt_driver.test()
    
if __name__ == "__main__":
    test()