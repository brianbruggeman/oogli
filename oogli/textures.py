#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import glfw
import numpy as np
from glfw import gl
from PIL import Image


class Texture(object):

    def __init__(self, image_path, type=None, filter=None, wrap=None):
        '''Creates a texture'''
        assert glfw.core.init(), 'Error: GLFW could not be initialized'
        self.image_path = image_path
        if not os.path.exists(image_path):
            raise IOError('Could not find image: {}'.format(image_path))
        texture_types = [gl.TEXTURE_1D, gl.TEXTURE_2D, gl.TEXTURE_3D]
        self.texture_type = gl.TEXTURE_2D if type not in texture_types else type
        if filter is None:
            filter = gl.NEAREST
        if wrap is None:
            wrap = gl.REPEAT
        self.wrap_r = wrap
        self.wrap_s = wrap
        self.wrap_t = wrap
        self.min_filter = filter
        self.mag_filter = filter
        self.size = None

    @property
    def texture(self):
        if not hasattr(self, '_id'):
            self._id = gl.gen_textures(1)
            gl.bind_texture(self.texture_type, self._id)
            gl.tex_parameteri(self.texture_type, gl.TEXTURE_WRAP_R, self.wrap_r)
            gl.tex_parameteri(self.texture_type, gl.TEXTURE_WRAP_S, self.wrap_s)
            gl.tex_parameteri(self.texture_type, gl.TEXTURE_WRAP_T, self.wrap_t)
            gl.tex_parameteri(self.texture_type, gl.TEXTURE_MIN_FILTER, self.min_filter)
            gl.tex_parameteri(self.texture_type, gl.TEXTURE_MAG_FILTER, self.mag_filter)
            with Image.open(self.image_path) as image:
                image_data = np.array(list(image.getdata()), np.uint8)
                self.size = width, height = image.width, image.height
                mapping = {
                    gl.TEXTURE_1D: gl.tex_image_1d,
                    gl.TEXTURE_2D: gl.tex_image_2d,
                    gl.TEXTURE_3D: gl.tex_image_3d
                }
                func = mapping[self.texture_type]
                func(self.texture_type, 0, gl.RGB, width, height, 0, gl.RGB, gl.FLOAT, image_data)
        return self._id

    def __repr__(self):
        cname = self.__class__.__name__
        texture_id = self.texture
        image_path = self.image_path
        size = ''
        if self.size:
            size = ' ({}, {})'.format(*self.size)
        string = '<{cname}:{texture_id} {image_path}{size}>'.format(**locals())
        return string
