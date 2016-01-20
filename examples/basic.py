import oogli
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
    out vec4 frag_color;
    void main () {
        frag_color = vec4(0.2, 1.0, 0.2, 1.0);
    }
'''

# Create a program from the shaders
#  Note: This will auto request an OpenGL context of 4.1
program = oogli.Program(vshader, fshader)

# Vertices for a 2D Triangle
triangle = [
    (0.0, 0.5),
    (-0.5, 0.5),
    (-0.5, -0.5)
]

width, height = (640, 480)

with Window('Oogli', width=width, height=height) as win:
    # Main Loop
    program.load(vertices=triangle)
    fill = oogli.gl.FILL
    while win.open is True:
        # Render triangle
        program.draw(fill=fill)
        win.cycle()
