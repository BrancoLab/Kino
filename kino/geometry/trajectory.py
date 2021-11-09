from __future__ import annotations


import numpy as np
from typing import Union
import matplotlib.pyplot as plt

from myterial import blue_grey_dark

from kino.geometry import Vector
from kino.geometry import vectors_utils as vu
from kino.math import smooth, derivative, angular_derivative


class Trajectory:
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
        return len(self.x)

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
            return Vector(self.x[item], self.y[item])

        elif isinstance(item, str):
            return self.__dict__[item]

    def __draw__(self, ax: plt.Axes = None, **kwargs):
        raise NotImplementedError
        # DrawPath(
        #     self.x.coordinates,
        #     self.y.coordinates,
        #     color=self.color,
        #     ax=ax,
        #     **kwargs,
        # )

        # ax.set(
        #     xticks=[self.x.min, self.x.max],
        #     yticks=[self.y.min, self.y.max],
        #     xlabel=self.x.unit,
        #     ylabel=self.y.unit,
        # )

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
