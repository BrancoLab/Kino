from __future__ import annotations

from copy import copy
import numpy as np
from typing import Generator
import matplotlib.pyplot as plt

from kino.geometry import Trajectory


class BodyPart(Trajectory):
    """
        Represents a body part with its 2D trajectory
    """

    def __init__(
        self, x: np.ndarray, y: np.ndarray, name: str, color: str, **kwargs
    ):
        super().__init__(x, y, name=name, color=color, **kwargs)

    def __repr__(self) -> str:
        return f'Body part: "{self.name}"'

    def __rich_repr__(self) -> Generator:
        yield self.name

    def at(self, index: int) -> BodyPart:
        """
            Returns a copy of the bodypart with the tracking
            at a frame
        """
        newbp = copy(self)
        newbp.x = self.x[index]
        newbp.y = self.y[index]

        return newbp

    def set_trajectory(
        self, x: np.ndarray, y: np.ndarray, fps: int = 1
    ) -> None:
        """
            Sets the XY trajectory for the body part tracking
        """
        self.fps = fps
        self.x, self.y = x, y

        self.compute_kinematics()

    def __draw__(
        self,
        ax: plt.Axes,
        show_vectors: bool = False,
        vectors_scale: float = 0.25,
        **kwargs,
    ):
        if len(self) > 1:
            ax.plot(
                self.x,
                self.y,
                lw=1,
                color=self.color,
                zorder=-1,
                label=self.name,
            )
            ax.scatter(
                self.x[:: self.fps],
                self.y[:: self.fps],
                s=50,
                ec="k",
                lw=0.5,
                zorder=100,
                color=self.color,
            )
        else:
            ax.scatter(
                self.x,
                self.y,
                s=50,
                ec="k",
                lw=0.5,
                zorder=100,
                color=self.color,
            )
