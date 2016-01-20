#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import logging

import glfw
import glfw.gl as gl

from oogli import Window


log = logging.getLogger('Window')


class DebugWindow(Window):
    '''Enables a number of nice things not within the default window'''

    @staticmethod
    @glfw.decorators.key_callback
    def on_key(win, key, code, action, mods):
        '''Handles a key event'''
        if key in [glfw.KEY_ESCAPE, glfw.KEY_Q] and action in [glfw.PRESS]:
            glfw.set_window_should_close(win, gl.TRUE)
