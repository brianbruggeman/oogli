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

# Vertices for a 2D Triangle
triangle = [(0.0, 0.5), (-0.5, 0.5), (-0.5, -0.5)]

with oogli.Window('Oogli', 100, 100) as win:
    # Main Loop
    program.load(vertices=triangle)
    while win.is_open:
        # Render triangle
        program.draw()
        win.cycle()
