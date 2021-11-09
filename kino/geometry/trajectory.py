from __future__ import annotations

import sys

sys.path.append("./")

import numpy as np
from typing import Union
import matplotlib.pyplot as plt

from myterial import blue_grey_dark

from kino.geometry import Vector
from kino.geometry import vectors_utils as vu
from kino.math import smooth, derivative, angular_derivative
from kino.draw import colors, gliphs


class Trajectory:
    """
        Class representing a 2D trajectory specified by a set of XY coordinates.
        Computes kinematics variables on the trajectory (e.g. velocity vector)
    """

    def __init__(
        self,
        x: np.ndarray,
        y: np.ndarray,
        name: str = "trajectory",
        fps: int = 1,
        smoothing_window: int = 5,
        compute_kinematics: bool = True,
        color: str = blue_grey_dark,
    ):

        self.x = np.array(x)
        self.y = np.array(y)
        self.xy = Vector(self.x, self.y)
        self.fps = fps
        self.name = name
        self.color = color

        if compute_kinematics:
            self.compute_kinematics(smoothing_window)

    def __len__(self):
        return len(self.x) if isinstance(self.x, np.ndarray) else 1

    def __rich_repr__(self):
        yield "Name: ", self.name
        yield "\n   n frames: ", len(self)
        yield f"\n   duration (seconds)", round(self.time[-1], 2)
        yield "\n   path length (cm) ", round(self.distance, 2)

    def __getitem__(self, item: Union[str, int]) -> Union[Vector, np.ndarray]:
        """
            If an integer index is used, it returns
            the XY coordinates at the corresponding frame,
            otherise for string item the corrisponding attribute is returned
        """
        if isinstance(item, int):
            if isinstance(self.x, np.ndarray):
                return self.xy[item]
            else:
                return self.xy
        elif isinstance(item, str):
            return self.__dict__[item]

    def __draw__(
        self,
        ax: plt.Axes,
        show_vectors: bool = False,
        vectors_scale: float = 0.25,
        **kwargs,
    ):
        # draw main tracking line
        ax.plot(
            self.x, self.y, color=self.color, **kwargs,
        )

        # draw kinematics
        if show_vectors:
            gliphs.Arrows(
                self.x,
                self.y,
                self.velocity.angle,
                L=vectors_scale,
                color=colors.velocity,
                step=self.fps,
            )
            gliphs.Arrows(
                self.x,
                self.y,
                self.acceleration.angle,
                L=vectors_scale,
                color=colors.acceleration,
                step=self.fps,
            )
            gliphs.Arrows(
                self.x,
                self.y,
                self.normal.angle,
                L=vectors_scale,
                color=colors.normal,
                step=self.fps,
            )

        ax.set(
            xticks=[round(self.x.min(), 2), round(self.x.max(), 2)],
            yticks=[round(self.y.min(), 2), round(self.y.max(), 2)],
            xlabel="cm",
            ylabel="cm",
        )

    def __matmul__(self, other: np.ndarray) -> Trajectory:
        """
            Override @ operator to filter path at timestamps
            (e.g. at given timepoints)
        """
        new_traj = Trajectory(
            self.x[other],
            self.y[other],
            fps=self.fps,
            name=self.name,
            compute_kinematics=False,
            color=self.color,
        )

        new_traj.velocity = self.velocity[other]
        new_traj.tangent = self.tangent[other]
        new_traj.normal = self.normal[other]
        new_traj.acceleration = self.acceleration[other]
        new_traj.speed = self.speed[other]
        new_traj.curvature = self.curvature[other]
        new_traj.acceleration_mag = self.acceleration_mag[other]
        new_traj.theta = self.theta[other]
        new_traj.thetadot = self.thetadot[other]
        new_traj.thetadotdot = self.thetadotdot[other]

        return new_traj

    @property
    def frames(self) -> np.ndarray:
        """
            Array with frame index
        """
        if isinstance(self.x, (int, float)):
            return np.array([0])
        else:
            return np.arange(len(self.x))

    @property
    def time(self) -> np.ndarray:
        """
            Array with time for each frame, in seconds
        """
        return self.frames / self.fps

    def trim(self, start: int, end: int) -> Trajectory:
        """
            Cuts kinematics variables between two time frames
        """
        return self @ np.arange(start, end)

    def compute_kinematics(self, window: int = 5):
        """
            Computes kinematic quantities like
            speed, velocity, acceleration...
        """
        # smooth XY trajectory
        if window:
            self.x = smooth(self.x, window)
            self.y = smooth(self.y, window)
            self.xy = Vector(self.x, self.y)

        # compute kinematics vectors / scalar quantities
        (
            self.velocity,
            self.tangent,
            self.normal,
            self.acceleration,
            self.speed,
            self.curvature,
        ) = vu.compute_vectors_from_coordinates(self.x, self.y, fps=self.fps)

        # smooth kinematics
        if window:
            self.velocity = vu.smooth_vector(self.velocity, window)
            self.acceleration = vu.smooth_vector(self.acceleration, window)
            self.tangent = vu.smooth_vector(self.tangent, window)
            self.normal = vu.smooth_vector(self.normal, window)
            self.curvature = smooth(self.curvature, window)

        self.speed = self.velocity.magnitude
        self.acceleration_mag = self.acceleration.magnitude

        # compute tangential angle and angular velocity
        self.theta = 180 - self.tangent.angle
        self.thetadot = angular_derivative(self.theta) * self.fps
        self.thetadotdot = derivative(self.thetadot)

        # compute distance travelled
        self.distance = np.sum(self.speed) / self.fps
        self.comulative_distance = np.cumsum(self.speed) / self.fps


if __name__ == "__main__":
    x = np.linspace(0, np.pi * 2, 300)
    y = np.cos(x)

    path = Trajectory(x, y, fps=50)

    from kino.draw import draw

    draw(path, lw=3)

    plt.show()
