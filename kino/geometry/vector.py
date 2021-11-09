from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from typing import Union, Tuple, List

from kino.draw.gliphs import Arrow, Arrows


class Vector:  # 2D vector
    """
        Vector.

        Class representing a 2D vector (specified by a tuple of coordinates (x,y)) or
        a list of 2D vectors (specified by (x_0, x_1, ..., x_T), (y_0, y_1, ..., y_T)).
        When representing a list of vectors, this is assumed to present a vector quantity
        (e.g. velocity vector) over a sequence of time steps.
        When representing a list of vectors, operations like vector subtraction are done 
        between two equally long sequences and elementwise for each time step.
    """

    def __init__(
        self, x: Union[np.ndarray, float], y: Union[np.ndarray, float] = None,
    ):
        if y is None and isinstance(x, np.ndarray):
            y, x = x[:, 1], x[:, 0]

        self.x = np.array(x) if not isinstance(x, (float, int)) else x
        self.y = np.array(y) if not isinstance(y, (float, int)) else y

    def __repr__(self):
        if self.single_vec:
            return f"Vector @ ({self.x}, {self.y})"
        else:
            return f"Array of {len(self.x)} vectors."

    def __draw__(self, ax: plt.Axes, **kwargs):
        """
            Draws the vector staring from origin
        """
        if self.single_vec:
            Arrow(0, 0, self.angle, self.magnitude, ax=ax, **kwargs)
        else:
            Arrows(
                np.zeros(len(self)),
                np.zeros(len(self)),
                self.angle,
                self.magnitude,
                ax=ax,
                step=5,
                **kwargs,
            )

    def __len__(self):
        if not self.single_vec:
            return len(self.x)
        else:
            return 1

    def __getitem__(self, item: Union[int, str, slice]) -> Vector:
        if isinstance(item, str):
            return self.__dict__[item]
        else:
            if self.single_vec:
                raise IndexError("Cannot index vector")
            else:
                return Vector(self.x[item], self.y[item])

    def __sub__(self, other: Vector):
        return Vector(self.x - other.x, self.y - other.y)

    def to_polar(self) -> Tuple[np.ndarray, np.ndarray]:
        rho = np.hypot(self.x, self.y)
        phi = np.degrees(np.arctan2(self.y, self.x))
        return rho, phi

    def to_unit_vector(self) -> Vector:
        x = self.x / self.magnitude
        y = self.y / self.magnitude
        return Vector(x, y)

    def as_array(self) -> np.ndarray:
        if self.single_vec:
            return np.array([self.x, self.y])
        else:
            return np.vstack([self.x, self.y]).T

    @classmethod
    def from_list(cls, vecs: List[Vector]) -> Vector:
        return Vector([v.x for v in vecs], [v.y for v in vecs])

    @property
    def single_vec(self):
        return isinstance(self.x, (float, int))

    @property
    def angle(self) -> np.ndarray:
        return np.degrees(np.arctan2(self.y, self.x))

    @property
    def magnitude(self) -> np.ndarray:
        if self.single_vec:
            return np.sqrt(self.x ** 2 + self.y ** 2)
        else:
            # compute norm of each vector
            vec = np.vstack([self.x, self.y]).T
            return np.apply_along_axis(np.linalg.norm, 1, vec)

    def dot(
        self, other: Vector, norm: bool = True
    ) -> Union[float, np.ndarray]:
        if len(self) != len(other):
            raise ValueError("only vectors of same length can be dotted")

        # compute dot product
        if self.single_vec:
            _dot = np.dot([self.x, self.y], [other.x, other.y])
        else:
            _dot = np.array(
                [
                    np.dot([self.x[i], self.y[i]], [other.x[i], other.y[i]])
                    for i in range(len(self))
                ]
            )

        # return normalize dot
        if norm:
            return _dot / other.magnitude
        else:
            return _dot

    def angle_with(self, other: Vector) -> Union[float, np.ndarray]:
        """
            Computes the angle between two vectors.
        """
        if self.single_vec != other.single_vec:
            raise NotImplementedError(
                "This doesnt work yet, need some sort of broadcasting"
            )

        _self = self.to_unit_vector().as_array()
        _other = other.to_unit_vector().as_array()

        if self.single_vec:
            return np.degrees(
                np.arccos(np.clip(np.dot(_self, _other), -1.0, 1.0))
            )
        else:
            return np.degrees(
                [
                    np.arccos(
                        np.clip(np.dot(_self[i, :], _other[i, :]), -1.0, 1.0)
                    )
                    for i in range(len(self))
                ]
            )
