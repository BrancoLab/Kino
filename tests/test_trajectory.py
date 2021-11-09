import numpy as np

from kino.geometry import Trajectory, Vector
from kino.draw import draw


def test_trajectory_basic():
    x = np.linspace(0, np.pi * 2, 300)
    y = np.cos(x)

    path = Trajectory(x, y)
    print(path)

    assert len(path) == 300

    # test indexing
    assert isinstance(path[0], Vector)
    assert isinstance(path["speed"], np.ndarray)
    assert isinstance(path["velocity"], Vector)

    # trimming
    short = path.trim(50, 150)
    assert len(short) == 100


def test_draw_trajectory():
    x = np.linspace(0, np.pi * 2, 300)
    y = np.cos(x)

    path = Trajectory(x, y)
    draw(path, show_vectors=True, vectors_scale=0.3)
