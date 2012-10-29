#*_* coding=utf8 *_*

"""
描述：基本上这个文件被设定为一个获取HOST和GUEST信息的文件
作者：唐万万
Email:tang_yi_1989@qq.com
"""
import sys
from nova import context
from nova import exception
from nova import flags
from nova import log as logging
from nova import db
from nova import utils
import socket

def get_all_guest_nw_info():
    guest_nw_info = []
    ctx = context.get_admin_context()
    hostname = "oneiric52"
    instances = db.instance_get_all_by_host(ctx, hostname)
    for inst in instances:
        fixed_ips = db.instance_get_fixed_addresses(ctx, inst['id'])
        guest_nw_info.append({inst['name'] : fixed_ips})
    return guest_nw_info

def get_default_flags():
    utils.default_flagfile()
    flags.FLAGS(sys.argv)

if __name__ == "__main__":
    get_default_flags()
    print get_all_guest_nw_info()
    
    