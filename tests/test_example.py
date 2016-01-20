#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest


def test_example():
    import oogli
    import numpy as np
    num_of_bytes = 3

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
            frag_color = vec4(0.3, 1.0, 0.3, 1.0);
        }
    '''

    if not oogli.opengl_supported(4, 1):
        pytest.skip("Unsupported configuration")

    # Create a program from the shaders
    #  Note: This will auto request an OpenGL context of 4.1
    program = oogli.Program(v_shader, f_shader)
    version = major, minor = program.version
    print('Opengl: {}'.format(version))

    # Vertices for a 2D Triangle
    triangle = [(0.0, 0.5), (-0.5, 0.5), (-0.5, -0.5)]
    width, height = 640, 480
    num_of_bytes = 3

    pixels = np.zeros((width, height, num_of_bytes), dtype=np.uint8)
    with oogli.Window(title='Oogli',
                      width=width, height=height,
                      major=major, minor=minor,
                      focus=False, visible=False) as win:
        # Main Loop
        # Loop through only once
        count = 0
        count_stop = 1
        running = True
        while running:
            # Render triangle
            program.draw(vertices=triangle)
            count += 1
            if win.open is False:
                running = False
            elif count > count_stop:
                running = False
            pixels = oogli.screenshot(pixels)

    # Checksum image
    pixel_sum = np.sum(pixels)
    checksum = 35587  # simple green triangle
    assert pixel_sum == checksum


if __name__ == '__main__':
    pytest.main()
