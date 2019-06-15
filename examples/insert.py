u"""Simple DOM example (Go sciter example port)."""

from __future__ import absolute_import
import sciter, sys

if __name__ == u"__main__":
    frame = sciter.Window(ismain=True, uni_theme=False)
    frame.set_title(u"Inserting example")

    # load simple html
    frame.load_html("""<html>html</html>""")

    # create div and link as child of root node (<html>)
    div = sciter.Element.create(u"div", u"hello, world")

    root = frame.get_root()
    root.insert(div, 0)

    # show window and run app
    frame.run_app()
