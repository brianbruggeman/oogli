#!/usr/bin/env python
# -*- coding: utf-8 -*-
import oogli
from oogli import np
from DebugWindow import DebugWindow as Window

vshader = '''
    #version 150
    in vec2 vertices;
    void main () {
        gl_Position = vec4(vertices, 0.0, 1.0);
    }
'''

fshader = '''
    #version 150
    out vec4 frag_color;
    void main () {
        frag_color = vec4(0.2, 1.0, 0.2, 1.0);
    }
'''

# Create a program from the shaders
#  Note: This will auto request an OpenGL context of 4.1 for future windows
program = oogli.Program(vshader, fshader)

# Vertices for a 2D Triangle
triangle = [
    (0.0, 0.5),
    (0.5, -0.5),
    (-0.5, -0.5)
]

width, height = (100, 100)

with Window('Oogli', width=width, height=height) as win:
    # Main Loop
    program.load(vertices=triangle)
    t = oogli.Texture('brick.png')
    print(t)

    # while win.open is True:
    #     # Render triangle
    #     program.draw()
    #     pixels = oogli.screenshot(win)
    #     win.cycle()

# print('Checksum: {}'.format(np.sum(pixels)))
