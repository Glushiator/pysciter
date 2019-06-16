u"""Download http content (Go sciter example port)."""

from __future__ import absolute_import
import sciter


class ContentEventHandler(sciter.EventHandler):
    u"""<div#content> event handler."""

    def document_complete(self):
        print u"content loaded."
        pass

    def on_data_arrived(self, nm):
        print u"data arrived, uri:", nm.uri, nm.dataSize, u"bytes"
        pass

    pass


class Frame(sciter.Window):
    def __init__(self):
        super(Frame, self).__init__(ismain=True, uni_theme=False, debug=True)
        pass

    def on_data_load(self, nm):
        # called on every html/img/css/etc resource download request
        pass

    def on_data_loaded(self, nm):
        # called on every downloaded resource
        print u"data loaded, uri:", nm.uri, nm.dataSize, u"bytes"
        pass

    def load(self, url):
        self.set_title(u"Download Element Content")
        self.load_html(
            '''<html><body>
            <p>Url to load: <span id='url'>placed here</span></p>
            <div id='content' style='size: *'></div></body></html>''',
            u"/")

        # get root element
        root = self.get_root()

        # get span#url and frame#content:
        span = root.find_first(u'#url')
        content = root.find_first(u'#content')

        # replace span text with url provided
        text = span.get_text()
        span.set_text(url)
        print u"span:", text

        # install event handler to content frame to print data_arrived events
        self.handler = ContentEventHandler(element=content)

        # make http request to download url and place result as inner of #content
        print u"load content"
        content.request_html(url)
        pass

    pass


if __name__ == u'__main__':
    import sys

    print u"Sciter version:", sciter.version(as_str=True)

    url = u"http://httpbin.org/html" if len(sys.argv) < 2 else sys.argv[1]
    print url

    frame = Frame()
    frame.load(url)
    frame.expand()
    frame.run_app(False)
