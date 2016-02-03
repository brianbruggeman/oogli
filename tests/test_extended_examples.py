#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest


def test_basic_load_example(options):
    '''Tests basic load api'''
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

    program = oogli.Program(v_shader, f_shader)

    # Vertices for a 2D Triangle
    vertices = options['triangle']

    # Setup window and screenshot pixels
    width, height = options['width'], options['height']
    with oogli.Window(title='Oogli|Test|Basic Load Example',
                      width=width, height=height,
                      major=major, minor=minor,
                      focus=False, visible=False) as win:
        # Main Loop
        # Loop through only once
        count = 0
        count_stop = 1
        running = True
        start_time = time.time()
        program.load(vertices=vertices)
        while running:
            # Render triangle
            program.draw()
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
    checksum = options['checksum']  # simple green triangle
    print('Draw loop ran in {:>0.2f} sec. {:>.0f} fps'.format(delta, count / delta))
    assert pixel_sum == checksum


def test_color_example(options):
    '''Tests basic draw api and uses colors'''
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
    vertices = options['triangle']

    # Setup window and screenshot pixels
    colors = options['colors']

    # Setup window and screenshot pixels
    width, height = options['width'], options['height']
    with oogli.Window(title='Oogli|Test|Color Example',
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
            program.draw(vertices=vertices, colors=colors)
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
    checksum = options['checksum']  # simple green triangle
    print('Draw loop ran in {:>0.2f} sec. {:>.0f} fps'.format(delta, count / delta))
    assert pixel_sum == checksum


def test_color_load_example(options):
    '''Tests basic draw api and uses colors'''
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
    vertices = options['triangle']

    # Setup window and screenshot pixels
    colors = options['colors']

    # Setup window and screenshot pixels
    width, height = options['width'], options['height']
    with oogli.Window(title='Oogli|Test|Color Load Example',
                      width=width, height=height,
                      major=major, minor=minor,
                      focus=False, visible=False) as win:
        # Main Loop
        # Loop through only once
        count = 0
        count_stop = 1
        running = True
        start_time = time.time()
        program.load(vertices=vertices, colors=colors)
        while running:
            # Render triangle
            program.draw()
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
    checksum = options['checksum']  # simple green triangle
    print('Draw loop ran in {:>0.2f} sec. {:>.0f} fps'.format(delta, count / delta))
    assert pixel_sum == checksum


def test_uniform_example(options):
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
        uniform vec3 color = vec3(1.0, 0.2, 0.2);
        out vec4 frag_color;
        void main () {
            frag_color = vec4(color, 1.0);
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
    vertices = options['triangle']
    color = options['color']

    # Setup window and screenshot pixels
    width, height = options['width'], options['height']
    with oogli.Window(title='Oogli|Test|Uniform Example',
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
            # Render vertices
            program.draw(vertices=vertices, color=color)
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
    checksum = options['checksum']  # simple green triangle
    print('Draw loop ran in {:>0.2f} sec. {:>.0f} fps'.format(delta, count / delta))
    assert pixel_sum == checksum


def test_uniform_load_example(options):
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
        uniform vec3 color = vec3(1.0, 0.2, 0.2);
        out vec4 frag_color;
        void main () {
            frag_color = vec4(color, 1.0);
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
    vertices = options['triangle']
    color = options['color']

    # Setup window and screenshot pixels
    width, height = options['width'], options['height']
    with oogli.Window(title='Oogli|Test|Uniform Load Example',
                      width=width, height=height,
                      major=major, minor=minor,
                      focus=False, visible=False) as win:
        # Main Loop
        # Loop through only once
        count = 0
        count_stop = 1
        running = True
        start_time = time.time()
        program.load(vertices=vertices, color=color)
        while running:
            # Render vertices
            program.draw()
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
    checksum = options['checksum']  # simple green triangle
    print('Draw loop ran in {:>0.2f} sec. {:>.0f} fps'.format(delta, count / delta))
    assert pixel_sum == checksum


if __name__ == '__main__':
    pytest.main()
