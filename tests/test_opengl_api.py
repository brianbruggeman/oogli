#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

import re


def _camelToSnake(string):
    patterns = [
        (r'(.)([0-9]+)', r'\1_\2'),
        # (r'(.)([A-Z][a-z]+)', r'\1_\2'),
        # (r'(.)([0-9]+)([a-z]+)', r'\1_\2\3'),
        (r'([a-z]+)([A-Z])', r'\1_\2'),
    ]
    engines = [
        (pattern, replacement, re.compile(pattern))
        for pattern, replacement in patterns
    ]
    for data in engines:
        pattern, replacement, eng = data
        string = eng.sub(replacement, string)
    string = string.lower()
    return string


def test_snake_case_conversion():
    '''Tests parity between snake case and non-snake case api'''
    from oogli import gl

    gl_uppers = [d for d in dir(gl) if d.upper() == d and d.startswith('GL_')]
    non_gl_uppers = [d for d in dir(gl) if d.upper() == d and not d.startswith('GL_')]
    if len(gl_uppers) != len(non_gl_uppers):
        for gl_api in gl_uppers:
            assert gl_api.replace('GL_', '') in non_gl_uppers

    gl_lowers = [d for d in dir(gl) if d.upper() != d and d.lower() != d and d.startswith('gl')]
    non_gl_lowers = [d for d in dir(gl) if d.upper() != d and d.lower() == d and not d.startswith(('gl', '_'))]
    if len(gl_lowers) != len(non_gl_lowers):
        for gl_api in gl_lowers:
            _gl_api = _camelToSnake(gl_api.replace('gl', ''))
            assert _gl_api in non_gl_lowers

    # A few explicit checks
    assert 'glDetachShader' in gl_lowers
    assert 'detach_shader' in non_gl_lowers
    assert gl.glDetachShader == gl.detach_shader

    assert 'glDeleteShader' in gl_lowers
    assert 'delete_shader' in non_gl_lowers
    assert gl.glDeleteShader == gl.delete_shader


if __name__ == '__main__':
    pytest.main()
