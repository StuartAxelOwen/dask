from __future__ import absolute_import, division, print_function

import pytest
pytest.importorskip('numpy')

import dask.array as da
from dask.utils import ignoring
from dask.array.reductions import arg_aggregate
import numpy as np


def eq(a, b):
    if isinstance(a, da.Array):
        a = a.compute()
    if isinstance(b, da.Array):
        b = b.compute()
    if isinstance(a, (np.generic, np.ndarray)):
        return np.allclose(a, b)
    else:
        return a == b


def test_arg_reduction():
    pairs = [([4, 3, 5], [10, 11, 12]),
             ([3, 5, 1], [1, 2, 3])]
    result = arg_aggregate(np.min, np.argmin, (100, 100), pairs)
    assert eq(result, np.array([101, 11, 103]))


def reduction_1d_test(da_func, darr, np_func, narr, use_dtype=True):
    assert eq(da_func(darr), np_func(narr))
    assert eq(da_func(darr, keepdims=True), np_func(narr, keepdims=True))
    if use_dtype:
        assert eq(da_func(darr, dtype='f8'), np_func(narr, dtype='f8'))
        assert eq(da_func(darr, dtype='i8'), np_func(narr, dtype='i8'))


def test_reductions_1D_float():
    x = np.arange(5).astype('f4')
    a = da.from_array(x, chunks=(2,))

    reduction_1d_test(da.sum, a, np.sum, x)
    reduction_1d_test(da.prod, a, np.prod, x)
    reduction_1d_test(da.mean, a, np.mean, x)
    reduction_1d_test(da.var, a, np.var, x)
    reduction_1d_test(da.std, a, np.std, x)
    reduction_1d_test(da.min, a, np.min, x, False)
    reduction_1d_test(da.max, a, np.max, x, False)
    reduction_1d_test(da.any, a, np.any, x, False)
    reduction_1d_test(da.all, a, np.all, x, False)

    reduction_1d_test(da.nansum, a, np.nansum, x)
    with ignoring(AttributeError):
        reduction_1d_test(da.nanprod, a, np.nanprod, x)
    reduction_1d_test(da.nanmean, a, np.mean, x)
    reduction_1d_test(da.nanvar, a, np.var, x)
    reduction_1d_test(da.nanstd, a, np.std, x)
    reduction_1d_test(da.nanmin, a, np.nanmin, x, False)
    reduction_1d_test(da.nanmax, a, np.nanmax, x, False)

    assert eq(da.argmax(a, axis=0), np.argmax(x, axis=0))
    assert eq(da.argmin(a, axis=0), np.argmin(x, axis=0))
    assert eq(da.nanargmax(a, axis=0), np.nanargmax(x, axis=0))
    assert eq(da.nanargmin(a, axis=0), np.nanargmin(x, axis=0))


def test_reductions_1D_int():
    x = np.arange(5).astype('i4')
    a = da.from_array(x, chunks=(2,))

    reduction_1d_test(da.sum, a, np.sum, x)
    reduction_1d_test(da.prod, a, np.prod, x)
    reduction_1d_test(da.mean, a, np.mean, x)
    reduction_1d_test(da.var, a, np.var, x)
    reduction_1d_test(da.std, a, np.std, x)
    reduction_1d_test(da.min, a, np.min, x, False)
    reduction_1d_test(da.max, a, np.max, x, False)
    reduction_1d_test(da.any, a, np.any, x, False)
    reduction_1d_test(da.all, a, np.all, x, False)

    reduction_1d_test(da.nansum, a, np.nansum, x)
    with ignoring(AttributeError):
        reduction_1d_test(da.nanprod, a, np.nanprod, x)
    reduction_1d_test(da.nanmean, a, np.mean, x)
    reduction_1d_test(da.nanvar, a, np.var, x)
    reduction_1d_test(da.nanstd, a, np.std, x)
    reduction_1d_test(da.nanmin, a, np.nanmin, x, False)
    reduction_1d_test(da.nanmax, a, np.nanmax, x, False)

    assert eq(da.argmax(a, axis=0), np.argmax(x, axis=0))
    assert eq(da.argmin(a, axis=0), np.argmin(x, axis=0))
    assert eq(da.nanargmax(a, axis=0), np.nanargmax(x, axis=0))
    assert eq(da.nanargmin(a, axis=0), np.nanargmin(x, axis=0))


