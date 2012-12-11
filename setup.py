import os
import setuptools
import sys


def read_file(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()

setuptools.setup(
    name="openwlee",
    version="2012.10",
    author="Li Lei, Tang Yi",
    author_email="101859673@qq.com, tang_yi_1989@qq.com",
    description="Monitor virtual machine for openstack",
    packages=["openwlee"],
    scripts=['bin/wlee-api', 
             'bin/wlee-agent', 
             'bin/wlee-daemon',
            ],
)