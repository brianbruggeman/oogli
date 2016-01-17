#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ctypes

from glfw import gl
import numpy as np

from .shaders import (
    Shader,
    VertexShader,
    FragmentShader,
    GeometryShader,
    TessellationControlShader,
    TessellationEvaluationShader,
)


def array(val, vtype=np.float32):
    return np.array(val, dtype=vtype)


class Program(object):

    @property
    def version(self):
        version = None if self.vert is None else self.vert.version
        return version

    def __init__(self, vert=None, frag=None, geo=None, tc=None, te=None):
        self.vert = VertexShader(vert) if vert is not None else None
        self.frag = FragmentShader(frag) if frag is not None else None
        self.geo = GeometryShader(geo) if geo is not None else None
        self.tc = TessellationControlShader(tc) if tc is not None else None
        self.te = TessellationEvaluationShader(te) if te is not None else None
        self.loaded = False
        self.built = False

    @property
    def program(self):
        if not hasattr(self, '_program'):
            self._program = gl.create_program()
        return self._program

    def __getitem__(self, key):
        return self.vert[key]

    def __setitem__(self, key, val):
        self.vert[key] = val

    def attach(self, shader):
        error_message = 'Attach expects a Shader object, not {}'.format(type(shader))
        assert isinstance(shader, Shader), error_message
        if isinstance(shader, VertexShader):
            self.vert = shader
        elif isinstance(shader, FragmentShader):
            self.frag = shader
        elif isinstance(shader, GeometryShader):
            self.geo = shader
        elif isinstance(shader, TessellationControlShader):
            self.tc = shader
        elif isinstance(shader, TessellationEvaluationShader):
            self.te = shader
        shader.compile()
        shader.attach(self)

    def build(self):
        shaders = [
            shader
            for shader in (self.vert, self.frag, self.geo, self.tc, self.te)
            if isinstance(shader, Shader)
        ]
        error_message = 'Both a vertex and fragment shader must be provided'
        assert len(shaders) >= 2, error_message
        assert self.vert is not None and self.frag is not None, error_message
        # Attach Shaders
        for shader in shaders:
            if isinstance(shader, Shader):
                self.attach(shader)
        # Link Shaders
        gl.link_program(self.program)
        # Check for errors
        result = gl.get_programiv(self.program, gl.LINK_STATUS)
        log_length = gl.get_programiv(self.program, gl.INFO_LOG_LENGTH)
        assert result == 0 and log_length == 0, gl.get_program_info_log(self.program)
        # Cleanup shaders
        for shader in shaders:
            if isinstance(shader, Shader):
                shader.cleanup(program=self)

    def load(self, mode=gl.TRIANGLES, fill=gl.LINE, indices=[], **kwds):
        if not self.built:
            try:
                self.build()
            except RuntimeError as e:
                print 'Build failed: {}'.format(self)
                for arg in e.args:
                    print arg
            self.built = True
        if not self.loaded:
            self.loaded = True
            self.bits = gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT
            self.mode = mode
            self.fill = fill

            self.vao = gl.gen_vertex_arrays(1)

            self.buffer_id = gl.gen_buffers(1)
            self.indices_id = gl.gen_buffers(1)

            gl.bind_buffer(gl.ARRAY_BUFFER, self.buffer_id)
            gl.bind_buffer(gl.ELEMENT_ARRAY_BUFFER, self.indices_id)

            data = {}
            data_len = 0
            for key, val in kwds.items():
                if key in self.vert:
                    if self.vert[key] == 'uniform':
                        setattr(self.vert, key, val)
                    else:
                        data[key] = val if isinstance(val, np.ndarray) else array(val)
                        data_len = len(data[key])
                        setattr(self.vert, key, val)
            self.buffer = np.zeros(
                data_len,
                dtype=[(k, v.dtype, v.shape[-1]) for k, v in data.items()]
            )
            for key, val in data.items():
                self.buffer[key] = val
            if not indices:
                indices = range(data_len)
            if not isinstance(indices, np.ndarray):
                indices = array(indices)
            gl.buffer_data(gl.ELEMENT_ARRAY_BUFFER, indices.flatten(), gl.GL_STATIC_DRAW)

    def draw(self, **kwds):
        '''Converts list data into array data and binds numpy arrays to
        vertex shader inputs.'''
        self.load(**kwds)
        # Setup for drawing
        gl.clear(self.bits)
        gl.polygon_mode(gl.FRONT_AND_BACK, self.fill)
        gl.enable(gl.DEPTH_TEST)
        gl.depth_func(gl.LESS)
        gl.use_program(self.program)
        gl.buffer_data(gl.ARRAY_BUFFER, self.buffer.nbytes, self.buffer, gl.DYNAMIC_DRAW)
        gl.bind_vertex_array(self.vao)
        stride = self.buffer.strides[0]
        last_name = None
        for varindex, varname, vartype in enumerate(self.vert.bound_attributes.items()):
            if vartype == 'uniform':
                continue
            if last_name is None:
                offset = ctypes.c_void_p(0)
                last_name = varname
            else:
                offset = ctypes.c_void_p(self.buffer.dtype[last_name].itemsize)
            pos = gl.glGetAttribLocation(self.program, 'position')
            gl.glEnableVertexAttribArray(pos)
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.indices_buffer_id)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer_id)
            gl.glVertexAttribPointer(pos, self.buffer[varname].shape[-1], gl.GL_FLOAT, False, stride, offset)

    def __repr__(self):
        cname = self.__class__.__name__
        version = self.version
        shaders = ', '.join(['{}'.format(s) for s in (self.vert, self.frag, self.geo, self.tc, self.te) if s])
        string = '<{cname}{version} shaders=[{shaders}]>'.format(cname=cname, version=version, shaders=shaders)
        return string
