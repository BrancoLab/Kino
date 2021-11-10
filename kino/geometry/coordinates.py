import numpy as np
from typing import Tuple


def R(theta: float) -> np.ndarray:
    """
        Returns the rotation matrix for rotating an object
        centered around the origin with a given angle

        Arguments:
            theta: angle in degrees

        Returns:
            R: 2x2 np.ndarray with rotation matrix
    """
    theta = np.radians(theta)
    return np.array(
        [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]
    )


def cart2pol(x: float, y: float) -> Tuple[float, float]:
    """
        Cartesian to polar coordinates

        angles in degrees
    """
    rho = np.hypot(x, y)
    phi = np.degrees(np.arctan2(y, x))
    return rho, phi


def pol2cart(rho: float, phi: float) -> Tuple[float, float]:
    """
        Polar to cartesian coordinates

        angles in degrees
    """
    x = rho * np.cos(np.radians(phi))
    y = rho * np.sin(np.radians(phi))
    return x, y
