#*_* coding=utf8 *_*

"""
描述：编写一个能统计连接数量，input connection, output connection的统计，
暂时不考虑新能问题，如果性能出现问题，之后改进性能。

作者：唐万万
邮箱：tang_yi_1989@qq.com
"""

import datetime
from cStringIO import StringIO

class LinuxNetStat():
    def __init__(self):
        pass
    
    def parse_stat_line(self, line):
        line = line.split('\t')
    
    def nf_connntrack_test(self):
        before = datetime.datetime.now()
        contrack_file = file('/proc/net/nf_conntrack')
        stat_lines = contrack_file.readlines()
        for line in stat_lines:
            pass
        

