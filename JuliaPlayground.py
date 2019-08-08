"""Wrapper function for the Julia module."""
import numpy
from Julia import *

class JuliaPlayground:
    """Class wrapper functions for the Julia module."""

    def __init__(self,
                 width,
                 height,
                 xmin_mandel=-2.0,
                 xmax_mandel=1.0,
                 ymin_mandel=-1.3,
                 ymax_mandel=1.3,
                 xmin_julia=-2.0,
                 xmax_julia=2.0,
                 ymin_julia=-2.0,
                 ymax_julia=2.0,
                 zExponent=2.0,
                 niter=256,
                 bound=4.0):
        """Initialise the wrapper functions with variables for the julia and mandelbrot set."""
        self.width = width
        self.height = height
        self.xmin_mandel = xmin_mandel
        self.xmax_mandel = xmax_mandel
        self.ymin_mandel = ymin_mandel
        self.ymax_mandel = ymax_mandel
        self.xmin_julia = xmin_julia
        self.xmax_julia = xmax_julia
        self.ymin_julia = ymin_julia
        self.ymax_julia = ymax_julia
        self.zExponent = zExponent
        self.niter = niter
        self.bound = bound

    def mandelbrot(self):
        """Return the mandelbrot set as a 2-d numpy matrix."""
        return gen_mandelbrot(self.width, self.height, self.xmin_mandel, self.xmax_mandel, self.ymin_mandel, self.ymax_mandel, self.zExponent, self.niter, self.bound)

    def julia(self, cx, cy):
        """Return the julia set as a 2-d numpy matrix where c = complex(cx, cy)."""
        return gen_julia_set(self.width, self.height, cx, cy, self.xmin_julia, self.xmax_julia, self.ymin_julia, self.ymax_julia, self.zExponent, self.niter, self.bound)

    def update_zExponent(self, zExponent):
        """Return a list with the mandelbrot and julia set, updated with a new zExponent."""
        self.zExponent = zExponent
        return [self.mandelbrot(), self.julia()]

    def update_niter(self, niter):
        """Return a list with the mandelbrot and julia set, updated with a new niter."""
        self.niter = niter
        return [self.mandelbrot(), self.julia()]

    def update_bound(self, bound):
        """Return a list with the mandelbrot and julia set, updated with a new bound."""
        self.bound = bound
        return [self.mandelbrot(), self.julia()]

    def update_xmin_mandel(self, xmin_mandel):
        """Return a list with the mandelbrot and julia set, with a new xmin for the mandelbrot set."""
        self.xmin_mandel = xmin_mandel
        return [self.mandelbrot(), self.julia()]

    def update_xmax_mandel(self, xmax_mandel):
        """Return a list with the mandelbrot and julia set, with a new xmax for the mandelbrot set."""
        self.xmax_mandel = xmax_mandel
        return [self.mandelbrot(), self.julia()]

    def update_ymin_mandel(self, ymin_mandel):
        """Return a list with the mandelbrot and julia set, with a new ymin for the mandelbrot set."""
        self.ymin_mandel = ymin_mandel
        return [self.mandelbrot(), self.julia()]

    def update_ymax_mandel(self, ymax_mandel):
        """Return a list with the mandelbrot and julia set, with a new ymax for the mandelbrot set."""
        self.ymax_mandel = ymax_mandel
        return [self.mandelbrot(), self.julia()]

    def set_width(self, width):
        """Set the number of colors per row."""
        self.width = width

    def set_height(self, height):
        """Set the number of colors per column."""
        self.height = height

