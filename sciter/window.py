u"""High level window wrapper."""

from __future__ import absolute_import
import sciter.capi.scdef
import sciter.capi.sctypes
import sciter.host
import sciter.event
import sciter.platform

_api = sciter.SciterAPI()


class Window(sciter.platform.BaseWindow, sciter.host.Host, sciter.event.EventHandler):
    u"""Basic Sciter window."""

    def __init__(self, ismain=False, ispopup=False, ischild=False, resizeable=True, parent=None, uni_theme=False, debug=True, pos=None, size=None):
        u"""Create a new window and setup the sciter and dom callbacks."""
        super(Window, self).__init__()
        from sciter.capi.scdef import SCITER_CREATE_WINDOW_FLAGS

        flags = SCITER_CREATE_WINDOW_FLAGS.SW_CONTROLS
        if resizeable:
            flags = flags | SCITER_CREATE_WINDOW_FLAGS.SW_RESIZEABLE
        if ismain:
            flags = flags | SCITER_CREATE_WINDOW_FLAGS.SW_MAIN | SCITER_CREATE_WINDOW_FLAGS.SW_TITLEBAR
        elif ispopup:
            flags = flags | SCITER_CREATE_WINDOW_FLAGS.SW_POPUP
        elif ischild:
            flags = flags | SCITER_CREATE_WINDOW_FLAGS.SW_CHILD

        if uni_theme:
            _api.SciterSetOption(None, sciter.capi.scdef.SCITER_RT_OPTIONS.SCITER_SET_UX_THEMING, True)

        if debug:
            flags = flags | SCITER_CREATE_WINDOW_FLAGS.SW_ENABLE_DEBUG
            self.setup_debug()

        self.window_flags = flags
        self._title_changed = False

        rect = sciter.capi.sctypes.RECT()
        if pos is not None:
            rect.left = pos[0]
            rect.top = pos[1]
            if size is None:
                raise ValueError(u"`size` is required if `pos` is provided!")
        if size is not None:
            rect.right = size[0]
            rect.bottom = size[1]
        if not pos and not size:
            rect = None

        self.hwnd = self._create(flags, rect=rect, parent=None)
        if not self.hwnd:
            raise sciter.SciterError(u"Could not create window")

        self.setup_callback(self.hwnd)
        self.attach(window=self.hwnd)
        pass

    def collapse(self, hide=False):
        u"""Minimize or hide window."""
        return super(Window, self).collapse(hide)

    def expand(self, maximize=False):
        u"""Show or maximize window."""
        return super(Window, self).expand(maximize)

    def dismiss(self):
        u"""Close window."""
        return super(Window, self).dismiss()

    def set_title(self, title):
        u"""Set native window title."""
        self._title_changed = True
        return super(Window, self).set_title(title)

    def get_title(self):
        u"""Get native window title."""
        return super(Window, self).get_title()

    def run_app(self, show=True):
        u"""Show window and run the main app message loop until window been closed."""
        if show:
            self.expand()
        ret = super(Window, self).run_app()
        return ret

    def quit_app(self, code=0):
        u"""Post quit message."""
        return super(Window, self).quit_app(code)

    # overrideable
    def _document_ready(self, target):
        # Set window title based on <title> content, if any
        if self._title_changed:
            return
        root = sciter.Element(target)
        title = root.find_first(u'html > head > title')
        if title:
            self.set_title(title.get_text())
        pass

    pass
