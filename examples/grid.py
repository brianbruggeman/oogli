#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

import oogli
from oogli import gl
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
    uniform vec3 color = vec3(0.2, 1.0, 0.2);
    out vec4 frag_color;
    void main () {
        frag_color = vec4(color, 1.0);
    }
'''

# Create a program from the shaders
#  Note: This will auto request an OpenGL context of 4.1 for future windows
program = oogli.Program(vshader, fshader)
major, minor = program.version

# Vertices for a 2D Triaffngle
triangle = [
    (0.0, 0.5),
    (0.5, -0.5),
    (-0.5, -0.5)
]

triangle_indices = [0, 1, 2]

# Grid
size = 2
increment = 1 / size
grid = [
    (x/size, y/size)
    for x in range(-size, size + 1)
    for y in range(-size, size + 1)
]

# Grid indices
grid_indices = []
for index, (x, y) in enumerate(grid):
    right = x + increment, y
    up = x, y + increment
    neighbors = [up, right]
    for neighbor in neighbors:
        try:
            neighbor_index = grid.index(neighbor)
            point = (index, neighbor_index)
            grid_indices.append(point)
        except ValueError:
            pass

grey = (0.4, 0.4, 0.4)
yellow = (1.0, 1.0, 1.0)
green = (0.2, 1.0, 0.2)
# width, height = (1366, 768)
width, height = (640, 480)

axis = [(-1, 0), (1, 0), (0, -1), (0, 1)]
axis_indices = [(0, 1), (2, 3)]


with Window(title='Oogli', width=width, height=height, major=major, minor=minor) as win:
    # Main Loop
    triangle_data, triangle_indices = program.setup(vertices=triangle, indices=triangle_indices)
    grid_data, grid_indices = program.setup(vertices=grid, indices=grid_indices)
    axis_data, axis_indices = program.setup(vertices=axis, indices=axis_indices)
    while win.open is True:
        # Render triangle
        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT)
        program.draw(mode=win.mode, fill=win.fill, data=triangle_data, indices=triangle_indices, color=green)
        program.draw(mode=gl.LINES, fill=gl.LINE, data=axis_data, indices=axis_indices, color=yellow)
        program.draw(mode=gl.LINES, fill=gl.LINE, data=grid_data, indices=grid_indices, color=grey)
        # pixels = oogli.screenshot(win)
        win.cycle()

# print('Checksum: {}'.format(np.sum(pixels)))
