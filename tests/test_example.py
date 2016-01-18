#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest


def test_example():
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
        out vec4 frag_color;
        void main () {
            frag_colour = vec4(0.3, 1.0, 0.3, 1.0);
        }
    '''

    # Create a program from the shaders
    #  Note: This will auto request an OpenGL context of 4.1
    program = oogli.Program(v_shader, f_shader)
    version = major, minor = program.version
    print('Opengl: {}'.format(version))

    # Vertices for a 2D Triangle
    triangle = [(0.0, 0.5), (-0.5, 0.5), (-0.5, -0.5)]

    with oogli.Window(title='Oogli',
                      width=640, height=480,
                      major=major, minor=minor,
                      focus=False, visible=False) as win:
        # Main Loop
        # Setup window in a 'debug' mode
        count = 0
        while win.open is True or count <= 10:
            # Render triangle
            program.draw(vertices=triangle)
            count += 1


if __name__ == '__main__':
    pytest.main()
