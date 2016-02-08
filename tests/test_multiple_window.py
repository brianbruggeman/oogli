#!/usr/bin/env python
import pytest


def test_multiple_windows(options):
    import oogli
    from DebugWindow import DebugWindow as Window
    import numpy as np
    import time

    v_shader = '''
        #version 410
        in vec2 vertices;
        void main () {
            gl_Position = vec4(vertices, 0.0, 1.0);
        }
    '''

    f_shader = '''
        #version 410
        uniform vec3 color = vec3(1.0, 0.2, 0.2);
        out vec4 frag_color;
        void main () {
            frag_color = vec4(color, 1.0);
        }
    '''
    # Create a program from the shaders
    #  Note: This will auto request an OpenGL context of 4.1
    program = oogli.Program(v_shader, f_shader)
    major, minor = program.version
    if not oogli.opengl_supported(major, minor):
        error_message = "OpenGL {major}.{minor} is not supported."
        pytest.skip(error_message.format(major=major, minor=minor))

    debug_window_options = dict(
        width=options['width'],
        height=options['height'],
        major=major,
        minor=minor,
        focus=True,
        visible=True
    )

    def color(step=1):
        '''Smooth color transition'''
        while True:
            start = 10
            end = 250
            data = [0, 0, 0]
            for x in range(3):
                for _ in range(start, end, step):
                    val = _ / end
                    data[x] = val
                    yield data
            for x in range(3):
                for _ in range(end, start, -step):
                    val = _ / end
                    data[x] = val
                    yield data

    win1 = Window(title='Oogli|Test|MultiWindow 1', **debug_window_options)
    win2 = Window(title='Oogli|Test|MultiWindow 2', **debug_window_options)
    program.load(vertices=options['triangle'], indices=options['indices'])
    color = color()

    while win1.open or win2.open:
        if win1.open:
            win1.focus = True
            program.draw(mode=win1.mode, fill=win1.fill, color=color.next())
            win1.cycle()
            win1.focus = False
        if win2.open:
            win2.focus = True
            program.draw(mode=win2.mode, fill=win2.fill, color=color.next())
            win2.cycle()
            win2.focus = False
