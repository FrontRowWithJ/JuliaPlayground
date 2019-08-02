import numpy
from numba import int32, float32, float64, guvectorize


# To calculate a point on the mandelbrot set, one
# must apply the function f(z_1) = z^2 + c
# where c is a complex number who's value corresponds
# to a the xy coordinate on the plane
# and the initial value for z is 0


@guvectorize([(float64[:], float64, float32, int32, float64, int32[:])], '(n),(),(),(),()->(n)', target='parallel')
def _get_mandel_color(cx, cy, zExponent, niter, bound, res):
    for i in range(cx.shape[0]):
        z = complex(0, 0)
        c = complex(cx[i], cy)
        for n in range(niter):
            if z.real * z.real + z.imag * z.imag > bound:
                res[i] = ((n << 9) + (n << 2) + n * 17) & 0xFF
                break
            z = z ** zExponent + c


@guvectorize([(float64[:], float64, float64, float64, float32, int32, float64, int32[:])], '(n),(),(),(),(),(),()->(n)', target='parallel')
def _get_julia_color(zr, zi, cr, ci, zExponent, niter, bound, res):
    for i in range(zr.shape[0]):
        z = complex(zr[i], zi)
        c = complex(cr, ci)
        for n in range(niter):
            if z.real * z.real + z.imag * z.imag > bound:
                res[i] = ((n << 6) + (n << 2) + n * 17) & 0xFF
                break
            z = z ** zExponent + c


def gen_mandelbrot(width, height, xmin, xmax, ymin, ymax, zExponent, niter, bound):
    res = numpy.zeros((height, width), numpy.int32)
    w = numpy.linspace(xmin, xmax, width)
    h = numpy.linspace(ymin, ymax, height)
    for i in range(height):
        _get_mandel_color(w, h[i], zExponent, niter, bound, res[i])
    return res


def gen_julia_set(width, height, x, y, xmin, xmax, ymin, ymax, zExponent, niter, bound):
    res = numpy.zeros((height, width), numpy.int32)
    w = numpy.linspace(xmin, xmax, width)
    h = numpy.linspace(ymin, ymax, height)
    for i in range(height):
        _get_julia_color(w, h[i], x, y, zExponent, niter, bound, res[i])
    return res
