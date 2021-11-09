import numpy as np

from kino import math


def test_smoothing():
    X = np.arange(100)

    X_smooth = math.smooth(X)

    assert len(X) == len(X_smooth)
