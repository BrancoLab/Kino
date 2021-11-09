from typing import Tuple

from kino.geometry import Vector
from kino.animal.bodypart import BodyPart


class Bone:
    def __init__(
        self, bp1: BodyPart, bp2: BodyPart, color: str,
    ):
        """
            Line segment connecting two bodyparts.
        """
        self.bp1 = bp1
        self.bp2 = bp2
        self.color = color

        # compute the vector going from BP1 to BP2
        self.vector: Vector = bp2.xy - bp1.xy
        self.length = self.vector.magnitude
        self.angle = self.vector.angle

    @property
    def bodyparts(self) -> Tuple[BodyPart, BodyPart]:
        return (self.bp1, self.bp2)

    def __rich_repr__(self):
        yield f"{self.bp1.name} - {self.bp2.name}"
