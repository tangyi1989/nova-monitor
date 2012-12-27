# Copyright 2012 by Tangwanwan
#This is setup tool of openWlee
#It will build the three process:wlee-api is the api function of monitor,wlee-agent is the data node of nova-computer,wlee-daemon 
# is the data collector.
#You can read the doc class to know how to build and run the project.
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
    install_requires = ['eventlet', 'pymongo','paste', 
                        'pasteDeploy','iso8601', 'routes', 
                        'webob', 'extras'],
    scripts=['bin/wlee-api', 
             'bin/wlee-agent', 
             'bin/wlee-daemon',
            ],
)
