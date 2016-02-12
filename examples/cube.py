#!/usr/bin/env python
# -*- coding: utf-8 -*-
import oogli
from oogli import np
from DebugWindow import DebugWindow as Window

vshader = '''
    #version 410
    uniform mat4 mvp = mat4(vec4(1.0, 0.0, 0.0, 0.0), vec4(0.0, 1.0, 0.0, 0.0), vec4(0.0, 0.0, 1.0, 0.0), vec4(0.0, 0.0, 0.0, 1.0));
    in vec3 vertices;
    in vec3 colors;
    out vec3 v_colors;
    void main () {
        gl_Position = mvp * vec4(vertices, 1.0);
        v_colors = colors;
    }
'''

fshader = '''
    #version 410
    in vec3 v_colors;
    out vec4 frag_color;
    void main () {
        frag_color = vec4(v_colors, 1.0);
    }
'''

# Create a program from the shaders
#  Note: This will auto request an OpenGL context of 4.1 for future windows
program = oogli.Program(vshader, fshader)

# Vertices for a 3D Cube
pt = 0.5
vertices = [
    (-pt, pt, pt),
    (pt, pt, pt),
    (pt, -pt, pt),
    (-pt, -pt, pt),
    (-pt, pt, -pt),
    (pt, pt, -pt),
    (pt, -pt, -pt),
    (-pt, -pt, -pt)
]

indices = [
    (0, 1, 2), (2, 3, 0),  # front
    (1, 5, 6), (6, 2, 1),  # top
    (7, 6, 5), (5, 4, 7),  # back
    (4, 0, 3), (3, 7, 4),  # bottom
    (4, 5, 1), (1, 0, 4),  # left
    (3, 2, 6), (6, 7, 3),  # right
]

colors = [
    (1.0, 0.2, 0.2),
    (1.0, 1.0, 0.2),
    (1.0, 0.2, 1.0),
    (0.2, 1.0, 0.2),
    (0.2, 1.0, 1.0),
    (0.2, 0.2, 1.0),
    (0.2, 0.2, 0.2),
    (1.0, 1.0, 1.0),
]

mvp = [
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1)
]

width, height = (100, 100)

with Window('Oogli', width=width, height=height) as win:
    # Main Loop
    program.load(vertices=vertices, indices=indices, colors=colors)
    while win.open is True:
        # Render triangle
        program.draw(fill=win.fill, mode=win.mode, mvp=mvp)
        pixels = oogli.screenshot(win)
        win.cycle()

print('Checksum: {}'.format(np.sum(pixels)))
