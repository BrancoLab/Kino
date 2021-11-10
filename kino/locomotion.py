from __future__ import annotations

import pandas as pd
from typing import Union
import rich.repr
import numpy as np
from copy import copy

from myterial import blue_grey_dark

from kino.animal import Animal, Bone
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
            bone_trajectory = self._make_bone(bone)
            self.bones[bone.name] = bone_trajectory

        # create bones for head and body axis
        self.head = self._make_bone(animal.head)
        self.body_axis = self._make_bone(animal.body_axis)

        # compute paws center of mass
        self.compute_center_of_mass(*self.animal.paws)

    def __getitem__(self, item: Union[int, str]):
        """
            returns a bodypart or bone if a string is passed, otherwise the 
            locomotor state at a moment in time 
        """
        if isinstance(item, str):
            if item in self.bodyparts.keys():
                return self.bodyparts[item]
            elif item in self.bones.keys():
                return self.bones[item]
            else:
                raise AttributeError(
                    f'Locomotion does not have attribute: "{item}"'
                )
        else:
            return self @ item

    def __repr__(self) -> str:
        return "Locomotion kinematics"

    def __rich_repr__(self) -> rich.repr.Result:
        yield "animal", self.animal
        yield f"bodyparts {len(self.bodyparts)}   ", self.bodyparts
        yield f"bones {len(self.bones)}  ", self.bones

    def __len__(self):
        return len(self.body)

    def __matmul__(self, other: Union[int, np.ndarray]) -> Locomotion:
        """
            Ovveriding @ operator to index the locomotor state at a frame
            (or set of frames)
        """
        new_locomotion = copy(self)
        new_locomotion.bodyparts = {
            name: bp @ other for name, bp in new_locomotion.bodyparts.items()
        }
        new_locomotion.bones = {
            name: bone @ other for name, bone in new_locomotion.bones.items()
        }
        new_locomotion.head = new_locomotion.head @ other
        new_locomotion.body_axis = new_locomotion.body_axis @ other
        return new_locomotion

    def _make_bone(self, bone: Bone) -> AnchoredTrajectory:
        """
            Given a Bone specified by two bodyparts, creates a 
            anchored set of vectors at bone.bp1 pointing at bone.bp2
        """
        bp1 = self.bodyparts[bone.bp1.name]
        bp2 = self.bodyparts[bone.bp2.name]
        return AnchoredTrajectory(
            bp1.x,
            bp1.y,
            vector=bp2.xy - bp1.xy,
            name=bone.name,
            color=bone.color,
        )

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
