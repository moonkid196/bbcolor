#!/usr/bin/env python
#
# Bryan Burke
# bburke@baburke.net
#
# Simple module to speed up/facilitate color printing
#

import sys

'''Module for handling simple terminal coloring'''

class BadColor(Exception):
    pass

class bbcolor:
    '''Class to handle a single color-scheme/output

    All set_* methods support resetting to defaults by calling the method with
    no arguments

    Example use:
    >>> from bbcolor import bbcolor
    >>> bbc = bbcolor()
    >>> bbc.set_fg(160)
    >>> bbc.pr('Hello, World!')'''

    _color = False
    _fg    = None
    _bg    = None
    _style = None
    _file  = sys.stdout

    def __init__(self, quiet=True):
        if not quiet:
            sys.stdout.write('+ Initializing bbcolor object\n')

        if sys.stdout.isatty():
            if not quiet:
                sys.stdout.write('\033[38;5;112m+ Detected terminal, using color\033[0m\n')
            self._color = True
        else:
            if not quiet:
                sys.stdout.write('+ No terminal detected, not using color\n')
            self._color = False

        self.set_fg()
        self.set_bg()
        self.set_style()
        self.set_file()

    def use_color(self, use):
        '''For the (dis)use of color

        use: True/False for whether to use color'''

        assert type(use) == bool

        self._color = use

    def set_fg(self, foreground=None):
        '''Set a default foreground color

        foreground: Numeric (0-255) color to use'''

        if foreground is None:
            self._fg = None
            return

        assert type(foreground) == int

        if foreground not in range(256):
            raise BadColor('%s is not in [0, 255]' % str(foreground))

        self._fg = foreground

    def set_bg(self, background=None):
        '''Set a default background color

        background: Numeric (0-255) color to use'''

        if background is None:
            self._bg = None
            return

        assert type(background) == int

        if background not in range(256):
            raise BadColor('%s is not in [0, 255]' % str(background))

        self._bg = background

    def set_style(self, style=None):
        '''Set a default style

        style: A comma-separated list of styles: normal, bold, underline,
        reverse, reset. Note that if 'reset' is used, all other styles are
        discarded'''

        if style is None:
            self._style = None
        else:
            self._style = str(style)

        self._style_string = self._parse_style(self._style)

    def _parse_style(self, style):
        '''Parse a style string'''

        if style is None:
            return '22'

        lstyle = []
        for s in style.split(','):
            if s == 'reset':
                lstyle = ['0']
                break
            elif s == 'normal':
                lstyle.append('22')
            elif s == 'bold':
                lstyle.append('1')
            elif s == 'underline':
                lstyle.append('4')
            elif s == 'reverse':
                lstyle.append('7')

        return ';'.join(lstyle)

    def set_file(self, out_file=None):
        '''Default output stream to use

        'out_file' should be a file-like object or None to reset to default'''

        if out_file is None:
            self._file = self.__class__._file
        else:
            self._file = out_file

    def pr(self, msg, foreground=None, background=None, style=None,
            out_file=None):
        '''Function to print a message with the given attributes'''

        # Set defaults, if any
        if out_file is None:
            _file = self._file

        out_str = self.format(msg, foreground=foreground, background=background,
                style=style)

        _file.write(out_str + '\n')

    def format(self, msg, foreground=None, background=None, style=None):
        '''Function to format a message with the given attributes'''

        if not self._color:
            return msg

        # Set defaults, if any
        if foreground is None:
            foreground = self._fg

        if background is None:
            background = self._bg

        if style is None:
            style = self._style_string
        else:
            style = self._parse_style(style)

        # Parse the actual values
        if foreground is None:
            foreground = '39'
        else:
            foreground = '38;5;%d' % foreground

        if background is None:
            background = '49'
        else:
            background = '48;5;%d' % background

        return '\033[%s;%s;%sm%s\033[0m' % (foreground, background, style, msg)
