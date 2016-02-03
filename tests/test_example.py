#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest


def test_basic_example(options):
    '''Tests basic draw api'''
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
    with oogli.Window(title='Oogli|Test|Basic Example',
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
            program.draw(vertices=vertices)
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
