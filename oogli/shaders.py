#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict
import re

import glfw
from glfw import gl


class Shader(object):
    '''Wrapper for opengl boilerplate code'''

    def __init__(self, source):
        assert glfw.core.init(), 'Error: GLFW could not be initialized'
        self.bound_attributes = OrderedDict()
        self.source = source
        self.parse(source)
        self.compiled = False

    @property
    def shader(self):
        if not hasattr(self, '_id'):
            self._id = gl.create_shader(self.opengl_type)
        return self._id

    def compile(self):
        gl.shader_source(self.shader, self.source)
        result = gl.get_shaderiv(self.shader, gl.COMPILE_STATUS)
        log_length = gl.get_shaderiv(self.shader, gl.INFO_LOG_LENGTH)
        assert result == 0 and log_length == 0, gl.get_shader_info_log(self.shader)
        self.compiled = True

    def attach(self, program):
        if not self.compiled:
            self.compile()
        gl.attach_shader(program.program, self.shader)

    def detach(self, program):
        if self.shader is not None:
            gl.detach_shader(program.program, self.shader)

    def delete(self):
        if self.shader is not None:
            gl.delete_shader(self.shader)
            self.shader = None

    def cleanup(self, program):
        self.detach(program)
        self.delete()

    def __contains__(self, key):
        return key in self.bound_attributes

    def __getitem__(self, key):
        if key not in self.bound_attributes:
            raise KeyError('Could not set "{}"'.format(key))
        else:
            return self.bound_attributes[key]

    def __setitem__(self, key, val):
        if key in self.bound_attributes:
            setattr(self, key, val)
        else:
            raise KeyError('Could not set "{}"'.format(key))

    def set_context(self, version):
        major, minor = version
        glfw.core.window_hint(glfw.FOCUSED, False)
        glfw.core.window_hint(glfw.CONTEXT_VERSION_MAJOR, major)
        glfw.core.window_hint(glfw.CONTEXT_VERSION_MINOR, minor)
        profile = glfw.OPENGL_ANY_PROFILE if version < (3, 2) else glfw.OPENGL_CORE_PROFILE
        glfw.core.window_hint(glfw.OPENGL_PROFILE, profile)
        # Setup forward compatibility if able
        forward_compat = False if version < (3, 0) else True
        glfw.core.window_hint(glfw.OPENGL_FORWARD_COMPAT, forward_compat)
        #  Keep the window invisible
        glfw.core.window_hint(glfw.VISIBLE, False)
        assert glfw.create_window(title='test', width=1, height=1)

    def parse(self, source):
        '''Parses source looking for context required as well as
        inputs and uniforms'''
        version_pattern = r'^\#version\s+(?P<version>[0-9]+)\s*$'
        inputs_pattern = r'^in (?P<vartype>[a-zA-Z_0-9]+)\s+(?P<varname>[a-zA-Z_0-9]+)\s*\;$'
        version_eng = re.compile(version_pattern)
        inputs_eng = re.compile(inputs_pattern)
        self.version = major, minor = (3, 2)
        for line in source.split('\n'):
            line = line.strip()
            if version_eng.search(line):
                data = [m.groupdict() for m in version_eng.finditer(line)][0]
                self.version = tuple([int(c) for c in data['version']][:2])
            if inputs_eng.search(line):
                data = [m.groupdict() for m in inputs_eng.finditer(line)][0]
                varname = data['varname']
                vartype = 'var' if data['vartype'] != 'uniform' else 'uniform'
                setattr(self, varname, None)
                self.bound_attributes[varname] = vartype
        self.set_context(self.version)

    def __repr__(self):
        cname = self.__class__.__name__
        version = self.version
        vars = ', '.join(a for a in self.bound_attributes)
        string = '<{cname}{version} vars=[{vars}]>'.format(cname=cname, version=version, vars=vars)
        return string


class VertexShader(Shader):

    opengl_type = gl.VERTEX_SHADER


class FragmentShader(Shader):

    opengl_type = gl.FRAGMENT_SHADER


class GeometryShader(Shader):

    opengl_type = gl.GEOMETRY_SHADER


class TessellationControlShader(Shader):

    opengl_type = gl.TESS_CONTROL_SHADER


class TessellationEvaluationShader(Shader):

    opengl_type = gl.TESS_EVALUATION_SHADER
