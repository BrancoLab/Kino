import numpy as np
from typing import Tuple
from kino.geometry.vector import Vector

np.seterr(all="ignore")


def compute_vectors_from_coordinates(
    x: np.ndarray, y: np.ndarray, fps: int = 1
) -> Tuple[Vector, Vector, Vector, Vector, np.array]:
    """
        Given the X and Y position at each frame -

        Compute vectors:
            i. velocity vector
            ii. unit tangent 
            iii. unit norm
            iv. acceleration

        and scalar quantities:
            i. speed
            ii. curvature
        
        See: https://stackoverflow.com/questions/28269379/curve-curvature-in-numpy
    """
    # compute velocity vector
    dx_dt = np.gradient(x)
    dy_dt = np.gradient(y)
    velocity = (
        np.array([[dx_dt[i], dy_dt[i]] for i in range(dx_dt.size)]) * fps
    )

    # compute scalr speed vector
    ds_dt = np.sqrt(dx_dt * dx_dt + dy_dt * dy_dt)

    # get unit tangent vector
    tangent = np.array([1 / ds_dt] * 2).transpose() * velocity
    unit_tangent = tangent / np.apply_along_axis(
        np.linalg.norm, 1, tangent
    ).reshape(len(tangent), 1)

    # get unit normal vector
    tangent_x = tangent[:, 0]
    tangent_y = tangent[:, 1]

    deriv_tangent_x = np.gradient(tangent_x)
    deriv_tangent_y = np.gradient(tangent_y)

    dT_dt = np.array(
        [
            [deriv_tangent_x[i], deriv_tangent_y[i]]
            for i in range(deriv_tangent_x.size)
        ]
    )

    length_dT_dt = np.sqrt(
        deriv_tangent_x * deriv_tangent_x + deriv_tangent_y * deriv_tangent_y
    )

    normal = np.array([1 / length_dT_dt] * 2).transpose() * dT_dt

    # get acceleration and curvature
    d2s_dt2 = np.gradient(ds_dt)
    d2x_dt2 = np.gradient(dx_dt)
    d2y_dt2 = np.gradient(dy_dt)

    curvature = (
        np.abs(d2x_dt2 * dy_dt - dx_dt * d2y_dt2)
        / (dx_dt * dx_dt + dy_dt * dy_dt) ** 1.5
    )
    t_component = np.array([d2s_dt2] * 2).transpose()
    n_component = np.array([curvature * ds_dt * ds_dt] * 2).transpose()

    acceleration = t_component * tangent + n_component * normal

    return (
        Vector(velocity),
        Vector(tangent),
        Vector(
            -unit_tangent[:, 1], unit_tangent[:, 0]
        ),  # normal as rotated tangent
        Vector(acceleration),
        curvature,
    )


def vectors_mean(*vectors: Vector):
    """
        Takes the mean of a list of vectors
    """
    return Vector(*np.mean([[v.x, v.y] for v in vectors], 0))


def smooth_vector(vec: Vector, window: int = 5) -> Vector:
    """
        Given a Vector object with a series of 2D vectors,
        it smooths the dynamics by binning the vector over time and 
        take the mean vector for each bin.
    """
    T = len(vec)
    means = []
    for t in np.arange(0, T):
        t_0 = t - window if t > window else 0
        t_1 = t + window if T - t > window else T

        means.append(vectors_mean(*[vec[i] for i in np.arange(t_0, t_1)]))

    return Vector.from_list(means)
