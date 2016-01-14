oogli
---------
[![Build Status](https://travis-ci.org/brianbruggeman/oogli.svg)](https://travis-ci.org/brianbruggeman/oogli)
[![PyPI version](https://img.shields.io/pypi/v/oogli.svg)](https://pypi.python.org/pypi/oogli)
[![Status](https://img.shields.io/pypi/status/oogli.svg)](https://pypi.python.org/pypi/oogli)
[![Python Compatibility](https://img.shields.io/pypi/pyversions/oogli.svg)](https://pypi.python.org/pypi/oogli)
[![Downloads](https://img.shields.io/pypi/dm/oogli.svg?period=week)](https://pypi.python.org/pypi/oogli)
[![Coverage Status](https://coveralls.io/repos/brianbruggeman/oogli/badge.svg?branch=develop&service=github)](https://coveralls.io/github/brianbruggeman/oogli?branch=develop)

Oogli is Beautiful

Object Oriented Graphics Library Interface written in Python

## Motivation:

I was dissatisfied with difficulty in producing easy to read and understand
OpenGL code.  This small library helps eliminate some of the boilerplate
inherent within OpenGL's API.  Oogli greatly simplifies the interface
while still providing access to the underlying GLFW3 and OpenGL API.

## License:

This package is released as Apache 2.0 license.

However, at your option, you may apply any OSI approved free software
license you choose provided that you adhere to the free software license
chosen and additionally follow these criteria:

 a. list the author's name of this software as a contributor to your
    final product

 b. provide credit to your end user of your product or software without
    your end user asking for where you obtained your software

 c. notify the author of this software that you are using this software

 d. If you believe there can be some benefit in providing your changes
    upstream, you'll submit a change request.  While this criteria is
    completely optional, please consider not being a dick.

## Installation:

Oogli was designed with GLFW-CFFI in mind and uses the API provided by
GLFW-CFFI.  In addition, Oogli uses numpy.

### Installing via pip

Install via `pip install oogli`.

### Installing GLFW-CFFI via pip

Install via `pip install glfw-cffi`.

### Installing Numpy via pip

Install via `pip install numpy`.

### Installing GLFW3

GLFW3 is available for several different platforms:

- Ubuntu/Debian: `sudo apt-get install -y libglfw3-dev`
- Fedora/Red Hat: `sudo yum install -y libglfw3-dev`
- Mac OS X with Homebrew: `brew install glfw3`
- Windows: There is an installer available
  [64-bit Windows](https://github.com/glfw/glfw/releases/download/3.1.2/glfw-3.1.2.bin.WIN64.zip) or
  [32-bit Windows](https://github.com/glfw/glfw/releases/download/3.1.2/glfw-3.1.2.bin.WIN32.zip)

GLFW3 is relatively new, so some older installations of Linux may not have
`libglfw` directly available.  You may check out the [travis.yml](https://github.com/brianbruggeman/glfw-cffi/blob/master/.travis.yml#L34-L52)
file within our github repo for more information on setup on older systems.

## Usage:

### Sample Usage:

This is the required code to produce a shaded triangle using oogli:

    import oogli

    v_shader = '''
        #version 410
        in vec2 vertices;
        void main () {
            gl_Position = vec4(vertices, 0.0, 1.0);
        }
    '''

    f_shader = '''
        #version 410
        out vec4 frag_color;
        void main () {
            frag_colour = vec4(0.3, 1.0, 0.3, 1.0);
        }
    '''

    # Create a program from the shaders
    #  Note: This will auto request an OpenGL context of 4.1
    program = oogli.Program(v_shader, f_shader)

    # Vertices for a 2D Triangle
    triangle = [(0.0, 0.5), (-0.5, 0.5), (-0.5, -0.5)]

    with oogli.Window('Oogli', 640, 480) as win:
        # Main Loop
        while win.should_run()
            # Render triangle
            program.draw(vertices=triangle)

More complex examples can be found within the examples folder on the github repo.


## Contributions:

Contributions are welcome. When opening a PR, please keep the following guidelines in mind:

- Before implementing, please open an issue for discussion.
- Make sure you have tests for the new logic.
- Make sure your code passes `flake8`
- Add yourself to contributors at `README.md` and/or  your contributions.

## Contributors

* [Brian Bruggeman](https://github.com/brianbruggeman) - Originator