def reduction_2d_test(da_func, darr, np_func, narr, use_dtype=True):
    assert eq(da_func(darr), np_func(narr))
    assert eq(da_func(darr, keepdims=True), np_func(narr, keepdims=True))
    assert eq(da_func(darr, axis=0), np_func(narr, axis=0))
    assert eq(da_func(darr, axis=1), np_func(narr, axis=1))
    assert eq(da_func(darr, axis=1, keepdims=True),
              np_func(narr, axis=1, keepdims=True))
    assert eq(da_func(darr, axis=(1, 0)), np_func(narr, axis=(1, 0)))

    if use_dtype:
        assert eq(da_func(darr, dtype='f8'), np_func(narr, dtype='f8'))
        assert eq(da_func(darr, dtype='i8'), np_func(narr, dtype='i8'))


def test_reductions_2D_float():
    x = np.arange(1, 122).reshape((11, 11)).astype('f4')
    a = da.from_array(x, chunks=(4, 4))

    b = a.sum(keepdims=True)
    assert b._keys() == [[(b.name, 0, 0)]]

    reduction_2d_test(da.sum, a, np.sum, x)
    reduction_2d_test(da.prod, a, np.prod, x)
    reduction_2d_test(da.mean, a, np.mean, x)
    reduction_2d_test(da.var, a, np.var, x, False)  # Difference in dtype algo
    reduction_2d_test(da.std, a, np.std, x, False)  # Difference in dtype algo
    reduction_2d_test(da.min, a, np.min, x, False)
    reduction_2d_test(da.max, a, np.max, x, False)
    reduction_2d_test(da.any, a, np.any, x, False)
    reduction_2d_test(da.all, a, np.all, x, False)

    reduction_2d_test(da.nansum, a, np.nansum, x)
    with ignoring(AttributeError):
        reduction_2d_test(da.nanprod, a, np.nanprod, x)
    reduction_2d_test(da.nanmean, a, np.mean, x)
    reduction_2d_test(da.nanvar, a, np.nanvar, x, False)  # Difference in dtype algo
    reduction_2d_test(da.nanstd, a, np.nanstd, x, False)  # Difference in dtype algo
    reduction_2d_test(da.nanmin, a, np.nanmin, x, False)
    reduction_2d_test(da.nanmax, a, np.nanmax, x, False)

    assert eq(da.argmax(a, axis=0), np.argmax(x, axis=0))
    assert eq(da.argmin(a, axis=0), np.argmin(x, axis=0))
    assert eq(da.nanargmax(a, axis=0), np.nanargmax(x, axis=0))
    assert eq(da.nanargmin(a, axis=0), np.nanargmin(x, axis=0))


