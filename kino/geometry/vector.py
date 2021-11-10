from __future__ import annotations

from rich import print
from rich.panel import Panel
from rich.table import Table
from rich import box
import numpy as np
from typing import Union, Tuple, List

from myterial import pink, blue

from kino.geometry import coordinates


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
        self.xy = np.vstack([self.x, self.y])

    def __repr__(self):
        if self.single_vec:
            return f"Vector @ ({self.x}, {self.y})"
        else:
            return f"Array of {len(self.x)} vectors."

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

    @classmethod
    def from_list(cls, vecs: List[Vector]) -> Vector:
        return Vector([v.x for v in vecs], [v.y for v in vecs])

    @property
    def single_vec(self):
        return isinstance(self.x, (float, int))

    @property
    def angle(self) -> np.ndarray:
        """
            Returns the angle in degrees in range (-180,180)
        """
        return np.degrees(np.arctan2(self.y, self.x))

    @property
    def angle2(self) -> np.ndarray:
        """
            Returns the angle in degrees in range(0, 360)
        """
        angle = self.angle
        if isinstance(angle, np.ndarray):
            angle[angle < 0] = 360 + angle[angle < 0]
        else:
            if angle < 0:
                angle = 360 + angle
        return angle

    @property
    def magnitude(self) -> np.ndarray:
        if self.single_vec:
            return np.sqrt(self.x ** 2 + self.y ** 2)
        else:
            # compute norm of each vector
            vec = np.vstack([self.x, self.y]).T
            return np.apply_along_axis(np.linalg.norm, 1, vec)

    def rotate(self, angle: float) -> Vector:
        """
            It rotates the vector by a given angle
        """
        R = coordinates.R(angle)

        if self.single_vec:
            xy_rot = R @ self.xy.ravel()

        else:
            xy_rot = R @ self.xy
        return Vector(xy_rot[0], xy_rot[1])

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


def print_vectors_angles_summary():
    """
        It prints a summary table with the value of Vector.angle
        and Vector.angle2 for vectors at different angles
    """
    # XY going around each quarter of the unit circle
    X = [1, 1, 0, -1, -1, -1, 0, 1, 1]
    Y = [0, 1, 1, 1, 0, -1, -1, -1, 0]
    angle = [0, 45, 90, 135, 180, 225, 270, 315, 360]

    # create column and fill in
    tb = Table(box=box.SIMPLE_HEAVY)
    tb.add_column(
        "x", header_style="bold yellow", justify="right", style="bold"
    )
    tb.add_column(
        "y", header_style="bold yellow", justify="right", style="bold"
    )
    tb.add_column("angle (-180, 180)", header_style=f"{pink}", justify="right")
    tb.add_column("angle (0, 360)", header_style=f"{blue}", justify="right")
    tb.add_column("angle manual", header_style="dim", justify="right")

    for x, y, t in zip(X, Y, angle):
        vec = Vector(x, y)

        tb.add_row(
            str(x), str(y), str(int(vec.angle)), str(int(vec.angle2)), str(t)
        )

    print(Panel.fit(tb))
