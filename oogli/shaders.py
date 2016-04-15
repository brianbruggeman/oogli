#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from collections import OrderedDict
from textwrap import dedent as dd

import glfw
from glfw import gl


class Shader(object):

    '''Wrapper for opengl boilerplate code'''

    def __init__(self, source):
        assert glfw.core.init(), 'Error: GLFW could not be initialized'
        self.inputs = OrderedDict()
        self.outputs = OrderedDict()
        self.uniforms = OrderedDict()
        self.source = dd('\n'.join([l for l in source.split('\n') if l.strip()]))
        self.parse(source)
        self.compiled = False

    @property
    def shader(self):
        if not hasattr(self, '_id'):
            self._id = gl.create_shader(self.opengl_type)
        return self._id

    def compile(self):
        '''Compiles and checks output'''
        if not self.compiled:
            shader_id = self.shader
            gl.shader_source(shader_id, self.source)
            gl.compile_shader(shader_id)
            result = gl.get_shaderiv(shader_id, gl.COMPILE_STATUS)
            log_length = gl.get_shaderiv(shader_id, gl.INFO_LOG_LENGTH)
            log = ''
            if log_length != 0:
                log = gl.get_shader_info_log(shader_id)
            if log.strip():
                assert result == gl.TRUE and log_length == 0, log
            self.compiled = True
            return shader_id

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

    def cleanup(self, program):
        self.detach(program)
        self.delete()

    def __del__(self):
        self.delete()

    def __contains__(self, key):
        return key in self.inputs or key in self.uniforms

    def __getitem__(self, key):
        if key not in self.inputs and key not in self.uniforms:
            raise KeyError('Could not set "{}"'.format(key))
        else:
            if key in self.inputs:
                return self.inputs[key]
            elif key in self.uniforms:
                return self.uniforms[key]

    def __setitem__(self, key, val):
        if key in self.inputs or key in self.uniforms:
            setattr(self, key, val)
        else:
            raise KeyError('Could not set "{}"'.format(key))

    def __iter__(self):
        for key in self.inputs:
            yield key
        for key in self.uniforms:
            yield key

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
        win = glfw.create_window(title='test', width=1, height=1)
        if win is not None:
            glfw.core.destroy_window(win)
        return major, minor

    def parse(self, source):
        '''Parses source looking for context required as well as
        inputs and uniforms'''
        opengl_mapping = {
            (1, 1): (2, 0),
            (1, 2): (2, 1),
            (1, 3): (3, 0),
            (1, 4): (3, 1),
            (1, 5): (3, 2),
        }
        version_pattern = r'^\#version\s+(?P<version>[0-9]+)\s*$'
        inputs2_pattern = ("\s*GLSL_TYPE\s+"
                           "((highp|mediump|lowp)\s+)?"
                           "(?P<vartype>\w+)\s+"
                           "(?P<varname>\w+)\s*"
                           "(\[(?P<varsize>\d+)\])?"
                           "(\s*\=\s*(?P<vardefault>[0-9.]+))?"
                           "\s*;"
                           )
        inputs_pattern = (
            r'(?P<direction>(in|out|uniform))\s+'
            r'((highp|mediump|lowp)\s+)?'
            r'(?P<vartype>\w+)\s+'
            r'(?P<varname>\w+)\s*'
            r'(\s*\=\s*(?P=vartype)?(?P<vardefault>(.+)))?'
            r'\;'
        )
        version_eng = re.compile(version_pattern)
        self.version = major, minor = (3, 2)
        engines = (
            [re.compile(inputs_pattern)] +
            [
                re.compile(inputs2_pattern.replace('GLSL_TYPE', kind), flags=re.MULTILINE)
                for kind in ('uniform', 'attribute', 'varying', 'const')
            ]
        )
        for line in source.split('\n'):
            line = line.strip()
            if version_eng.search(line):
                data = [m.groupdict() for m in version_eng.finditer(line)][0]
                version = tuple([int(c) for c in data['version']][:2])
                self.version = opengl_mapping.get(version, version)
            for eng in engines:
                if eng.search(line):
                    data = [m.groupdict() for m in eng.finditer(line)][0]
                    varname = data['varname']
                    vartype = data['vartype']
                    direction = data['direction']
                    default = data['vardefault']
                    if direction == 'in':
                        setattr(self, varname, vartype)
                        self.inputs[varname] = vartype
                    elif direction == 'out':
                        setattr(self, varname, vartype)
                        self.outputs[varname] = vartype
                    elif direction == 'uniform':
                        setattr(self, varname, vartype)
                        if default:
                            self.uniforms[varname] = ('uniform', vartype, default)
                        else:
                            self.uniforms[varname] = ('uniform', vartype, )
                    break
        self.set_context(self.version)

    def __repr__(self):
        cname = self.__class__.__name__
        version = self.version
        inputs = ''
        uniforms = ''
        if self.inputs.keys():
            inputs = 'inputs=[{}]'.format(', '.join(a for a in self.inputs.keys()))
        if self.uniforms.keys():
            uniforms = 'uniforms=[{}]'.format(', '.join(a for a in self.uniforms.keys()))
            if inputs:
                uniforms = ' {}'.format(uniforms)
        string = '<{cname}{version} {inputs}{uniforms}>'.format(**locals())
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
