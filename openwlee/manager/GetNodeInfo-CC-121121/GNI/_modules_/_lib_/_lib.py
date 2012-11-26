

'''
#File Name: _lib.py
#Version : v1.0
#Author : Li Desheng
#Time : 2012-10-30
#Usage :
'''
# -*- coding:gbk -*-
import os
from ctypes import *

class _lib_(object):
    def __init__(self,libfile):
        self.lib=cdll.LoadLibrary(libfile)

