"""
Classes for interacting with Logisim's RAW format: http://www.cburch.com/logisim/docs/2.7/en/html/guide/mem/menu.html
"""

import io

from logzero import logger

class RawWriter(object):
    """A simple writer for Logisim's RAW v2.0 files."""
    def __init__(self, output: io.TextIOBase, width: int):
        self.output = output
        self.output.write('raw v2.0\n')
        self.width = width
        
    def format(self, value: int):
        return "{value:0{width}x}".format(value=value, width=self.width)

    def write(self, *values):
        formatted = [self.format(v) for v in values]
        self.output.write(' '.join(formatted) + '\n')
