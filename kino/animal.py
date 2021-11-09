from __future__ import annotations

import rich.repr
from typing import Optional
from dataclasses import dataclass


@dataclass
class BodyPart:
    """
        Represents a body part with its 2D trajectory
    """

    name: str
    color: str

    def __repr__(self) -> str:
        return f'Body part: "{self.name}"'

    def __rich_repr__(self) -> rich.repr.Resul:
        yield self.name


@dataclass
class Bone:
    """
        Line segment connecting two bodyparts.
    """

    bp1: BodyPart
    bp2: BodyPart
    color: str

    def __repr__(self) -> str:
        return f"Bone: {self.bp1.name} -> {self.bp2.name}"

    def __rich_repr__(self) -> rich.repr.Resul:
        yield f"{self.bp1.name} -> {self.bp2.name}"


class Animal:
    """
        Class storing information about an animal's body parts
        and their connections.
    """

    def __init__(
        self, animal_data: dict,
    ):
        """
            Creates the animal representation.

        """
        self.build(animal_data)

    def __rich_repr__(self):
        yield f"{self.name}"
        yield f"    body parts ({self.n_bodyparts}) ", self.bodyparts
        yield f"    bones ({self.n_bones})", self.bones, True

    def __getitem__(self, item: str):
        return self.__dict__[item]

    def get_bone(self, bp1: BodyPart, bp2: BodyPart) -> Optional[Bone]:
        """
            Returns a Bone object between two bodyparts if it
            exists
        """
        bps = [bp1, bp2]
        valid_bones = [b for b in self.bones if b.bp1 in bps and b.bp2 in bps]

        return valid_bones[0] if valid_bones else None

    def build(self, animal_data: dict):
        """
            Creates the internal representation of the animal's body
        """
        self.name = animal_data["name"]
        self.paws = animal_data["paws"]

        # add bodyparts
        for bp in animal_data["bodyparts"]:
            bodypart = BodyPart(bp, animal_data["colors"][bp],)
            setattr(self, bp, bodypart)

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
