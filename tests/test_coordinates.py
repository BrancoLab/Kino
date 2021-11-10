import numpy as np

from kino.geometry import coordinates, Vector


def test_rotation_matrix():
    # test with a single array
    arr = np.array([1, 0])  # oriented along the X

    rot = coordinates.R(90)  # rotate 90 degrees counter clockwise

    rotated = rot @ arr

    assert rotated[0] < 0.001
    assert rotated[1] == 1
    assert np.dot(arr, rotated) < 0.001

    # test with vectors - single
    vec = Vector(1, 0)
    rot = vec.rotate(90)

    assert isinstance(rot, Vector)
    assert rot.dot(vec) == vec.dot(rot)
    assert rot.dot(vec) < 0.001
    assert rot.angle2 == 90

    # test with vectors - multi
    vec = Vector([1, 1, 1], [0, 0, 0])
    rot = vec.rotate(90)

    assert isinstance(rot, Vector)
    assert len(vec) == len(vec)
    assert rot.dot(vec)[0] == vec.dot(rot)[0]
    assert rot.dot(vec)[0] < 0.001
    assert rot.angle2[0] == 90
