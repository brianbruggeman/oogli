import oogli
from DebugWindow import DebugWindow as Window

vshader = '''
    #version 410
    in vec3 vertices;
    in vec3 colors;
    out vec3 vcolors;
    void main () {
        gl_Position = vec4(vertices.xyz, 1.0);
        vcolors = colors;
    }
'''

fshader = '''
    #version 410
    uniform vec3 colored = vec3(0.2, 1.0, 0.2);
    in vec3 vcolors;
    out vec4 frag_color;
    void main () {
        frag_color = vec4(vcolors.xyz, 1.0);
        // frag_color = vec4(0.2, 1.0, 0.2, 1.0);
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

colors = [
    (1.0, 0.0, 0.0),
    (1.0, 1.0, 0.0),
    (1.0, 0.0, 1.0),
]

width, height = (100, 100)

with Window('Oogli', width=width, height=height) as win:
    # Main Loop
    program.load(vertices=triangle, colors=colors)
    while win.open is True:
        # Render triangle
        program.draw(mode=win.mode, fill=win.fill)
        win.cycle()
