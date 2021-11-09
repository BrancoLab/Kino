import pandas as pd
from typing import Union
import rich.repr
import numpy as np

from myterial import blue_grey_dark

from kino.animal import Animal
from kino.geometry import Trajectory, AnchoredTrajectory


class Locomotion:
    """
        Represents a sequence of locomotion movements 
        of an animal
    """

    def __init__(
        self, animal: Animal, tracking: Union[dict, pd.DataFrame], fps: int = 1
    ):
        self.animal = animal
        self.tracking = tracking
        self.fps = fps

        # Create a Trajectory object for each of the animal's bodyparts
        self.bodyparts = {}
        for bp in animal.bodyparts:
            bp_trajectory = Trajectory(
                tracking[f"{bp.name}_x"],
                tracking[f"{bp.name}_y"],
                name=bp.name,
                color=bp.color,
                fps=fps,
            )
            setattr(self, bp.name, bp_trajectory)
            self.bodyparts[bp.name] = bp_trajectory

        # create an AnchoredTrajectory object for each bone (2D vectors at a point)
        self.bones = {}
        for bone in animal.bones:
            bp1 = self.bodyparts[bone.bp1.name]
            bp2 = self.bodyparts[bone.bp1.name]
            bone_trajectory = AnchoredTrajectory(
                bp1.x, bp1.y, bp2.xy - bp1.xy, bone.name
            )
            self.bones[bone.name] = bone_trajectory

    def __repr__(self) -> str:
        return "Locomotion kinematics"

    def __rich_repr__(self) -> rich.repr.Result:
        yield "animal", self.animal
        yield f"bodyparts {len(self.bodyparts)}   ", self.bodyparts
        yield f"bones {len(self.bones)}  ", self.bones

    def __len__(self):
        return len(self.body)

    def compute_center_of_mass(self, *bps: str) -> Trajectory:
        """
            Averages the position of given bodyparts at each
            frame to get the center of mass between them
        """
        # get bodyparts Trajectories
        bps_trajectories = [self.bodyparts[bp] for bp in bps]

        # get average trajectory
        X = np.mean(np.vstack([bp.x for bp in bps_trajectories]), 0)
        Y = np.mean(np.vstack([bp.y for bp in bps_trajectories]), 0)

        self.com = Trajectory(
            X, Y, name="CoM", fps=self.fps, color=blue_grey_dark
        )
        self.bodyparts["com"] = self.com
        return self.com
