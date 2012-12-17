import os
import sys
import setuptools

from setuptools import find_packages

setuptools.setup(
    name="openwlee",
    version="2012.10",
    author="Li Lei, Tang Yi",
    author_email="101859673@qq.com, tang_yi_1989@qq.com",
    description="Monitor virtual machine for openstack",
    packages=find_packages(exclude=['test', 'bin']),
    install_requires = ['eventlet', 'pymongo'],
    scripts=['bin/wlee-api', 
             'bin/wlee-agent', 
             'bin/wlee-daemon',
            ],
)