import numpy as np

from kino.geometry import Vector


def test_vector_single():
    vec = Vector(1, 2)

    assert vec.x == 1
    assert vec.y == 2
    assert vec.single_vec is True
    assert len(vec) == 1

    print(vec)


def test_vector_multi():
    vec = Vector([1, 2], [3, 4])
    vec2 = Vector(np.array([1, 2, 3]), np.array([3, 4, 5]))

    assert len(vec) == 2
    assert len(vec2) == 3


def test_vec_properties():
    v1 = Vector(0, 2)

    assert v1.magnitude == 2
    assert v1.angle == 90
    assert v1.to_unit_vector().magnitude == 1

    v2 = Vector(2, 0)

    assert v1.dot(v2) == 0
    assert v1.angle_with(v2) == 90
