#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import ctypes
from textwrap import dedent as dd

import numpy as np
import OpenGL
OpenGL.ERROR_CHECKING = True
import glfw
from glfw import gl


# ######################################################################
# Data
# ######################################################################
title = 'OpenGL 4.1 Rendering'
width, height = 100, 75
major, minor = (4, 1)
draw_array = False
use_data = True

modes = sorted([
    gl.POINTS,
    gl.LINES,
    gl.LINE_LOOP,
    gl.LINE_STRIP,
    gl.LINES_ADJACENCY,
    gl.LINE_STRIP_ADJACENCY,
    # gl.QUADS,
    gl.TRIANGLES,
    gl.TRIANGLE_STRIP,
    gl.TRIANGLE_FAN,
    gl.TRIANGLE_STRIP_ADJACENCY,
    gl.TRIANGLES_ADJACENCY,
    # gl.PATCHES,
])
mode_index = modes.index(gl.TRIANGLES)

fills = [
    gl.FILL,
    gl.POINT,
    gl.LINE
]
fill_index = fills.index(gl.LINE)

pt = 0.5

vertices = np.array([
    (x, y) for x in [-pt, 0, pt] for y in [-pt, 0, pt]
], dtype=np.float32)

indices = np.array([
    # index for index in range(vertices.shape[0])
    5, 6, 0,
    # 5, 2, 0,
    # 5, 8, 6,
], dtype=np.uint32)

# Generate some colors for the points
rgb = 3
colors = np.array([
    (1.0, 0.0, 0.0),
    (0.0, 1.0, 0.0),
    (0.0, 0.0, 1.0),

    (1.0, 0.0, 1.0),
    (0.0, 1.0, 1.0),
    (1.0, 1.0, 0.0),

    (0.5, 0.5, 0.5),
    (0.5, 0.5, 0.0),
    (0.0, 0.5, 0.5),
], dtype=np.float32)

data = np.zeros(
    len(vertices),
    dtype=[
        ('position', np.float32, vertices.shape[-1]),
        ('color', np.float32, colors.shape[-1]),
    ]
)

# Interleave vertex data for position and color
data['position'] = vertices
data['color'] = colors

vshader = '''
    #version 410

    in vec2 position;
    in vec3 color;
    out vec3 v_color;

    void main () {
        gl_Position = vec4(position, 0.0, 1.0);
        v_color = color;
    }
    '''

fshader = '''
    #version 410

    in vec3 v_color;
    out vec4 frag_colour;

    void main () {
        frag_colour = vec4(v_color, 1.0);
        frag_colour = vec4(0.2, 1.0, 0.2, 1.0);
    }
    '''


# ######################################################################
# Helper functions
def screenshot(pixels):
    assert isinstance(pixels, np.ndarray), 'data must be a numpy array'
    width, height = pixels.shape[0:2]
    return gl.read_pixels(0, 0, width, height, gl.RGB, gl.UNSIGNED_BYTE, pixels)


@glfw.decorators.key_callback
def on_key(win, key, code, action, mods):
    '''Handles keyboard event'''
    global mode_index
    global fill_index
    global draw_array
    global indices_buffer_id
    global vertices
    global colors
    global data
    global use_data
    if action in [glfw.PRESS, glfw.REPEAT]:
        if key in [glfw.KEY_ESCAPE, glfw.KEY_Q]:
            # Quit
            glfw.core.set_window_should_close(win, gl.TRUE)
        elif key == glfw.KEY_M:
            # Update draw mode (points, lines, triangles, quads, etc.)
            if mods & glfw.MOD_SHIFT:
                mode_index = mode_index - 1 if mode_index - 1 >= 0 else len(modes) - 1
            else:
                mode_index = mode_index + 1 if mode_index + 1 < len(modes) else 0
            print('New mode: {}'.format(modes[mode_index]))
        elif key == glfw.KEY_W:
            # Update fill mode (wireframe, solid, points)
            if mods & glfw.MOD_SHIFT:
                fill_index = fill_index - 1 if fill_index - 1 >= 0 else len(fills) - 1
            else:
                fill_index = fill_index + 1 if fill_index + 1 < len(fills) else 0
            print('New fill: {}'.format(fills[fill_index]))
        elif key == glfw.KEY_SPACE:
            if mods & glfw.MOD_SHIFT:
                colors = np.array([
                    (1.0, 0.0, 0.0),
                    (0.0, 1.0, 0.0),
                    (0.0, 0.0, 1.0),

                    (1.0, 0.0, 1.0),
                    (0.0, 1.0, 1.0),
                    (1.0, 1.0, 0.0),

                    (0.5, 0.5, 0.5),
                    (0.5, 0.5, 0.0),
                    (0.0, 0.5, 0.5),
                ], dtype=np.float32)
            else:
                # Randomize colors
                colors = np.random.rand(len(vertices), 3)
            data['color'] = colors


