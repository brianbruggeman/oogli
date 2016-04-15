#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import logging
import threading

import glfw
import glfw.gl as gl


log = logging.getLogger('Window')


class Window(object):
    '''Wraps GLFW functions into a convenient package

    >>> win = Window(title='Example', width=1080, height=720)
    >>> win.loop()
    '''
    registry = {}

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwds):
        glfw.core.set_window_should_close(self.win, True)

    def clear(self):
        '''Clears the window'''
        black_background_color = [0.0, 0.0, 0.0, 1.0]
        gl.clear_color(*black_background_color)
        gl.clear(gl.COLOR_BUFFER_BIT)
        if self.open:
            self.cycle()

    @property
    def width(self):
        '''Window width'''
        width, height = glfw.get_window_size(self.win)
        return width

    @property
    def height(self):
        '''Window height'''
        width, height = glfw.get_window_size(self.win)
        return height

    @property
    def fb_width(self):
        '''Framebuffer width'''
        fb_width, fb_height = glfw.get_framebuffer_size(self.win)
        return fb_width

    @property
    def fb_height(self):
        '''Framebuffer height'''
        fb_width, fb_height = glfw.get_framebuffer_size(self.win)
        return fb_height

    def __init__(self, title='GLFW Example', height=480, width=640, major=None, minor=None, visible=True, focus=True, background=None):
        # Determine available major/minor compatibility
        #  This contains init and terminate logic for glfw, so it must be run first
        major, minor = self.get_opengl_version(major, minor)
        self.title = title

        # Lock is for thread aware Windows and opening, closing and garbage
        #  collection
        self.lock = threading.Lock()

        if not glfw.core.init():
            raise RuntimeError('Could not initialize glfw')

        # Hinting must be run before window creation
        glfw.core.window_hint(glfw.CONTEXT_VERSION_MAJOR, major)
        glfw.core.window_hint(glfw.CONTEXT_VERSION_MINOR, minor)
        glfw.core.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.core.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.TRUE)
        glfw.core.window_hint(glfw.VISIBLE, visible)
        glfw.core.window_hint(glfw.FOCUSED, focus)

        # Unnecessary
        glfw.core.window_hint(glfw.SAMPLES, 1)
        glfw.core.window_hint(glfw.RED_BITS, 8)
        glfw.core.window_hint(glfw.GREEN_BITS, 8)
        glfw.core.window_hint(glfw.BLUE_BITS, 8)
        glfw.core.window_hint(glfw.ALPHA_BITS, 8)
        glfw.core.window_hint(glfw.DEPTH_BITS, 8)

        # Generate window
        self.win = glfw.create_window(height=height, width=width, title=title)
        Window.registry[self.win] = self

        # Setup window callbacks: Must be run after creating an OpenGL window
        self.setup_callbacks()

        # Set context
        glfw.core.make_context_current(self.win)
        self.init()
        if background is not None:
            bg = [0.0, 0.0, 0.0, 1.0]
            background = list(background) + bg[len(background):]
            gl.clear_color(*background)

    def __del__(self):
        '''Removes the glfw window'''
        if hasattr(self, 'win'):
            glfw.core.set_window_should_close(self.win, gl.TRUE)
            # Wait for loop to end
            self.lock.acquire()
            glfw.core.destroy_window(self.win)
            self.lock.release()

    def get_opengl_version(self, major=None, minor=None):
        '''Contains logic to determine opengl version.

        Only run this within initialization before running standard window code
        '''
        # Determine available major/minor compatibility
        #  This contains init and terminate logic for glfw, so it must be run first
        ffi = glfw._ffi
        opengl_version = (gl.get_integerv(gl.MAJOR_VERSION), gl.get_integerv(gl.MINOR_VERSION))
        versions = [
            (4, 5), (4, 4), (4, 3), (4, 2), (4, 1), (4, 0),
            (3, 3), (3, 2), (3, 1), (3, 0),
            (2, 1), (2, 0),
            (1, 5), (1, 4), (1, 3), (1, 2), (1, 1), (1, 0),
        ]
        if major and minor:
            ver = (major, minor)
            vindex = versions.index((major, minor))
            versions.pop(vindex)
            versions.insert(0, (major, minor))
        farg = ffi.new('char []', bytes(''.encode('utf-8')))
        title = farg

        if not glfw.core.init():
            glfw.terminate()
            raise RuntimeError('Could not initialize GLFW')

        for major, minor in versions:
            try:
                glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, major)
                glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, minor)
                glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
                if major >= 3 and minor in [0, 1]:
                    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
                glfw.window_hint(glfw.VISIBLE, False)
                glfw.window_hint(glfw.FOCUSED, False)
                window = glfw.core.create_window(1, 1, title, ffi.NULL, ffi.NULL)
                if window != ffi.NULL:
                    glfw.destroy_window(window)
                    if opengl_version is None or opengl_version == (0, 0):
                        opengl_version = (major, minor)
            except Exception as e:
                import traceback as tb
                for line in tb.format_exc(e).split('\n'):
                    log.error(line)

        glfw.terminate()
        if opengl_version is None or not opengl_version > (0, 0):
            raise RuntimeError('Could not set opengl context to version: {}.{}'.format(major, minor))
        return opengl_version

    def init(self):
        '''Scene initialization'''
        gl.clear(gl.COLOR_BUFFER_BIT)

    @property
    def visible(self):
        return glfw.get_window_attrib(self.win, glfw.VISIBLE)

    @visible.setter
    def visible(self, value):
        if value in [True, gl.TRUE, ]:
            glfw.show_window(self.win)
        elif value in [False, gl.FALSE]:
            glfw.hide_window(self.win)
        return self._visible

    @property
    def focus(self):
        return glfw.get_window_attrib(self.win, glfw.FOCUSED)

    @focus.setter
    def focus(self, value):
        if value in [True, False, gl.TRUE, gl.FALSE]:
            self._focus = value
            glfw.window_hint(glfw.FOCUSED, self._focus)
        return self._focus

    def render(self):
        '''Empty scene'''
        self.clear()

    def loop(self):
        '''Simplified loop'''
        self.lock.acquire()
        while self.open:
            self.render()
            self.handle_buffers_and_events()
        self.lock.release()

    def cycle(self):
        glfw.core.swap_buffers(self.win)
        glfw.core.poll_events()

    def set_background(self, color):
        default_color = [0.0, 0.0, 0.0, 1.0]
        color = color + default_color[len(color):]
        gl.clear_color(color)
        gl.clear(gl.COLOR_BUFFER_BIT)

    def setup_callbacks(self):
        '''Creates glfw callbacks for this window'''
        glfw.core.set_char_callback(self.win, self.on_char)
        glfw.core.set_char_mods_callback(self.win, self.on_char_mods)
        glfw.core.set_cursor_enter_callback(self.win, self.on_cursor_focus)
        glfw.core.set_cursor_pos_callback(self.win, self.on_mouse_move)
        glfw.core.set_error_callback(self.on_error)
        glfw.core.set_key_callback(self.win, self.on_key)
        glfw.core.set_mouse_button_callback(self.win, self.on_mouse_button)
        glfw.core.set_scroll_callback(self.win, self.on_scroll)
        glfw.core.set_window_refresh_callback(self.win, self.on_window_refresh)
        glfw.core.set_window_size_callback(self.win, self.on_window_resize)
        glfw.core.set_window_pos_callback(self.win, self.on_window_move)
        glfw.core.set_window_close_callback(self.win, self.on_window_close)
        glfw.core.set_window_focus_callback(self.win, self.on_window_focus)
        glfw.core.set_window_iconify_callback(self.win, self.on_window_minimize)
        glfw.core.set_drop_callback(self.win, self.on_file_drag_and_drop)
        glfw.core.set_framebuffer_size_callback(self.win, self.on_framebuffer_resize)
        glfw.core.set_monitor_callback(self.on_monitor)

    @property
    def open(self):
        return not glfw.core.window_should_close(self.win)

    @open.setter
    def open(self, value):
        if value in [True, gl.TRUE]:
            glfw.core.set_window_should_close(value)

    @staticmethod
    @glfw.decorators.char_callback
    def on_char(win, codepoint):
        '''Handles unicode char callback

        This is useful for handling simple character strokes and text input
        '''

    @staticmethod
    @glfw.decorators.char_mods_callback
    def on_char_mods(win, codepoint, mods):
        '''Handles unicode char callback /w mods

        This is useful for handling simple character strokes and text input
        with modifiers
        '''

    @staticmethod
    @glfw.decorators.cursor_enter_callback
    def on_cursor_focus(win, state):
        '''Cursor position upon entering client area'''

    @staticmethod
    @glfw.decorators.drop_callback
    def on_file_drag_and_drop(win, count, paths):
        '''Handles drag and drop of file paths'''

    @staticmethod
    @glfw.decorators.error_callback
    def on_error(code, message):
        '''Handles an error callback event'''
        error_message = glfw.ffi_string(message)
        message = '{}: {}'.format(code, error_message)
        log.error(message)

    @staticmethod
    @glfw.decorators.framebuffer_size_callback
    def on_framebuffer_resize(win, width, height):
        '''Handles a framebuffer resize event'''

    @staticmethod
    @glfw.decorators.key_callback
    def on_key(win, key, code, action, mods):
        '''Handles a key event'''
        if key in [glfw.KEY_ESCAPE] and action in [glfw.PRESS]:
            glfw.set_window_should_close(win, gl.TRUE)

    @staticmethod
    @glfw.decorators.monitor_callback
    def on_monitor(monitor, event=None):
        '''Handles monitor connect and disconnect'''

    @staticmethod
    @glfw.decorators.mouse_button_callback
    def on_mouse_button(win, button, action, mods):
        '''Handles a mouse button event'''

    @staticmethod
    @glfw.decorators.cursor_pos_callback
    def on_mouse_move(win, x, y):
        '''Mouse movement handler'''

    @staticmethod
    @glfw.decorators.scroll_callback
    def on_scroll(win, x, y):
        '''Scrollback handler'''

    @staticmethod
    @glfw.decorators.window_close_callback
    def on_window_close(win):
        '''Handles a window close event'''

    @staticmethod
    @glfw.decorators.window_focus_callback
    def on_window_focus(win, state):
        ''''''

    @staticmethod
    @glfw.decorators.window_iconify_callback
    def on_window_minimize(win, state):
        '''Handles window minimization/restore events'''

    @staticmethod
    @glfw.decorators.window_pos_callback
    def on_window_move(win, x, y):
        '''Handles window move event'''

    @staticmethod
    @glfw.decorators.window_refresh_callback
    def on_window_refresh(win):
        '''Window refresh handler

        Called periodically or during window resize events'''

    @staticmethod
    @glfw.decorators.window_size_callback
    def on_window_resize(win, width, height):
        '''Window resize handler'''
