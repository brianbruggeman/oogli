#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ctypes
from collections import OrderedDict

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
        self.tc = TessellationControlShader(tc) if tc is not None else None
        self.te = TessellationEvaluationShader(te) if te is not None else None
        self.geo = GeometryShader(geo) if geo is not None else None
        self.loaded = False
        self.built = False
        self.bound_attributes = OrderedDict()

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
        elif isinstance(shader, TessellationControlShader):
            self.tc = shader
        elif isinstance(shader, TessellationEvaluationShader):
            self.te = shader
        elif isinstance(shader, GeometryShader):
            self.geo = shader
        shader.compile()
        shader.attach(self)

    def build(self):
        shaders = [
            shader
            for shader in (self.vert, self.frag, self.tc, self.te, self.geo)
            if isinstance(shader, Shader)
        ]
        error_message = 'Both a vertex and fragment shader must be provided.'
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
        assert result == gl.TRUE and log_length == 0, gl.get_program_info_log(self.program)
        self.bound_attributes = OrderedDict((k, v) for k, v in self.vert.bound_attributes.items())
        # Cleanup shaders
        for shader in shaders:
            if isinstance(shader, Shader):
                shader.cleanup(program=self)
        # Bind the attributes based on their index in bound_attributes
        for index, varname in enumerate(self.bound_attributes):
            gl.bind_attrib_location(self.program, index, varname)

    def load(self, mode=gl.TRIANGLES, fill=gl.LINE, indices=[], data=[], **kwds):
        if not self.built:
            try:
                self.build()
            except RuntimeError as e:
                print('Build failed: {}'.format(self))
                for arg in e.args:
                    print(arg)
            self.built = True
        if not self.loaded:
            self.loaded = True
            self.bits = gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT
            self.mode = mode
            self.fill = fill

            self.buffer = kwds.pop('data', data)
            data_len = len(self.buffer)
            if data_len == 0:
                data = {}
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
                self.indices = range(data_len)
            else:
                self.indices = indices
            if not isinstance(self.indices, np.ndarray):
                self.indices = array(self.indices, vtype=np.uint32)

            self.vao = gl.gen_vertex_arrays(1)

            self.buffer_id = gl.gen_buffers(1)
            self.indices_id = gl.gen_buffers(1)

            gl.bind_buffer(gl.ARRAY_BUFFER, self.buffer_id)
            gl.bind_buffer(gl.ELEMENT_ARRAY_BUFFER, self.indices_id)
            gl.buffer_data(gl.ELEMENT_ARRAY_BUFFER, self.indices.flatten(), gl.GL_STATIC_DRAW)

    def draw(self, mode=gl.TRIANGLES, fill=gl.LINE, indices=[], data=[], **kwds):
        '''Converts list data into array data and binds numpy arrays to
        vertex shader inputs.'''
        if data or indices:
            self.loaded = False
        self.load(mode=mode, fill=fill, indices=indices, data=data, **kwds)
        # Setup for drawing
        gl.clear(self.bits)
        gl.polygon_mode(gl.FRONT_AND_BACK, fill or self.fill)
        gl.buffer_data(gl.ARRAY_BUFFER, self.buffer.nbytes, self.buffer, gl.DYNAMIC_DRAW)
        gl.enable(gl.DEPTH_TEST)
        gl.depth_func(gl.LESS)
        gl.use_program(self.program)

        gl.bind_vertex_array(self.vao)
        stride = self.buffer.strides[0]
        # vert = gl.glGetAttribLocation(self.program, 'vertices')
        # gl.glEnableVertexAttribArray(vert)
        # gl.glBindBuffer(gl.ELEMENT_ARRAY_BUFFER, self.indices_id)
        # gl.glBindBuffer(gl.ARRAY_BUFFER, self.buffer_id)
        # gl.glVertexAttribPointer(vert, self.buffer['vertices'].shape[-1], gl.FLOAT, False, stride, None)

        last_varname = None
        for varindex, vardata in enumerate(self.bound_attributes.items()):
            varname, vartype = vardata
            if last_varname is None or varname == last_varname:
                offset = ctypes.c_void_p(0)
                last_varname = varname
            else:
                offset = ctypes.c_void_p(self.buffer.dtype[last_varname].itemsize)
            gl.enable_vertex_attrib_array(varindex)
            gl.bind_buffer(gl.ELEMENT_ARRAY_BUFFER, self.indices_id)
            gl.bind_buffer(gl.ARRAY_BUFFER, self.buffer_id)
            gl.vertex_attrib_pointer(
                varindex,
                self.buffer[varname].shape[-1],
                gl.GL_FLOAT,
                False,
                stride,
                offset
            )
        gl.draw_elements(mode or self.mode, len(self.indices), gl.GL_UNSIGNED_INT, None)
        gl.glDisableVertexAttribArray(self.vao)

    def __repr__(self):
        cname = self.__class__.__name__
        version = self.version
        shaders = ', '.join(['{}'.format(s) for s in (self.vert, self.frag, self.tc, self.te, self.geo) if s])
        string = '<{cname}{version} shaders=[{shaders}]>'.format(cname=cname, version=version, shaders=shaders)
        return string