def compile_shader(shader_source, shader_type):
    '''Compiles and checks output'''
    shader_id = gl.glCreateShader(shader_type)
    gl.glShaderSource(shader_id, dd(shader_source))
    gl.glCompileShader(shader_id)
    shader_result = gl.glGetShaderiv(shader_id, gl.COMPILE_STATUS)
    shader_log = gl.glGetShaderiv(shader_id, gl.INFO_LOG_LENGTH)
    assert shader_result == gl.TRUE
    if shader_log > 0:
        error_message = gl.glGetShaderInfoLog(shader_id)
        print('ERROR: Vertex Shader Compilation | {}'.format(error_message))
    return shader_id


def compile_program(*shader_sources):
    '''Compiles shaders, links to a program and checks output'''
    assert len(shader_sources) >= 2
    shader_types = [
        gl.VERTEX_SHADER,
        gl.FRAGMENT_SHADER,
        gl.TESS_CONTROL_SHADER,
        gl.TESS_EVALUATION_SHADER,
        gl.GEOMETRY_SHADER,
    ]
    shaders = [
        compile_shader(shader_source, shader_type)
        for shader_source, shader_type in zip(shader_sources, shader_types)
    ]
    program = gl.glCreateProgram()
    for shader in shaders:
        gl.glAttachShader(program, shader)
    gl.glLinkProgram(program)
    assert gl.glGetProgramiv(program, gl.LINK_STATUS) == gl.TRUE
    assert gl.glGetProgramiv(program, gl.INFO_LOG_LENGTH) == 0, gl.glGetProgramInfoLog(program)

    # Cleanup shaders
    for shader in shaders:
        gl.glDetachShader(program, shader)
        gl.glDeleteShader(shader)
    return program


def setup_context(major, minor):
    glfw.core.init()
    glfw.core.window_hint(glfw.SAMPLES, 4)
    glfw.core.window_hint(glfw.CONTEXT_VERSION_MAJOR, major)
    glfw.core.window_hint(glfw.CONTEXT_VERSION_MINOR, minor)
    glfw.core.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.core.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
    glfw.core.window_hint(glfw.RED_BITS, 24)
    glfw.core.window_hint(glfw.GREEN_BITS, 24)
    glfw.core.window_hint(glfw.BLUE_BITS, 24)
    glfw.core.window_hint(glfw.ALPHA_BITS, 24)
    glfw.core.window_hint(glfw.DEPTH_BITS, 24)

# ######################################################################
# Setup OpenGL Context
setup_context(major, minor)
num_byte_size = 3
pixels = np.zeros((width, height, num_byte_size), dtype=np.uint8)
win = glfw.create_window(title=title, width=width, height=height)
glfw.core.set_key_callback(win, on_key)
glfw.core.make_context_current(win)

# Build pipeline
program = compile_program(vshader, fshader)

# Bind attributes
gl.glBindAttribLocation(program, 0, 'position')
gl.glBindAttribLocation(program, 1, 'color')


# ######################################################################
# Setup VBO and VAO
vao = gl.glGenVertexArrays(1)
buffer_id = gl.glGenBuffers(1)
indices_buffer_id = gl.glGenBuffers(1)
gl.glBindBuffer(gl.ARRAY_BUFFER, buffer_id)

gl.glBindBuffer(gl.ELEMENT_ARRAY_BUFFER, indices_buffer_id)
gl.glBufferData(gl.ELEMENT_ARRAY_BUFFER, indices.flatten(), gl.STATIC_DRAW)

# ######################################################################
# Render
while not glfw.window_should_close(win):
    gl.glClear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT)
    gl.glPolygonMode(gl.FRONT_AND_BACK, fills[fill_index])
    gl.glBufferData(gl.ARRAY_BUFFER, data.nbytes, data, gl.DYNAMIC_DRAW)
    gl.glEnable(gl.DEPTH_TEST)
    gl.glDepthFunc(gl.LESS)
    gl.glUseProgram(program)

    gl.glBindVertexArray(vao)
    stride = data.strides[0]

    offset = ctypes.c_void_p(0)
    pos = gl.glGetAttribLocation(program, 'position')
    gl.glEnableVertexAttribArray(pos)
    gl.glBindBuffer(gl.ELEMENT_ARRAY_BUFFER, indices_buffer_id)
    gl.glBindBuffer(gl.ARRAY_BUFFER, buffer_id)
    gl.glVertexAttribPointer(pos, data['position'].shape[-1], gl.FLOAT, False, stride, offset)

    offset = ctypes.c_void_p(data.dtype['position'].itemsize)
    col = gl.glGetAttribLocation(program, 'color')
    gl.glEnableVertexAttribArray(col)
    gl.glBindBuffer(gl.ELEMENT_ARRAY_BUFFER, indices_buffer_id)
    gl.glBindBuffer(gl.ARRAY_BUFFER, buffer_id)
    gl.glVertexAttribPointer(col, data['color'].shape[-1], gl.FLOAT, False, stride, offset)

    gl.glDrawElements(modes[mode_index], len(indices), gl.UNSIGNED_INT, None)
    gl.glDisableVertexAttribArray(vao)

    pixels = screenshot(pixels)
    # Standard Loop Event handling
    glfw.core.swap_buffers(win)
    glfw.core.poll_events()

checksum = np.sum(pixels)
assert checksum == 39499, checksum

# ######################################################################
# Cleanup
gl.glUseProgram(0)
glfw.core.terminate()
