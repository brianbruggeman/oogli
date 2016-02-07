from __future__ import division

import oogli
from oogli import np
from DebugWindow import DebugWindow as Window

vshader = '''
    #version 410
    in vec2 vertices;
    void main () {
        gl_Position = vec4(vertices, 0.0, 1.0);
    }
'''

fshader = '''
    #version 410
    uniform vec3 color = vec3(1.0, 0.0, 0.0);
    out vec4 frag_color;
    void main () {
        frag_color = vec4(color, 1.0);
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
green = (0.2, 1.0, 0.2)
blue = (0.2, 0.2, 1.0)
red = (1.0, 0.2, 0.2)


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


with Window('Oogli', width=width, height=height) as win:
    # Main Loop
    program.load(vertices=triangle, color=blue)
    colors = color()
    while win.open is True:
        # Render triangle
        program.draw(fill=win.fill, mode=win.mode, color=colors.next())
        pixels = oogli.screenshot(win)
        win.cycle()

print('Checksum: {}'.format(np.sum(pixels)))