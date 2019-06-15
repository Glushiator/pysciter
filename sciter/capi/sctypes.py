u"""Sciter platform-dependent types."""

from __future__ import absolute_import
import sys
import ctypes

from ctypes import (POINTER,
                    c_char, c_byte, c_ubyte,
                    c_void_p, c_char_p,
                    c_int32, c_uint32, c_int64, c_uint64,
                    c_longlong, c_ulonglong, c_double,
                    sizeof, c_size_t, c_ssize_t)


# 'win32', 'darwin', 'linux'
SCITER_OS = sys.platform
SCITER_WIN = SCITER_OS == u'win32'
SCITER_OSX = SCITER_OS == u'darwin'
SCITER_LNX = SCITER_OS in (u'linux', u'linux2')


def _wstrlen(address):
    import sys
    from ctypes import pointer, c_int16
    memory_location = pointer(c_int16.from_address(address))
    for n in xrange(0, sys.maxint):
        if memory_location[n] == 0:
            return n
    return -1


def utf16tostr(addr, size=-1):
    u"""Read UTF-16 string from memory and encode as python string."""
    if addr is None:
        return None
    cb = size if size > 0 else (_wstrlen(addr) * 2)
    bstr = ctypes.string_at(addr, cb)
    return bstr.decode(u'utf-16le')


class c_utf16_p(ctypes.c_char_p):
    u"""A ctypes wrapper for UTF-16 string pointer."""
    # Taken from https://stackoverflow.com/a/35507014/736762, thanks to @eryksun.
    def __init__(self, value=None):
        super(c_utf16_p, self).__init__()
        if value is not None:
            self.value = value

    @property
    def value(self,
              c_void_p=ctypes.c_void_p):
        addr = c_void_p.from_buffer(self).value
        return utf16tostr(addr)

    @value.setter
    def value(self, value,
              c_char_p=ctypes.c_char_p):
        value = value.encode(u'utf-16le') + '\x00'
        c_char_p.value.__set__(self, value)

    @classmethod
    def from_param(cls, obj):
        if isinstance(obj, unicode):
            obj = obj.encode(u'utf-16le') + '\x00'
        return super(c_utf16_p, cls).from_param(obj)

    @classmethod
    def _check_retval_(cls, result):
        return result.value
    pass


class UTF16LEField(object):
    u"""Structure member wrapper for UTF-16 string pointers."""
    # Taken from https://stackoverflow.com/a/35507014/736762, thanks to @eryksun.
    def __init__(self, name):
        self.name = name

    def __get__(self, obj, cls,
                c_void_p=ctypes.c_void_p,
                addressof=ctypes.addressof):
        field_addr = addressof(obj) + getattr(cls, self.name).offset
        addr = c_void_p.from_address(field_addr).value
        return utf16tostr(addr)

    def __set__(self, obj, value):
        value = value.encode(u'utf-16le') + '\x00'
        setattr(obj, self.name, value)
    pass


if SCITER_WIN:
    # sciter.dll since 4.0.0.0
    SCITER_DLL_NAME = u"sciter"
    SCITER_DLL_EXT = u".dll"

    SCFN = ctypes.WINFUNCTYPE
    SC_CALLBACK = ctypes.WINFUNCTYPE

    HWINDOW = c_void_p  # HWND
    HDC = c_void_p      # HDC

    BOOL = c_int32
    LPCWSTR = LPWSTR = ctypes.c_wchar_p

    ID2D1RenderTarget = c_void_p
    ID2D1Factory = c_void_p
    IDWriteFactory = c_void_p

    IDXGISwapChain = c_void_p
    IDXGISurface = c_void_p

elif SCITER_OSX:
    # sciter-osx-32 since 3.3.1.8
    SCITER_DLL_NAME = u"sciter-osx-64" if sys.maxsize > 2**32 else u"sciter-osx-32"
    SCITER_DLL_EXT = u".dylib"

    SCFN = ctypes.CFUNCTYPE
    SC_CALLBACK = ctypes.CFUNCTYPE

    HWINDOW = c_void_p  # NSView*
    HDC = c_void_p      # CGContextRef

    BOOL = c_byte
    LPCWSTR = LPWSTR = c_utf16_p

elif SCITER_LNX:
    # libsciter since 3.3.1.7
    # libsciter-gtk.so instead of libsciter-gtk-64.so since 4.1.4
    SCITER_DLL_NAME = u"libsciter-gtk"
    SCITER_DLL_EXT = u".so"

    SCFN = ctypes.CFUNCTYPE
    SC_CALLBACK = ctypes.CFUNCTYPE

    HWINDOW = c_void_p  # GtkWidget*
    HDC = c_void_p      # cairo_t

    BOOL = c_byte
    LPCWSTR = LPWSTR = c_utf16_p


# Common types

VOID = None
nullptr = POINTER(c_int32)()

BYTE = c_byte
INT = c_int32
UINT = c_uint32
INT64 = c_int64
tiscript_value = c_uint64

# must be pointer-wide
# WPARAM is defined as UINT_PTR (unsigned type)
# LPARAM is defined as LONG_PTR (signed type)
WPARAM = c_size_t
LPARAM = c_ssize_t

UINT_PTR = c_size_t
LRESULT = c_ssize_t

PBOOL = LPBOOL = POINTER(BOOL)
LPCBYTE = c_char_p
LPCSTR = LPSTR = c_char_p
LPCVOID = LPVOID = c_void_p
LPUINT = POINTER(UINT)


class RECT(ctypes.Structure):
    u"""Rectangle coordinates structure."""
    _fields_ = [(u"left", c_int32),
                (u"top", c_int32),
                (u"right", c_int32),
                (u"bottom", c_int32)]
tagRECT = _RECTL = RECTL = RECT
PRECT = LPRECT = POINTER(RECT)


class POINT(ctypes.Structure):
    u"""Point coordinates structure."""
    _fields_ = [(u"x", c_int32),
                (u"y", c_int32)]
tagPOINT = _POINTL = POINTL = POINT
PPOINT = LPPOINT = POINTER(POINT)


class SIZE(ctypes.Structure):
    u"""SIZE structure for width and height."""
    _fields_ = [(u"cx", c_int32),
                (u"cy", c_int32)]
tagSIZE = SIZEL = SIZE
PSIZE = LPSIZE = POINTER(SIZE)


class MSG(ctypes.Structure):
    u"""MSG structure for windows message queue."""
    _fields_ = [(u"hWnd", HWINDOW),
                (u"message", c_uint32),
                (u"wParam", WPARAM),
                (u"lParam", LPARAM),
                (u"time", c_uint32),
                (u"pt", POINT)]

PMSG = LPMSG = POINTER(MSG)
