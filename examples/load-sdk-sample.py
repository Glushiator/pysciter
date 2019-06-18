u"""Minimalistic PySciter sample for Windows."""

from __future__ import absolute_import
import sciter
import sys


def main():
    sciter.runtime_features(allow_sysinfo=True)
    frame = sciter.Window(ismain=True, uni_theme=True)
    frame.load_file(sys.argv[1].decode("utf-8"))
    frame.run_app()


if __name__ == u'__main__':
    main()
