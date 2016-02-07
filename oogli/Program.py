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
from .utils import uniform_mapping


def array(val, vtype=np.float32):
    mapping = {
        'vec2': 'f',
        'vec3': 'f',
        'vec4': 'f',
    }
    if vtype not in dir(np):
        vtype = mapping.get(vtype, vtype)
    if not isinstance(val, np.ndarray):
        val = np.array(val, dtype=vtype)
    return val


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
        self.created = False
        self.inputs = OrderedDict()
        self.uniforms = OrderedDict()

    @property
    def program(self):
        if not hasattr(self, '_program'):
            self._program = gl.create_program()
            self.created = True
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
        program_id = self.program
        assert program_id != 0
        error_message = 'Both a vertex and fragment shader must be provided.'
        assert len(shaders) >= 2, error_message
        assert self.vert is not None and self.frag is not None, error_message
        # Attach Shaders
        for shader in shaders:
            if isinstance(shader, Shader):
                self.attach(shader)
                for varname in shader:
                    val = shader[varname]
                    if isinstance(val, (tuple, list)) and val[0] == 'uniform':
                        self.uniforms[varname] = shader

        # Link Shaders
        gl.link_program(program_id)
        # Check for errors
        result = gl.get_programiv(program_id, gl.LINK_STATUS)
        log_length = gl.get_programiv(program_id, gl.INFO_LOG_LENGTH)
        log = ''
        if log_length != 0:
            log = gl.get_program_info_log(program_id)
        if log.strip():
            assert result == gl.TRUE and log_length == 0, log
        self.inputs = OrderedDict((k, v) for k, v in self.vert.inputs.items())
        # Cleanup shaders
        for shader in shaders:
            if isinstance(shader, Shader):
                shader.cleanup(program=self)
        # Bind the attributes based on their index in bound_attributes
        for index, varname in enumerate(self.inputs):
            gl.bind_attrib_location(program_id, index, varname)
        # Bind the uniforms based on their index in bound_attributes
        for index, varname in enumerate(self.uniforms):
            shader = self.uniforms[varname]
            vardata = shader[varname]
            loc = gl.get_uniform_location(self.program, varname)
            vartype = vardata[1]
            mapping = uniform_mapping[vartype]
            uniform_binder = lambda data: mapping(loc, *array(data, vartype))
            self.uniforms[varname] = uniform_binder
        self.built = True

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

            # TODO:  FIX THIS!
            if not isinstance(data, np.ndarray):
                data = np.array(data, dtype='f')
            data_len = len(data)
            if data_len == 0:
                interleaved = OrderedDict()
                for key in self.inputs.keys() + self.uniforms.keys():
                    if key in kwds and key in self.vert:
                        val = kwds[key]
                        if key in self.uniforms:
                            setattr(self, key, val)
                        else:
                            interleaved[key] = val if isinstance(val, np.ndarray) else array(val)
                            data_len = len(interleaved[key])
                            setattr(self.vert, key, val)
                self.buffer = np.zeros(
                    data_len,
                    dtype=[(k, v.dtype, v.shape[-1]) for k, v in interleaved.items()]
                )
                for key, val in interleaved.items():
                    self.buffer[key] = val
            elif not hasattr(self, 'buffer'):
                self.buffer = data

            if isinstance(indices, list) and not indices:
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
        return self.buffer

    def draw(self, mode=gl.TRIANGLES, fill=gl.LINE, indices=[], data=[], **kwds):
        '''Converts list data into array data and binds numpy arrays to
        vertex shader inputs.'''
        if isinstance(data, list) and data or isinstance(indices, list) and indices:
            self.loaded = False
        self.load(mode=mode, fill=fill, indices=indices, data=data, **kwds)
        # Setup for drawing
        gl.clear(self.bits)
        gl.polygon_mode(gl.FRONT_AND_BACK, fill or self.fill)
        gl.enable(gl.DEPTH_TEST)
        gl.depth_func(gl.LESS)
        gl.use_program(self.program)

        gl.bind_vertex_array(self.vao)
        gl.buffer_data(gl.ARRAY_BUFFER, self.buffer.nbytes, self.buffer, gl.DYNAMIC_DRAW)
        stride = self.buffer.strides[0]

        last_varname = None
        for varindex, vardata in enumerate(self.inputs.items()):
            varname, vartype = vardata
            if last_varname is None:
                offset = None
                last_varname = varname
            else:
                offset = self.buffer.dtype[last_varname].itemsize
            loc = gl.glGetAttribLocation(self.program, varname)
            offset = ctypes.c_void_p(offset)
            gl.enable_vertex_attrib_array(loc)
            gl.bind_buffer(gl.ELEMENT_ARRAY_BUFFER, self.indices_id)
            gl.vertex_attrib_pointer(
                loc,
                self.buffer[varname].shape[-1],
                gl.GL_FLOAT,
                False,
                stride,
                offset
            )
        for varname, binder in self.uniforms.items():
            vardata = kwds.get(varname, getattr(self, varname, None))
            if vardata:
                binder(vardata)
        gl.draw_elements(mode or self.mode, len(self.indices), gl.GL_UNSIGNED_INT, None)
        gl.glDisableVertexAttribArray(self.vao)
        return self.buffer

    def __repr__(self):
        cname = self.__class__.__name__
        version = self.version
        shaders = ', '.join(['{}'.format(s) for s in (self.vert, self.frag, self.tc, self.te, self.geo) if s])
        string = '<{cname}{version} shaders=[{shaders}]>'.format(cname=cname, version=version, shaders=shaders)
        return string
