u"""TIScript Virtual Machine Runtime.

Incomplete.
"""
from __future__ import absolute_import
import ctypes

HVM = ctypes.c_void_p
value = ctypes.c_uint64


class tiscript_native_interface(ctypes.Structure):
    u"""."""
    _fields_ = [
        (u"create_vm", ctypes.c_void_p),
        # TODO: rest of TIScript API
        ]
