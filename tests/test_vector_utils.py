import numpy as np


from kino.geometry import Vector
from kino.geometry import vectors_utils as vu


def test_vec_smoothing():
    vec = Vector(np.array([1] * 20), np.array([1] * 20))

    smooth = vu.smooth_vector(vec)

    assert len(vec) == len(smooth)
