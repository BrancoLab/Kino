import matplotlib.pyplot as plt
from celluloid import Camera
from typing import Union, List
from rich.progress import track
from loguru import logger
from pathlib import Path
import numpy as np

from kino.locomotion import Locomotion
from kino.draw import DrawAnimal


class BaseAnimation:
    """
        Base class to animate a Locomotion trajectory
        (either egocentric or base reference frames)
    """

    def __init__(
        self,
        locomotion: Locomotion,
        fps: int = None,
        ax: plt.Axes = None,
        bodyparts: List[str] = None,
    ):
        self.locomotion = locomotion
        self.fps = fps or locomotion.fps
        self.bps_to_draw = bodyparts or list(self.locomotion.bodyparts.keys())
        self.ax = ax or plt.gca()

        # initialize camera
        self.frame_idx = 0
        self.interpolation_idx = 0

        # compute the number of interpolated frames
        self.n_interpolated = int(locomotion.fps / self.fps)
        if self.n_interpolated < 1:
            raise ValueError(
                f"Cannot generate animation at {self.fps} fps given locomotion fps of: {locomotion.fps}"
            )
        self.P = (
            np.linspace(0, 1, self.n_interpolated)
            if self.n_interpolated > 1
            else [1]
        )

    def make_next_frame(self) -> bool:
        if (
            self.frame_idx >= len(self.locomotion) - 2
        ):  # -2 because of interpolation
            return False

        # reset interpolation index
        if self.interpolation_idx >= len(self.P):
            self.interpolation_idx = 0
            self.frame_idx += 1

        # get interpolation factor
        p = self.P[self.interpolation_idx]

        # draw the interpolated position of the animal
        DrawAnimal.at_frame_interpolated(
            self.locomotion.animal, self.locomotion, self.frame_idx, p, self.ax
        )

        self.interpolation_idx += 1
        return True

    def animate(self, save_path: Union[str, Path]):
        # initialize camera
        camera = Camera(self.ax.figure)

        # run
        L = int(len(self.locomotion) * len(self.P))
        logger.debug(f"Creating animation with {L} frames | fps: {self.fps}")
        for framen in track(
            range(L), transient=True, description="Creating animation"
        ):
            running = self.make_next_frame()
            camera.snap()
            if not running:
                break

        # save
        logger.debug("   ... saving")
        animation = camera.animate(interval=1000 / self.fps)
        animation.save(save_path, fps=self.fps)
        logger.debug(f'Animation created, saved at: "{save_path}"')
