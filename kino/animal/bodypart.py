import numpy as np
from typing import Generator

from kino.geometry import Trajectory


class BodyPart(Trajectory):
    """
        Represents a body part with its 2D trajectory
    """

    def __init__(
        self, name: str, color: str, x: np.ndarray, y: np.ndarray, **kwargs
    ):
        super().__init__(x, y, name=name, **kwargs)

    def __rich_repr__(self) -> Generator:
        yield self.name
