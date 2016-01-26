#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest


def test_basic_example():
    import oogli
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
        out vec4 frag_color;
        void main () {
            frag_color = vec4(0.2, 1.0, 0.2, 1.0);
        }
    '''

    major, minor = (4, 1)
    if not oogli.opengl_supported(major, minor):
        error_message = "OpenGL {major}.{minor} is not supported."
        pytest.skip(error_message.format(major=major, minor=minor))

    # Create a program from the shaders
    #  Note: This will auto request an OpenGL context of 4.1
    program = oogli.Program(v_shader, f_shader)

    # Vertices for a 2D Triangle
    triangle = [(0.0, 0.5), (-0.5, 0.5), (-0.5, -0.5)]
    # colors = [
    #     (0.2, 1.0, 0.2),
    #     (0.2, 1.0, 0.2),
    #     (0.2, 1.0, 0.2),
    # ]

    # Setup window and screenshot pixels
    width, height = 100, 100
    with oogli.Window(title='Oogli',
                      width=width, height=height,
                      major=major, minor=minor,
                      focus=False, visible=False) as win:
        # Main Loop
        # Loop through only once
        count = 0
        count_stop = 1
        running = True
        start_time = time.time()
        while running:
            # Render triangle
            # program.draw(vertices=triangle, colors=colors)
            program.draw(vertices=triangle)
            count += 1
            if win.open is False:
                running = False
            elif count > count_stop:
                running = False
            win.cycle()
            pixels = oogli.screenshot(win)
        delta = time.time() - start_time

    # Checksum image
    pixel_sum = np.sum(pixels)
    checksum = 35587  # simple green triangle
    print('Draw loop ran in {:>0.2f} sec. {:>.0f} fps'.format(delta, count / delta))
    assert pixel_sum == checksum


def test_color_example():
    import oogli
    import numpy as np
    import time

    v_shader = '''
        #version 410
        in vec2 vertices;
        in vec3 colors;
        out vec3 vcolors;
        void main () {
            gl_Position = vec4(vertices, 0.0, 1.0);
            vcolors = colors;
        }
    '''

    f_shader = '''
        #version 410
        in vec3 vcolors;
        out vec4 frag_color;
        void main () {
            frag_color = vec4(vcolors, 1.0);
        }
    '''

    major, minor = (4, 1)
    if not oogli.opengl_supported(major, minor):
        error_message = "OpenGL {major}.{minor} is not supported."
        pytest.skip(error_message.format(major=major, minor=minor))

    # Create a program from the shaders
    #  Note: This will auto request an OpenGL context of 4.1
    program = oogli.Program(v_shader, f_shader)

    # Vertices for a 2D Triangle
    triangle = [(0.0, 0.5), (-0.5, 0.5), (-0.5, -0.5)]
    colors = [
        (0.2, 1.0, 0.2),
        (0.2, 1.0, 0.2),
        (0.2, 1.0, 0.2),
    ]

    # Setup window and screenshot pixels
    width, height = 100, 100
    with oogli.Window(title='Oogli',
                      width=width, height=height,
                      major=major, minor=minor,
                      focus=False, visible=False) as win:
        # Main Loop
        # Loop through only once
        count = 0
        count_stop = 1
        running = True
        start_time = time.time()
        while running:
            # Render triangle
            program.draw(vertices=triangle, colors=colors)
            count += 1
            if win.open is False:
                running = False
            elif count > count_stop:
                running = False
            win.cycle()
            pixels = oogli.screenshot(win)
        delta = time.time() - start_time

    # Checksum image
    pixel_sum = np.sum(pixels)
    checksum = 35587  # simple green triangle
    print('Draw loop ran in {:>0.2f} sec. {:>.0f} fps'.format(delta, count / delta))
    assert pixel_sum == checksum


def test_uniform_example():
    import oogli
    import numpy as np
    import time

    v_shader = '''
        #version 410
        in vec2 vertices;

        void main () {
            vec4 pos = vec4(vertices.xy, 0.0, 1.0);
            gl_Position = pos;
        }
    '''

    f_shader = '''
        #version 410
        uniform vec3 color;
        out vec4 frag_color;
        void main () {
            frag_color = vec4(colors, 1.0);
        }
    '''

    major, minor = (4, 1)
    if not oogli.opengl_supported(major, minor):
        error_message = "OpenGL {major}.{minor} is not supported."
        pytest.skip(error_message.format(major=major, minor=minor))

    # Create a program from the shaders
    #  Note: This will auto request an OpenGL context of 4.1
    program = oogli.Program(v_shader, f_shader)

    # Vertices for a 2D Triangle
    triangle = [(0.0, 0.5), (-0.5, 0.5), (-0.5, -0.5)]
    color = (0.2, 1.0, 0.2)  # Green

    # Setup window and screenshot pixels
    width, height = 100, 100
    with oogli.Window(title='Oogli',
                      width=width, height=height,
                      major=major, minor=minor,
                      focus=False, visible=False) as win:
        # Main Loop
        # Loop through only once
        count = 0
        count_stop = 1
        running = True
        start_time = time.time()
        while running:
            # Render triangle
            program.draw(vertices=triangle, color=color)
            count += 1
            if win.open is False:
                running = False
            elif count > count_stop:
                running = False
            win.cycle()
            pixels = oogli.screenshot(win)
        delta = time.time() - start_time

    # Checksum image
    pixel_sum = np.sum(pixels)
    checksum = 35587  # simple green triangle
    print('Draw loop ran in {:>0.2f} sec. {:>.0f} fps'.format(delta, count / delta))
    assert pixel_sum == checksum


if __name__ == '__main__':
    pytest.main()
