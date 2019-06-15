u"""Minimalistic PySciter sample for Windows."""

from __future__ import absolute_import

import faulthandler; faulthandler.enable()

import sciter

if __name__ == u'__main__':
    sciter.runtime_features(allow_sysinfo=True)

    frame = sciter.Window(ismain=True, uni_theme=True)
    frame.load_file(u"examples/minimal.htm")
    frame.run_app()
