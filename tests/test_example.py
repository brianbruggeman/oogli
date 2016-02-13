#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest


def test_basic_example(options):
    '''Tests basic draw api'''
    import time
    import numpy as np
    import oogli

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

    major, minor = (4, 1)
    if not oogli.opengl_supported(major, minor):
        error_message = "OpenGL {major}.{minor} is not supported."
        pytest.skip(error_message.format(major=major, minor=minor))

    # Create a program from the shaders
    #  Note: This will auto request an OpenGL context of 4.1
    program = oogli.Program(v_shader, f_shader)
    major, minor = program.version
    if not oogli.opengl_supported(major, minor):
        error_message = "OpenGL {major}.{minor} is not supported."
        pytest.skip(error_message.format(major=major, minor=minor))

    # Vertices for a 2D Triangle
    vertices = options['triangle']

    # Setup window and screenshot pixels
    width, height = options['width'], options['height']
    with oogli.Window(title='Oogli|Test|Basic Example',
                      width=width, height=height,
                      major=major, minor=minor,
                      focus=False, visible=False) as win:
        # Main Loop
        # Loop through only once
        count = 0
        count_stop = 100
        running = True
        data = program.load(vertices=vertices)
        start_time = time.time()
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
    fps = count / delta
    assert fps > 50, 'Draw loop ran in {:>0.2f} sec. {:>.0f} fps'.format(delta, fps)
    checksum = options['checksum']  # simple green triangle
    print('Draw loop ran in {:>0.2f} sec. {:>.0f} fps'.format(delta, count / delta))
    # assert pixel_sum != checksum
    options['checksum'] == pixel_sum


if __name__ == '__main__':
    pytest.main()
