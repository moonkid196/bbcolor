#!/usr/bin/env python3
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
            print('+ Initializing bbcolor object')

        if sys.stdout.isatty():
            if not quiet:
                print('\033[38;5;112m+ Detected terminal, using color\033[0m')
            self._color = True
        else:
            if not quiet:
                print('+ No terminal detected, not using color')
            self._color = False

        self.set_fg()
        self.set_bg()
        self.set_style()
        self.set_file()

    def use_color(self, use):
        '''For the (dis)use of color

        use: True/False for whether to use color'''

        # Just making sure it get sets to a boolean
        if use:
            self._color = True
        else:
            self._color = False

    def set_fg(self, fg=None):
        '''Set a default foreground color
        
        fg: Numeric (0-255) color to use'''

        if fg is None:
            self._fg = None
            return

        if not self._color:
            return

        if fg not in range(256):
            raise BadColor('%s is not in [0, 255]' % str(fg))

        self._fg = fg

    def set_bg(self, bg=None):
        '''Set a default background color
        
        bg: Numeric (0-255) color to use'''

        if bg is None:
            self._bg = None
            return

        if not self._color:
            return

        if bg not in range(256):
            raise BadColor('%s is not in [0, 255]' % str(bg))

        self._bg = bg

    def set_style(self, style=None):
        '''Set a default style

        style: A comma-separated list of styles: normal, bold, underline,
        reverse, reset. Note that if 'reset' is used, all other styles are
        discarded'''

        if style is None:
            self._style = style
        else:
            self._style = str(style)

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

    def set_file(self, file=None):
        '''Default output stream to use
        
        'file' should be a file-like object or None to reset to default'''

        if file is None:
            self._file = self.__class__._file
        else:
            self._file = file

    def pr(self, msg, fg=None, bg=None, style=None, file=None):
        '''Function to print a message with the given attributes'''

        # Set defaults, if any
        if file is None:
            file = self._file

        s = self.format(msg, fg=fg, bg=bg, style=style)

        print(s, file=file)

    def format(self, msg, fg=None, bg=None, style=None):
        '''Function to format a message with the given attributes'''

        # Set defaults, if any
        if fg is None:
            fg = self._fg

        if bg is None:
            bg = self._bg

        if style is None:
            style = self._style

        # Parse the actual values
        if fg is None:
            fg = '39'
        else:
            fg = '38;5;%d' % fg

        if bg is None:
            bg = '49'
        else:
            bg = '48;5;%d' % bg

        style = self._parse_style(style)

        if self._color:
            return '\033[%s;%s;%sm%s\033[0m' % (fg, bg, style, msg)
        else:
            return '\033[%sm%s\033[0m' % (style, msg)
