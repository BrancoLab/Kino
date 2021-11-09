from __future__ import annotations

from typing import Union, List, Optional
import copy
import sys
import matplotlib.pyplot as plt
import pandas as pd

sys.path.append("./")

from kino.draw import draw
from kino import io
from kino.geometry import Trajectory
from kino.animal.bone import Bone
from kino.animal.bodypart import BodyPart


class Animal:
    """
        Class storing information about an animal's body parts
        and their connections.
    """

    paws = [
        "left_fl",
        "right_fl",
        "right_hl",
        "left_hl",
    ]

    def __init__(
        self,
        animal_data: Union[str, Trajectory, dict],
        tracking: pd.DataFrame,
        fps: int = 1,
    ):
        """
            Creates the animal representation.

            Arguments:
                animal_data: str, Trajectory, dict. Either a dictionary
                    with entries 'bodyparts' and 'skeleton' or a
                    path to a yaml file with the same data
        """
        if isinstance(animal_data, dict):
            self.build(animal_data, tracking, fps)
        else:
            self.build(io.from_yaml(animal_data), tracking, fps)  # type: ignore

    def __rich_repr__(self):
        yield f"{self.name}"
        yield f"    body parts ({self.n_bodyparts}) ", self.bodyparts
        yield f"    bones ({self.n_bones})", self.bones

    def __getitem__(self, item: str):
        return self.__dict__[item]

    def __draw__(self, ax: plt.Axes):
        for bone in self.bones:
            draw(bone)

        for bp in self.bodyparts:
            draw(bp)

            ax.legend()

    @property
    def bodyparts(self) -> List:
        return [getattr(self, bp) for bp in self.bodyparts_names]

    def at(self, index: int) -> Animal:
        """
            Returns a copy of the the animal object + tracking
            at a specified frame
        """
        new_mouse = copy.copy(self)

        # get body parts at frame
        for bp in new_mouse.bodyparts:
            setattr(new_mouse, bp.name, bp.at(index))

        # update bones
        new_mouse.bones = [bone.at(index) for bone in self.bones]

        return new_mouse

    def get_bone(self, bp1: BodyPart, bp2: BodyPart) -> Optional[Bone]:
        """
            Returns a Bone object between two bodyparts if it
            exists
        """
        bps = [bp1, bp2]
        valid_bones = [b for b in self.bones if b.bp1 in bps and b.bp2 in bps]

        return valid_bones[0] if valid_bones else None

    def build(self, animal_data: dict, tracking: pd.DataFrame, fps: int = 1):
        """
            Creates the internal representation of the animal's body
        """
        self.name = animal_data["name"]

        # add bodyparts
        for bp in animal_data["bodyparts"]:
            bodypart = BodyPart(
                tracking[f"{bp}_x"],
                tracking[f"{bp}_y"],
                bp,
                animal_data["colors"][bp],
                fps=fps,
            )
            setattr(self, bp, bodypart)

        # store pointers to bodyparts
        self.bodyparts_names = animal_data["bodyparts"]

        # add skeleton
        self.bones = []
        for bp1, bp2, color in animal_data["skeleton"]:
            if (
                bp1 not in animal_data["bodyparts"]
                or bp2 not in animal_data["bodyparts"]
            ):
                raise ValueError(f'Bodypart "{bp1}" or "{bp2}" not found')
            self.bones.append(
                Bone(getattr(self, bp1), getattr(self, bp2), color,)
            )

        # store metadata
        self.n_bones = len(self.bones)
        self.n_bodyparts = len(self.bodyparts_names)