def test_reductions_2D_int():
    x = np.arange(1, 122).reshape((11, 11)).astype('i4')
    a = da.from_array(x, chunks=(4, 4))

    reduction_2d_test(da.sum, a, np.sum, x)
    reduction_2d_test(da.prod, a, np.prod, x)
    reduction_2d_test(da.mean, a, np.mean, x)
    reduction_2d_test(da.var, a, np.var, x, False)  # Difference in dtype algo
    reduction_2d_test(da.std, a, np.std, x, False)  # Difference in dtype algo
    reduction_2d_test(da.min, a, np.min, x, False)
    reduction_2d_test(da.max, a, np.max, x, False)
    reduction_2d_test(da.any, a, np.any, x, False)
    reduction_2d_test(da.all, a, np.all, x, False)

    reduction_2d_test(da.nansum, a, np.nansum, x)
    with ignoring(AttributeError):
        reduction_2d_test(da.nanprod, a, np.nanprod, x)
    reduction_2d_test(da.nanmean, a, np.mean, x)
    reduction_2d_test(da.nanvar, a, np.nanvar, x, False)  # Difference in dtype algo
    reduction_2d_test(da.nanstd, a, np.nanstd, x, False)  # Difference in dtype algo
    reduction_2d_test(da.nanmin, a, np.nanmin, x, False)
    reduction_2d_test(da.nanmax, a, np.nanmax, x, False)

    assert eq(da.argmax(a, axis=0), np.argmax(x, axis=0))
    assert eq(da.argmin(a, axis=0), np.argmin(x, axis=0))
    assert eq(da.nanargmax(a, axis=0), np.nanargmax(x, axis=0))
    assert eq(da.nanargmin(a, axis=0), np.nanargmin(x, axis=0))
    assert eq(da.argmax(a, axis=1), np.argmax(x, axis=1))
    assert eq(da.argmin(a, axis=1), np.argmin(x, axis=1))
    assert eq(da.nanargmax(a, axis=1), np.nanargmax(x, axis=1))
    assert eq(da.nanargmin(a, axis=1), np.nanargmin(x, axis=1))


def test_moment():
    def moment(x, n, axis=None):
        return ((x - x.mean(axis=axis, keepdims=True))**n).sum(
                axis=axis)/np.ones_like(x).sum(axis=axis)

    # Poorly conditioned
    x = np.array([1., 2., 3.]*10).reshape((3, 10)) + 1e8
    a = da.from_array(x, chunks=5)
    assert eq(a.moment(2), moment(x, 2))
    assert eq(a.moment(3), moment(x, 3))
    assert eq(a.moment(4), moment(x, 4))

    x = np.arange(1, 122).reshape((11, 11)).astype('f8')
    a = da.from_array(x, chunks=(4, 4))
    assert eq(a.moment(4, axis=1), moment(x, 4, axis=1))
    assert eq(a.moment(4, axis=(1, 0)), moment(x, 4, axis=(1, 0)))


def test_reductions_with_negative_axes():
    x = np.random.random((4, 4, 4))
    a = da.from_array(x, chunks=2)

    assert eq(a.argmin(axis=-1), x.argmin(axis=-1))

    assert eq(a.sum(axis=-1), x.sum(axis=-1))
    assert eq(a.sum(axis=(0, -1)), x.sum(axis=(0, -1)))


def test_nan():
    x = np.array([[1, np.nan, 3, 4],
                  [5, 6, 7, np.nan],
                  [9, 10, 11, 12]])
    d = da.from_array(x, chunks=(2, 2))

    assert eq(np.nansum(x), da.nansum(d))
    assert eq(np.nansum(x, axis=0), da.nansum(d, axis=0))
    assert eq(np.nanmean(x, axis=1), da.nanmean(d, axis=1))
    assert eq(np.nanmin(x, axis=1), da.nanmin(d, axis=1))
    assert eq(np.nanmax(x, axis=(0, 1)), da.nanmax(d, axis=(0, 1)))
    assert eq(np.nanvar(x), da.nanvar(d))
    assert eq(np.nanstd(x, axis=0), da.nanstd(d, axis=0))
    assert eq(np.nanargmin(x, axis=0), da.nanargmin(d, axis=0))
    assert eq(np.nanargmax(x, axis=0), da.nanargmax(d, axis=0))
    with ignoring(AttributeError):
        assert eq(np.nanprod(x), da.nanprod(d))


def test_0d_array():
    x = da.mean(da.ones(4, chunks=4), axis=0).compute()
    y = np.mean(np.ones(4))
    assert type(x) == type(y)

    x = da.sum(da.zeros(4, chunks=1)).compute()
    y = np.sum(np.zeros(4))
    assert type(x) == type(y)


def test_reduction_on_scalar():
    x = da.from_array(np.array(1.0), chunks=())
    assert (x == x).all()
