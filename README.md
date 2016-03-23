# bbcolor

Simple module to provide color output in a terminal for python scripts. All
other tools seemed to roll their own, so I thought I'd make it a little more
formal.

## Synopsys

  >>> import bbcolor
  >>> bbc = bbcolor.bbcolor()
  >>> bbc.set_fd(160)
  >>> bbc.set_bg(50)
  >>> bbc.set_style('bold')
  >>> bbc.pr('Hello, World!')

For more detailed information, see the docstrings/inline-python help

## Features/Notes

- **IMPORTANT** -- This module *assumes* 256-color-capable terminal, if
  connected to one at all. It does no **TERM**/termcap checking to ensure the
  terminal supports this.
- Simple, quick color output control via a minimal API
- Caching of the more complex parsing/ANSI-escapes
- Easy enable/disable via the *use_color()* method
- Checks if *stdout* is a tty for whether to use color
