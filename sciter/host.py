u"""Sciter host application helpers."""

from __future__ import absolute_import
import ctypes
import os.path

from sciter.capi.scdef import *
from sciter.capi.sctypes import HWINDOW

import sciter
import sciter.dom

import sys

_api = sciter.SciterAPI()


class Host(object):
    u"""Standard implementation of SCITER_CALLBACK_NOTIFY handler."""

    def __init__(self):
        u"""."""
        super(Host, self).__init__()
        self.hwnd = None
        self.root = None
        pass

    def __call__(self, name, *args):
        u"""Alias for self.call_function()."""
        return self.call_function(name, *args)

    def setup_callback(self, hwnd):
        u"""Set callback for sciter engine events."""
        if not hwnd:
            raise ValueError(u"Invalid window handle provided.")
        self.hwnd = hwnd
        self.root = self.get_root()  # if called on existing document
        self._sciter_handler_proc = SciterHostCallback(self.handle_notification)
        _api.SciterSetCallback(hwnd, self._sciter_handler_proc, ctypes.c_void_p(0))
        pass

    def setup_debug(self, hwnd=None):
        u"""Setup debug output function for specific window or globally."""
        ok = _api.SciterSetOption(hwnd, SCITER_RT_OPTIONS.SCITER_SET_DEBUG_MODE, True)
        self._sciter_debug_proc = DEBUG_OUTPUT_PROC(self.on_debug_output)
        _api.SciterSetupDebugOutput(hwnd, None, self._sciter_debug_proc)
        pass

    def set_option(self, option, value):
        u"""Set various sciter engine options, see the SCITER_RT_OPTIONS."""
        hwnd = self.hwnd
        if option in (SCITER_RT_OPTIONS.SCITER_SET_GPU_BLACKLIST, SCITER_RT_OPTIONS.SCITER_SET_GFX_LAYER, SCITER_RT_OPTIONS.SCITER_SET_UX_THEMING):
            hwnd = None
        ok = _api.SciterSetOption(hwnd, option, value)
        if not ok:
            raise sciter.SciterError(u"Could not set option " + unicode(option) + u"=" + unicode(value))
        return self

    def set_home_url(self, url):
        u"""Set sciter window home url."""
        ok = _api.SciterSetHomeURL(self.hwnd, url)
        if not ok:
            raise sciter.SciterError(u"Could not home url " + unicode(url))
        return self

    def set_media_type(self, media_type):
        u"""Set media type of this sciter instance."""
        ok = _api.SciterSetMediaType(self.hwnd, media_type)
        if not ok:
            raise sciter.SciterError(u"Could not set media type " + unicode(media_type))
        return self

    def set_media_vars(self, media):
        u"""Set media variables of this sciter instance."""
        v = sciter.Value(media)
        ok = _api.SciterSetMediaVars(self.hwnd, v)
        if not ok:
            raise sciter.SciterError(u"Could not set media vars " + unicode(media))
        return self

    def set_master_css(self, css_str, append):
        u"""Set Master style sheet."""
        utf = css_str.encode(u'utf-8')
        if append:
            ok = _api.SciterAppendMasterCSS(utf, len(utf))
        else:
            ok = _api.SciterSetMasterCSS(utf, len(utf))
        if not ok:
            raise sciter.SciterError(u"Could not set master CSS")
        return self

    def set_css(self, css_str, base_url, media_type):
        u"""Set (reset) style sheet of current document."""
        utf = css_str.encode(u'utf-8')
        ok = _api.SciterSetCSS(self.hwnd, utf, len(utf), base_url, media_type)
        if not ok:
            raise sciter.SciterError(u"Could not set CSS")
        return self

    def get_hwnd(self):
        u"""Get window handle."""
        return self.hwnd

    def load_file(self, uri, normalize=True):
        u"""Load HTML document from file."""
        if normalize and u"://" not in uri:
            uri = u"file://" + os.path.abspath(uri).replace(u"\\", u"/")
        ok = _api.SciterLoadFile(self.hwnd, uri)
        if not ok:
            raise sciter.SciterError(u"Unable to load file " + uri)
        self.root = self.get_root()
        return self

    def load_html(self, html, uri=None):
        u"""Load HTML document from memory."""
        if not isinstance(html, str):
            raise TypeError(u"html must be a bytes type")
        cb = len(html)
        pb = ctypes.c_char_p(html)
        ok = _api.SciterLoadHtml(self.hwnd, pb, cb, uri)
        if not ok:
            raise sciter.SciterError(u"Unable to load html " + unicode(uri))
        self.root = self.get_root()
        return self

    def get_root(self):
        u"""Get window root DOM element."""
        he = sciter.dom.HELEMENT()
        ok = _api.SciterGetRootElement(self.hwnd, ctypes.byref(he))
        return sciter.dom.Element(he) if he else None

    def eval_script(self, script, name=None):
        u"""Evaluate script in context of current document."""
        rv = sciter.Value()
        ok = _api.SciterEval(self.hwnd, script, len(script), rv)
        sciter.Value.raise_from(rv, ok != False, name if name else u'Host.eval')
        return rv

    def call_function(self, name, *args):
        u"""Call scripting function defined in the global namespace."""
        rv = sciter.Value()
        argc, argv, this = sciter.Value.pack_args(*args)
        ok = _api.SciterCall(self.hwnd, name.encode(u'utf-8'), argc, argv, rv)
        sciter.Value.raise_from(rv, ok != False, name)
        return rv

    def data_ready(self, uri, data, request_id=None, hwnd=None):
        u"""This function is used as response to SCN_LOAD_DATA request."""
        if not hwnd:
            hwnd = self.hwnd
        if request_id is not None:
            ok = _api.SciterDataReadyAsync(hwnd, uri, data, len(data), request_id)
        else:
            ok = _api.SciterDataReady(hwnd, uri, data, len(data))
        if not ok:
            raise sciter.SciterError(u"Unable to pass data for " + uri)
        pass


    ## @name following functions can be overloaded
    def on_load_data(self, nm):
        u"""Notifies that Sciter is about to download a referred resource."""
        pass

    def on_data_loaded(self, nm):
        u"""This notification indicates that external data (for example image) download process completed."""
        pass

    def on_attach_behavior(self, nm):
        u"""This notification is sent on parsing the document and while processing elements having non empty `style.behavior` attribute value."""
        pass

    def on_debug_output(self, tag, subsystem, severity, text, text_len):
        u"""This output function will be used for reprting problems found while loading html and css documents."""
        sysname = OUTPUT_SUBSYTEMS(subsystem).name.lower()
        sevname = OUTPUT_SEVERITY(severity).name.lower()
        if not sciter.SCITER_WIN:
            text = text.value
        message = text.replace(u"\r", u"\n").rstrip()
        if message:
            destination = sys.stdout if sevname == u'info' else sys.stderr
            print >>destination, u"{}:{}: {}".format(sevname, sysname, message)
        pass

    def handle_notification(self, pnm, param):
        u"""Sciter notification handler."""
        rv = 0
        nm = pnm.contents
        if nm.code == SciterNotification.SC_LOAD_DATA:
            rv = self.on_load_data(ctypes.cast(pnm, ctypes.POINTER(SCN_LOAD_DATA)).contents)
        elif nm.code == SciterNotification.SC_DATA_LOADED:
            rv = self.on_data_loaded(ctypes.cast(pnm, ctypes.POINTER(SCN_DATA_LOADED)).contents)
        elif nm.code == SciterNotification.SC_ATTACH_BEHAVIOR:
            rv = self.on_attach_behavior(ctypes.cast(pnm, ctypes.POINTER(SCN_ATTACH_BEHAVIOR)).contents)
        assert(rv is None or isinstance(rv, int))
        return 0 if rv is None else rv
    pass
