from __future__ import annotations

import sys

sys.path.append("./")

import numpy as np
from typing import Union
from dataclasses import dataclass

from myterial import blue_grey_dark

import kino.geometry as kg
from kino.geometry import Vector
from kino.geometry import vectors_utils as vu
from kino.math import (
    smooth,
    derivative,
    angular_derivative,
    resample_linear_1d,
)


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

    def __len__(self) -> int:
        try:
            return len(self.x)
        except TypeError:
            return 1

    def __repr__(self):
        return f'Trajectory: "{self.name}" | {self.distance:.2f}cm, {len(self)} data points'

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

    def __matmul__(self, other: Union[int, np.ndarray]) -> Trajectory:
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
        new_traj.acceleration_mag = self.acceleration_mag[other]  # type: ignore
        new_traj.theta = self.theta[other]
        new_traj.thetadot = self.thetadot[other]
        new_traj.thetadotdot = self.thetadotdot[other]

        return new_traj

    @property
    def longitudinal_acceleration(self):
        """
            Returns the projection of the acceleration
            vector onto the tangential direction
        """
        return smooth(self.acceleration.dot(self.tangent))

    @property
    def normal_acceleration(self):
        """
            Returns the projection of the acceleration
            vector onto the normal direction
        """
        return smooth(self.acceleration.dot(self.normal))

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

    @property
    def duration(self) -> float:
        return self.time[-1]

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
        if window > 1:
            self.velocity = vu.smooth_vector(self.velocity, window)
            self.acceleration = vu.smooth_vector(self.acceleration, window)
            self.tangent = vu.smooth_vector(self.tangent, window)
            self.normal = vu.smooth_vector(self.normal, window)
            self.curvature = smooth(self.curvature, window)

        self.speed = self.velocity.magnitude
        self.acceleration_mag = self.acceleration.dot(self.tangent)

        # compute tangential angle and angular velocity
        self.theta = 180 - self.tangent.angle
        self.thetadot = angular_derivative(self.theta) * self.fps
        self.thetadot[:3] = self.thetadot[4]
        self.thetadotdot = derivative(self.thetadot)

        # compute distance travelled
        self.distance = np.sum(self.speed) / self.fps
        self.comulative_distance = np.cumsum(self.speed) / self.fps

    def interpolate(self, spacing: float = 1) -> Trajectory:
        """
            Interpolates the current path to produce 
            a new path with points 'spacing' apart
        """
        generated: dict = dict(x=[], y=[])
        for n in range(len(self) - 1):
            # get current and next point
            p0 = self[n]
            p1 = self[n + 1]

            # get number of new points
            segment = p1 - p0
            if segment.magnitude <= spacing:
                if n > 0:
                    prev = Vector(generated["x"][-1], generated["y"][-1])
                    if (prev - p0).magnitude >= spacing:
                        generated["x"].append(p0.x)
                        generated["y"].append(p0.y)
                    else:
                        continue
                else:
                    generated["x"].append(p0.x)
                    generated["y"].append(p0.y)
            else:
                n_new = int(np.floor(segment.magnitude / spacing))

                # create new points
                for p in np.linspace(0, 1, n_new):
                    if n > 0 and p == 0:
                        continue  # avoid doubling
                    generated["x"].append(kg.interpolation.lerp(p0.x, p1.x, p))  # type: ignore
                    generated["y"].append(kg.interpolation.lerp(p0.y, p1.y, p))  # type: ignore
        return Trajectory(generated["x"], generated["y"])

    def downsample(self, spacing: float = 1) -> Trajectory:
        """
            Downsamples the path keeping only points that are spacing apart.
            It downsamples the path by selecting points that are spaced
            along the path: the spacing reflects the path-length between two
            points along the original path, even though they might be very close in 
            euclidean terms.
        """
        downsampled: dict = dict(x=[], y=[])
        for n in range(len(self)):
            if n == 0:
                downsampled["x"].append(self[0].x)
                downsampled["y"].append(self[0].y)
                last_distance = 0
            else:
                # get path distance until current point
                curr_distance = np.sum(self.speed[:n]) / self.fps

                if curr_distance - last_distance > spacing:
                    downsampled["x"].append(self[n].x)
                    downsampled["y"].append(self[n].y)
                    last_distance = curr_distance
        return Trajectory(downsampled["x"], downsampled["y"])

    def downsample_euclidean(self, spacing: float = 1) -> Trajectory:
        """
            Downsamples the path keeping only points that are spacing apart.
            This function looks at the euclidean distance between points, 
            ignores the path length distance between them
        """
        downsampled: dict = dict(x=[], y=[])
        for n in range(len(self)):
            if n == 0:
                downsampled["x"].append(self[0].x)
                downsampled["y"].append(self[0].y)
            else:
                p0 = Vector(downsampled["x"][-1], downsampled["y"][-1])
                p1 = self[n]

                # if distance > spacing
                if (p1 - p0).magnitude >= spacing:
                    # the distance between the two could be > spacing
                    # get a new point at the right distance
                    vec = p1 - p0
                    downsampled["x"].append(
                        p0.x + spacing * np.cos(np.radians(vec.angle))
                    )
                    downsampled["y"].append(
                        p0.y + spacing * np.sin(np.radians(vec.angle))
                    )
        return Trajectory(downsampled["x"], downsampled["y"])

    def downsample_in_time(self, n_timesteps: int) -> Trajectory:
        """
            It downsamples the X,Y trajectories to have a target number of
            samples
        """
        return Trajectory(
            resample_linear_1d(self.x, n_timesteps),
            resample_linear_1d(self.y, n_timesteps),
        )


@dataclass
class AnchoredTrajectory:
    """
        Represents a sequence of 2D vectors at a sequence of points (XY).
    """

    x: np.ndarray  # or floats
    y: np.ndarray  # or floats
    vector: Vector
    color: str
    name: str

    def __len__(self) -> int:
        return len(self.x)

    def __repr__(self) -> str:
        return f"AnchoredTrajectory: {self.name} | {len(self)} points"

    def __matmul__(self, other: Union[int, np.ndarray]) -> AnchoredTrajectory:
        return AnchoredTrajectory(
            self.x[other],
            self.y[other],
            self.vector[other],
            self.color,
            self.name,
        )

    @property
    def theta(self):
        return self.vector.angle2

    @property
    def thetadot(self):
        val = smooth(angular_derivative(self.theta))
        val[:2] = val[3]
        return val

    @property
    def thetadotdot(self):
        val = smooth(derivative(self.thetadot))
        val[:2] = val[3]
        return val
