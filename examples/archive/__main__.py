"""Minimalistic PySciter sample for Windows."""

import sciter

if __name__ == '__main__':
    frame = sciter.Window(ismain=True, uni_theme=True)
    frame.load_file("archive.zip#archived.htm", normalize=False)
    frame.expand()
    frame.run_app()
