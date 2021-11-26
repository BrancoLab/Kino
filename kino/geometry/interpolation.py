from typing import Union
from copy import copy

from kino.locomotion import Locomotion

import kino.geometry as kg

# import kg.Vector, kg.Trajectory, kg.AnchoredTrajectory


def lerp(x0: float, x1: float, p: float) -> float:
    """
        Interplates linearly between two values such that when p=0
        the interpolated value is x0 and at p=1 it's x1
    """
    return (1 - p) * x0 + p * x1


def interpolate_vectors(v0: kg.Vector, v1: kg.Vector, p: float) -> kg.Vector:
    """
        Interpolates two 2D vectors
    """
    return kg.Vector(lerp(v0.x, v1.x, p), lerp(v0.y, v1.y, p))


def interpolate_vector_at_frame(
    vector: kg.Vector, frame: int, p: float
) -> kg.Vector:
    """
        Interpolates a 2D vector between two following frames
    """
    v0 = vector[frame]
    v1 = vector[frame + 1]

    return interpolate_vectors(v0, v1, p)


def interpolate_trajectory_at_frame(
    trajectory: kg.Trajectory, frame: int, p: float
) -> kg.Trajectory:
    """
        Interpolate a trajectory at a frame
    """
    # get trajectory snapshots
    t0 = trajectory @ frame
    t1 = trajectory @ (frame + 1)

    # create new trajectory object
    newT = kg.Trajectory(
        lerp(t0.x, t1.x, p),
        lerp(t0.y, t1.y, p),
        fps=trajectory.fps,
        name=trajectory.name,
        compute_kinematics=False,
        color=trajectory.color,
    )

    # interpolate variables (vector and scalar variables)
    newT.velocity = interpolate_vectors(t0.velocity, t1.velocity, p)
    newT.tangent = interpolate_vectors(t0.tangent, t1.tangent, p)
    newT.normal = interpolate_vectors(t0.normal, t1.normal, p)
    newT.acceleration = interpolate_vectors(
        t0.acceleration, t1.acceleration, p
    )
    newT.speed = lerp(t0.speed, t1.speed, p)
    newT.curvature = lerp(t0.curvature, t1.curvature, p)
    newT.acceleration_mag = lerp(t0.acceleration_mag, t1.acceleration_mag, p)
    newT.theta = lerp(t0.theta, t1.theta, p)
    newT.thetadot = lerp(t0.thetadot, t1.thetadot, p)
    newT.thetadotdot = lerp(t0.thetadotdot, t1.thetadotdot, p)

    return newT


def interpolate_anchored_trajectory_at_frame(
    trajectory: kg.AnchoredTrajectory, frame: int, p: float
) -> kg.AnchoredTrajectory:
    """
        Interpolates an kg.AnchoredTrajectory object at a frame
    """
    # get snapshots
    t0 = trajectory @ frame
    t1 = trajectory @ (frame + 1)

    # create new interpolated
    return kg.AnchoredTrajectory(
        x=lerp(t0.x, t1.x, p),
        y=lerp(t0.y, t1.y, p),
        vector=interpolate_vectors(t0.vector, t1.vector, p),
        color=trajectory.color,
        name=trajectory.name,
    )


def interpolate_locomotion_at_frame(
    locomotion: Locomotion, frame: int, p: float
) -> Locomotion:
    """
        Interpolates a locomotion object at a frame
    """
    new_locomotion = copy(locomotion)
    new_locomotion.bodyparts = {
        name: interpolate_trajectory_at_frame(bp, frame, p)
        for name, bp in new_locomotion.bodyparts.items()
    }
    new_locomotion.bones = {
        name: interpolate_anchored_trajectory_at_frame(bone, frame, p)
        for name, bone in new_locomotion.bones.items()
    }
    new_locomotion.head = interpolate_anchored_trajectory_at_frame(
        new_locomotion.head, frame, p
    )
    new_locomotion.body_axis = interpolate_anchored_trajectory_at_frame(
        new_locomotion.body_axis, frame, p
    )
    return new_locomotion


def interpolate_at_frame(
    obj: Union[kg.Vector, kg.Trajectory, kg.AnchoredTrajectory, Locomotion],
    frame: int,
    p: float,
):
    """
        Generic interpolation function for different geometric objects
    """
    if isinstance(obj, kg.Vector):
        return interpolate_vector_at_frame(obj, frame, p)
    elif isinstance(obj, kg.Trajectory):
        return interpolate_trajectory_at_frame(obj, frame, p)
    elif isinstance(obj, kg.AnchoredTrajectory):
        return interpolate_anchored_trajectory_at_frame(obj, frame, p)
    elif isinstance(obj, Locomotion):
        return interpolate_locomotion_at_frame(obj, frame, p)
