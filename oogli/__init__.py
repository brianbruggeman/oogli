#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Oogli
-----

Oogli is Beautiful

A beautiful Object Oriented Graphics Library Interface

Created by Brian Bruggeman
Copyright (c) 2016

Usage:

    >>> import oogli
    >>> win = oogli.Window('Sample')
    >>> vshader = open('shader.vert', 'r').read()
    >>> fshader = open('shader.frag', 'r').read()
    >>> program = oogli.create_program(vshader, fshader)
    >>> triangle = [(0.0, 0.5), (-0.5, 0.5), (-0.5, -0.5)]
    >>> with oogli.create_window() as win:
    ...     while win.is_open():  # ctrl+c to break
    ...         program.draw(position=triangle)  # renders triangle
    ...         oogli.cycle()  # handles events and swapping
    ...


License:  This file is released as Apache 2.0 license.  However, at
your option, you may apply any free software license you choose
provided that you adhere to the free software license chosen and
additionally follow these three criteria:
 a. list the author's name of this software as a contributor to your
    final product
 b. provide credit to your end user of your product or software without
    your end user asking for where you obtained your software
 c. notify the author of this software that you are using this software
 d. in addition, if you believe there can be some benefit in providing
    your changes upstream, you'll submit a change request.  While this
    criteria is completely optional, please consider not being a dick.
'''
import atexit

import glfw
from glfw import gl
import numpy as np

from .Program import Program
from .Window import Window

###############################################################################
__title__ = 'oogli'
__version__ = '0.2.0-dev'
__author__ = 'Brian Bruggeman'
__email__ = 'brian.m.bruggeman@gmail.com'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Brian Bruggeman'
__url__ = 'https://github.com/brianbruggeman/oogli.git'
__shortdesc__ = 'Oogli is a beautiful object oriented graphics library interface'


###############################################################################
def create_program(v_shader, f_shader):
    assert glfw.core.init() != 0
    program = Program(v_shader, f_shader)
    program.build()
    return program


def create_window(title='Oogli', width=800, height=600, *args, **kwds):
    assert glfw.core.init() != 0
    win = Window(title=title, width=width, height=height, *args, **kwds)
    return win


def cycle():
    assert glfw.core.init() != 0
    glfw.core.swap_buffers()
    glfw.core.poll_events()

from .utils import screenshot, opengl_supported, uniform_mapping

###############################################################################
atexit.register(glfw.core.terminate)
