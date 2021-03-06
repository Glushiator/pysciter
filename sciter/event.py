u"""Behaviors support (a.k.a windowless controls)."""

from __future__ import absolute_import
import ctypes

import sciter.capi.scdef

from sciter.capi.scbehavior import *
from sciter.capi.scdom import SCDOM_RESULT, HELEMENT

_api = sciter.SciterAPI()


class EventHandler(object):
    u"""DOM event handler which can be attached to any DOM element."""

    ALL_EVENTS = EVENT_GROUPS.HANDLE_ALL
    DEFAULT_EVENTS = EVENT_GROUPS.HANDLE_INITIALIZATION | EVENT_GROUPS.HANDLE_SIZE | EVENT_GROUPS.HANDLE_BEHAVIOR_EVENT | EVENT_GROUPS.HANDLE_SCRIPTING_METHOD_CALL

    def __init__(self, window=None, element=None, subscription=DEFAULT_EVENTS):
        u"""Attach event handler to dom::element or sciter::window."""
        super(EventHandler, self).__init__()
        self.subscription = subscription
        self.element = None
        self._attached_to_window = None
        self._attached_to_element = None
        self._dispatcher = dict()
        self.set_dispatch_options()
        if window or element:
            self.attach(window, element, subscription)
        pass

    def __del__(self):
        assert(not self.element)
        pass

    def attach(self, window=None, element=None, subscription=DEFAULT_EVENTS):
        u"""Attach event handler to dom::element or sciter::window."""
        assert(window or element)
        self.subscription = subscription
        self._event_handler_proc = sciter.capi.scdef.ElementEventProc(self._element_proc)
        tag = id(self)
        if window:
            self._attached_to_window = window
            ok = _api.SciterWindowAttachEventHandler(window, self._event_handler_proc, tag, subscription)
            if ok != SCDOM_RESULT.SCDOM_OK:
                raise sciter.SciterError(u"Could not attach to window")
        elif element:
            self._attached_to_element = element
            ok = _api.SciterAttachEventHandler(element, self._event_handler_proc, tag)
            if ok != SCDOM_RESULT.SCDOM_OK:
                raise sciter.SciterError(u"Could not attach to element")
        pass

    def detach(self):
        u"""Detach event handler from dom::element or sciter::window."""
        tag = id(self)
        if self._attached_to_window:
            ok = _api.SciterWindowDetachEventHandler(self._attached_to_window, self._event_handler_proc, tag)
            if ok != SCDOM_RESULT.SCDOM_OK:
                raise sciter.SciterError(u"Could not detach from window")
            self._attached_to_window = None
        elif self._attached_to_element:
            ok = _api.SciterDetachEventHandler(self._attached_to_element, self._event_handler_proc, tag)
            if ok != SCDOM_RESULT.SCDOM_OK:
                raise sciter.SciterError(u"Could not attach from element")
            self._attached_to_element = None
        pass

    def dispatch(self, name, args):
        u"""Route script call to python handler directly."""
        # fn = getattr(self, name, None)
        # if fn is not None:
        #     return fn(*args)
        pass

    def set_dispatch_options(self, enable=True, require_attribute=True, dynamic_handlers=False):
        u"""Set the various script dispatch options."""
        self._dispatcher[u'enabled'] = enable                # enable or disable dispatching of script calls to class handlers
        self._dispatcher[u'runtime'] = dynamic_handlers      # class handlers may be added at runtime, so we won't cache it
        self._dispatcher[u'require'] = require_attribute     # class handlers require @sciter.script attribute
        self._dispatcher[u'handlers'] = {}
        self._dispatcher_update(True)
        return self

    ## @name following functions can be overloaded
    ## @param he - a `this` element for behavior attached to
    ## @param source - source element of this event
    ## @param target - target element of this event

    def attached(self, he):
        u"""Called when handler was attached to element."""
        pass

    def detached(self, he):
        u"""Called when handler was detached from element."""
        pass

    def document_complete(self):
        u"""Notification that document finishes its loading - all requests for external resources are finished."""
        pass

    def document_close(self):
        u"""The last notification before document removal from the DOM."""
        pass

    def on_subscription(self, groups):
        u"""Return list of event groups this event_handler is subscribed to."""
        return self.subscription

    def on_script_call(self, name, args):
        u"""Script calls from CSSS! script and TIScript. Arguments are Sciter types. Return something to prevent @script handlers to be executed."""
        # Return something except None to indicate that function handled (e.g. found).
        pass

    def on_event(self, source, target, code, phase, reason):
        u"""Notification event from builtin behaviors."""
        pass

    def on_data_arrived(self, nm):
        u"""Requested data has been delivered."""
        pass

    ## @}

    def _document_ready(self, target):
        u"""Document created, script namespace initialized. target -> the document."""
        pass

    def _dispatcher_update(self, force=False):
        if not self._dispatcher[u'enabled']:
            return
        if not force and not self._dispatcher[u'runtime']:
            return
        required = self._dispatcher[u'require']
        handlers = {}
        for name in dir(self):
            member = getattr(self, name, None)

            # check optional attribute for name mapping
            attr = getattr(member, u'_from_sciter', False)
            fnname = attr if isinstance(attr, unicode) else name
            if attr or not required:
                handlers[fnname] = member
        self._dispatcher[u'handlers'] = handlers
        pass

    def _on_script_call(self, f):
        # update handlers on every call if needed
        self._dispatcher_update()

        fname = f.name.decode(u'utf-8')
        fn = self._dispatcher[u'handlers'].get(fname)
        rv = None

        # call raw handler first
        if True:
            try:
                args = [sciter.Value(f.argv[i]) for i in xrange(f.argc)]
                rv = self.on_script_call(fname, args)
            except Exception, e:
                import traceback
                traceback.print_exc()
                rv = e

        # if not handled, call decorated method
        if rv is None and fn:
            cfg = getattr(fn, u'_sciter_cfg', {})
            skip_exception = not cfg.get(u'safe', True)
            try:
                if cfg.get(u'convert'):
                    args = sciter.Value.unpack_from(f.argv, f.argc)
                rv = fn(*args)
            except Exception, e:
                import traceback
                traceback.print_exc()
                rv = unicode(e) if skip_exception else e

        # if handled, pack result for Sciter
        if fn or rv is not None:
            sciter.Value.pack_to(f.result, rv)
            return True
        return False

    # event handler native callback
    def _element_proc(self, tag, he, evt, params):
        he = HELEMENT(he)
        if evt == EVENT_GROUPS.SUBSCRIPTIONS_REQUEST:
            p = ctypes.cast(params, ctypes.POINTER(ctypes.c_uint))
            subscribed = self.on_subscription(p.contents)
            if subscribed is not None:
                p.contents = ctypes.c_ulong(int(subscribed))
                return True

        elif evt == EVENT_GROUPS.HANDLE_INITIALIZATION:
            # handle initialization events and route to attached() and detached()
            # NOTE: when attaching to empty window, this called with he == NULL
            p = ctypes.cast(params, ctypes.POINTER(INITIALIZATION_PARAMS))
            if p.contents.cmd == INITIALIZATION_EVENTS.BEHAVIOR_DETACH:
                self.detached(he)
                self.element = None
            elif p.contents.cmd == INITIALIZATION_EVENTS.BEHAVIOR_ATTACH:
                self.element = sciter.Element(he)
                self.attached(he)
            return True

        elif evt == EVENT_GROUPS.HANDLE_BEHAVIOR_EVENT:
            # handle behavior events and route to on_event(), document_complete() and document_close()
            p = ctypes.cast(params, ctypes.POINTER(BEHAVIOR_EVENT_PARAMS))
            m = p.contents
            if m.cmd == BEHAVIOR_EVENTS.DOCUMENT_COMPLETE:
                self.element = sciter.Element(he)
                self.document_complete()
            elif m.cmd == BEHAVIOR_EVENTS.DOCUMENT_CLOSE:
                self.document_close()
                self.element = None
            elif m.cmd == BEHAVIOR_EVENTS.DOCUMENT_READY:
                self._document_ready(HELEMENT(m.heTarget))

            code = (m.cmd & 0xFFF)
            phase = PHASE_MASK(m.cmd & 0xFFFFF000)
            reason = m.reason                   # reason can be CLICK_REASON or EDIT_CHANGED_REASON, so leave it as int
            try:
                event = BEHAVIOR_EVENTS(code)   # not all codes enumerated in BEHAVIOR_EVENTS :-\
            except ValueError:
                event = code
            handled = self.on_event(HELEMENT(m.he), HELEMENT(m.heTarget), event, phase, reason)
            return handled or False

        elif evt == EVENT_GROUPS.HANDLE_SCRIPTING_METHOD_CALL:
            # handle script calls
            p = ctypes.cast(params, ctypes.POINTER(SCRIPTING_METHOD_PARAMS))
            return self._on_script_call(p.contents)

        elif evt == EVENT_GROUPS.HANDLE_DATA_ARRIVED:
            # notification event: data requested by HTMLayoutRequestData just delivered
            p = ctypes.cast(params, ctypes.POINTER(DATA_ARRIVED_PARAMS))
            handled = self.on_data_arrived(p.contents)
            return handled or False

        return False
    pass
