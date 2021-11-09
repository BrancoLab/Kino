from __future__ import annotations

from typing import Union, Tuple
import numpy as np
import copy
from dataclasses import dataclass
import sys

sys.path.append("./")

from kino import io
from kino.geometry import Trajectory


@dataclass
class BodyPart:
    name: str
    color: str

    has_tracking: bool = False

    def __repr__(self) -> str:
        return self.name

    def add_tracking(self, x: np.ndarray, y: np.ndarray):
        self.has_tracking = True
        self.tracking = Trajectory(x, y, name=self.name, color=self.color)


@dataclass
class Bone:
    bp1: BodyPart
    bp2: BodyPart
    color: str

    @property
    def bodyparts(self) -> Tuple[BodyPart, BodyPart]:
        return (self.bp1, self.bp2)

    def __rich_repr__(self):
        yield f"{self.bp1.name} - {self.bp2.name}"


class Animal:
    """
        Class storing information about an animal's body parts
        and their connections.
    """

    def __init__(self, animal_data: Union[str, Trajectory, dict]):
        """
            Creates the animal representation.

            Arguments:
                animal_data: str, Trajectory, dict. Either a dictionary
                    with entries 'bodyparts' and 'skeleton' or a
                    path to a yaml file with the same data
        """
        if isinstance(animal_data, dict):
            self.build(animal_data)
        else:
            self.build(io.from_yaml(animal_data))  # type: ignore

    def __repr__(self) -> str:
        return f"Animal - {self.name}"

    def __rich_repr__(self):
        yield f"{self.name}"
        yield f"\n    bodyparts ({self.n_bodyparts}) ", self.bodyparts_names
        yield f"\n    bones ({self.n_bones})", self.bones

    def __getitem__(self, item: str):
        return self.__dict__[item]

    @property
    def has_tracking(self):
        return self.bodyparts[0].has_tracking

    def at(self, index: int) -> Animal:
        """
            Returns a copy of the the animal object + tracking
            at a specified frame
        """
        new_mouse = copy.copy(self)
        if not self.has_tracking:
            return new_mouse

        for bp in new_mouse.bodyparts_names:
            new_mouse[bp].tracking[index]
        return new_mouse

    def get_bone(self, bp1: BodyPart, bp2: BodyPart) -> Bone:
        """
            Returns a Bone object between two bodyparts if it
            exists
        """
        bps = [bp1, bp2]
        valid_bones = [b for b in self.bones if b.bp1 in bps and b.bp2 in bps]

        if not valid_bones or len(valid_bones) > 1:
            raise ValueError(
                f"Error searching bone with bodyparts: {bps}: zero or too many results"
            )
        return valid_bones[0]

    def build(self, animal_data: dict):
        """
            Creates the internal representation of the animal's body
        """
        self.name = animal_data["name"]

        # add bodyparts
        for bp in animal_data["bodyparts"]:
            setattr(self, bp, BodyPart(bp, animal_data["colors"][bp]))

        # store pointers to bodyparts
        self.bodyparts_names = animal_data["bodyparts"]
        self.bodyparts = [getattr(self, bp) for bp in self.bodyparts_names]

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


# TODO add tracking for each bodyparts
# TODO add method to draw
# TODO specify center bodyparts
# TODO add method to get coordinates in egocentric coordinates
# TODO draw in egocentric coordinates

if __name__ == "__main__":
    animal_data = dict(
        name="Mouse",
        bodyparts=("snout", "neck", "body", "tail_base"),
        skeleton=(("snout", "neck"), ("neck", "body"), ("body", "tail_base"),),
    )

    animal = Animal(animal_data)

    from rich import print

    print(animal)
