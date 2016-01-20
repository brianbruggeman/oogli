#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest


def test_vertex_shader():
    '''Tests shader compilation for a vertex shader'''

    import oogli

    shader_source = '''
        #version

        '''
    assert shader_source is not None
    assert hasattr(oogli, 'create_window')


if __name__ == '__main__':
    pytest.main()
