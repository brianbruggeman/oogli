#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import logging

import glfw
import glfw.gl as gl

from oogli import Window


log = logging.getLogger('Window')

modes = sorted([
    gl.POINTS,
    gl.LINES,
    gl.LINE_LOOP,
    gl.LINE_STRIP,
    gl.LINES_ADJACENCY,
    gl.LINE_STRIP_ADJACENCY,
    # gl.QUADS,
    gl.TRIANGLES,
    gl.TRIANGLE_STRIP,
    gl.TRIANGLE_FAN,
    gl.TRIANGLE_STRIP_ADJACENCY,
    gl.TRIANGLES_ADJACENCY,
    # gl.PATCHES,
])

fills = [
    gl.FILL,
    gl.POINT,
    gl.LINE
]


class DebugWindow(Window):
    '''Enables a number of nice things not within the default window'''

    mode_index = modes.index(gl.TRIANGLES)
    fill_index = fills.index(gl.LINE)

    @property
    def fill(self):
        fill = fills[self.fill_index]
        return fill

    @property
    def mode(self):
        mode = modes[self.mode_index]
        return mode

    @staticmethod
    @glfw.decorators.key_callback
    def on_key(win, key, code, action, mods):
        '''Handles a key event'''
        self = Window.registry.get(win)
        if key in [glfw.KEY_ESCAPE, glfw.KEY_Q] and action in [glfw.PRESS]:
            glfw.set_window_should_close(win, gl.TRUE)

        elif key in [glfw.KEY_M] and action in [glfw.PRESS]:
            if mods & glfw.MOD_SHIFT:
                self.mode_index = self.mode_index - 1 if self.mode_index - 1 > 0 else len(modes) - 1
            else:
                self.mode_index = self.mode_index + 1 if self.mode_index + 1 < len(modes) else 0

        elif key in [glfw.KEY_F] and action in [glfw.PRESS]:
            if mods & glfw.MOD_SHIFT:
                self.fill_index = self.fill_index - 1 if self.fill_index > 0 else len(fills) - 1
            else:
                self.fill_index = self.fill_index + 1 if (self.fill_index + 1) < len(fills) else 0