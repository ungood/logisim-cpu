#!/usr/bin/env python

import binascii

from ctypes import *

class ControlSignals(Structure):
    _fields_ = [
        ("halt", c_bool),
        
        ("mi", c_bool),
        ("mo", c_bool),
        
        ("ri", c_bool),
        ("ro", c_bool),
        
        ("ii", c_bool),
        ("io", c_bool),
        
        ("ci", c_bool),
        ("co", c_bool),
        ("ce", c_bool)
    ]


CI = ControlSignals(ci=True)
CO = ControlSignals(co=True)
print(CI)
print(bytearray(CI))

print(dir(CI))