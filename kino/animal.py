from __future__ import annotations

import rich.repr
from typing import Optional
from dataclasses import dataclass

from myterial import (
    pink,
    pink_darker,
    blue,
    blue_darker,
    blue_grey_light,
    blue_grey_dark,
    blue_grey_darker,
    salmon,
)


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
    name: str

    def __repr__(self) -> str:
        return f"Bone: '{self.bp1.name} -> {self.bp2.name}''"

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

    def __repr__(self) -> str:
        return f"""
{self.name}
body parts ({self.n_bodyparts}) = {self.bodyparts}
bones ({self.n_bones}) = {self.bones}
            """

    def __rich_repr__(self) -> rich.repr.Resul:
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

            bp1, bp2 = (
                getattr(self, bp1),
                getattr(self, bp2),
            )  # get BodyPart from name
            self.bones.append(
                Bone(bp1, bp2, color, name=f"{bp1.name}_{bp2.name}")
            )

        # add body and head 'bones'
        self.body_axis = Bone(
            self[animal_data["body_axis"][0]],
            self[animal_data["body_axis"][1]],
            color=blue_grey_darker,
            name="body_axis",
        )
        self.head = Bone(
            self[animal_data["head"][0]],
            self[animal_data["head"][1]],
            color=salmon,
            name="head",
        )

        # store metadata
        self.n_bones = len(self.bones)
        self.n_bodyparts = len(self.bodyparts_names)


"""
    Default animal with fixed skeleton
"""

default_animal_data = dict(
    name="Mouse",
    paws=("left_fl", "right_fl", "right_hl", "left_hl"),
    body_axis=("tail_base", "neck"),
    head=("neck", "snout"),
    bodyparts=(
        "left_fl",
        "right_fl",
        "body",
        "right_hl",
        "left_hl",
        "snout",
        "neck",
        "tail_base",
    ),
    colors=dict(
        left_fl=pink,
        right_fl=blue,
        right_hl=blue_darker,
        left_hl=pink_darker,
        snout=blue_grey_light,
        neck=blue_grey_light,
        body=blue_grey_dark,
        tail_base=blue_grey_darker,
    ),
    skeleton=(
        ("body", "left_fl", blue_darker),
        ("body", "right_fl", blue_darker),
        ("body", "right_hl", blue_darker),
        ("body", "left_hl", blue_darker),
        ("snout", "neck", "k"),
        ("neck", "body", "k"),
        ("body", "tail_base", "k"),
    ),
)

mouse = Animal(default_animal_data)

if __name__ == "__main__":
    print(mouse)
