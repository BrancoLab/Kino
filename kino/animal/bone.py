from __future__ import annotations

from copy import copy
from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np

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

        self.name = f"{self.bp1.name} -> {self.bp2.name}"

    def __rich_repr__(self):
        yield self.name

    def __draw__(self, ax: plt.Axes):
        if len(self.bp1) > 1:
            for frame in self.bp1.frames:
                if not frame % self.bp1.fps == 0:
                    continue
                ax.plot(
                    [self.bp1.x[frame], self.bp2.x[frame]],
                    [self.bp1.y[frame], self.bp2.y[frame]],
                    lw=2,
                    color=self.color,
                    zorder=0,
                )
        else:
            ax.plot(
                [self.bp1.x, self.bp2.x],
                [self.bp1.y, self.bp2.y],
                lw=2,
                color=self.color,
                zorder=0,
            )

    @property
    def bodyparts(self) -> Tuple[BodyPart, BodyPart]:
        return (self.bp1, self.bp2)

    @property
    def vector(self) -> Vector:
        return self.bp2.xy - self.bp1.xy

    @property
    def length(self) -> np.ndarray:
        return self.vector.magnitude

    @property
    def angle(self) -> np.ndarray:
        return self.vector.angle

    def at(self, index: int) -> Bone:
        """
            returns the position of the bone at a given moment in time
        """
        new_bone = copy(self)
        new_bone.bp1 = new_bone.bp1.at(index)
        new_bone.bp2 = new_bone.bp2.at(index)

        return new_bone
