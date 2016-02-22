#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glfw
from glfw import gl
from PIL import Image
import numpy as np


class Texture(object):

    def __init__(self, image_path, texture_type=None, min_filter=None, mag_filter=None, wrap_r=None, wrap_s=None, wrap_t=None):
        assert glfw.core.init(), 'Error: GLFW could not be initialized'
        self.image_path = image_path
        texture_types = [gl.TEXTURE_1D, gl.TEXTURE_2D, gl.TEXTURE_3D]
        if texture_type not in texture_types:
            texture_type = gl.TEXTURE_2D
        self.texture_type = texture_type
        self.wrap_r = gl.REPEAT if wrap_r is None else wrap_r
        self.wrap_s = gl.REPEAT if wrap_s is None else wrap_s
        self.wrap_t = gl.REPEAT if wrap_t is None else wrap_t
        self.min_filter = gl.NEAREST if min_filter is None else min_filter
        self.mag_filter = gl.NEAREST if mag_filter is None else mag_filter
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
                gl.tex_image_2d(self.texture_type, 0, gl.RGB, width, height, 0, gl.RGB, gl.FLOAT, image_data)
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
