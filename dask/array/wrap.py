from __future__ import absolute_import, division, print_function

from itertools import count, product
from functools import partial

from toolz import curry
import numpy as np

from .core import Array, normalize_chunks, tokens
from .numpy_compat import full

names = ('wrapped_%d' % i for i in count(1))


def dims_from_size(size, blocksize):
    """

    >>> list(dims_from_size(30, 8))
    [8, 8, 8, 6]
    """
    result = (blocksize,) * (size // blocksize)
    if size % blocksize:
        result = result + (size % blocksize,)
    return result


def wrap_func_shape_as_first_arg(func, *args, **kwargs):
    """
    Transform np.random function into blocked version
    """
    if 'shape' not in kwargs:
        shape, args = args[0], args[1:]
    else:
        shape = kwargs.pop('shape')

    if not isinstance(shape, (tuple, list)):
        shape = (shape,)

    chunks = kwargs.pop('chunks', None)
    chunks = normalize_chunks(chunks, shape)
    name = kwargs.pop('name', None)

    dtype = kwargs.pop('dtype', None)
    if dtype is None:
        dtype = func(shape, *args, **kwargs).dtype

    name = name or next(names)

    keys = product([name], *[range(len(bd)) for bd in chunks])
    shapes = product(*chunks)
    func = partial(func, dtype=dtype, **kwargs)
    vals = ((func,) + (s,) + args for s in shapes)

    dsk = dict(zip(keys, vals))
    return Array(dsk, name, chunks, dtype=dtype)

@curry
def wrap(wrap_func, func, **kwargs):
    f = partial(wrap_func, func, **kwargs)
    f.__doc__ = """
    Blocked variant of %(name)s

    Follows the signature of %(name)s exactly except that it also requires a
    keyword argument chunks=(...)

    Original signature follows below.
    """ % {'name': func.__name__} + func.__doc__

    f.__name__ = 'blocked_' + func.__name__
    return f


w = wrap(wrap_func_shape_as_first_arg)

ones = w(np.ones, dtype='f8')
zeros = w(np.zeros, dtype='f8')
empty = w(np.empty, dtype='f8')
full = w(full)
