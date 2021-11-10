import matplotlib.pyplot as plt
from celluloid import Camera
from typing import Union, List, Tuple, Optional
from loguru import logger
from pathlib import Path
from dataclasses import dataclass

from kino.progress import track
from kino.locomotion import Locomotion
from kino.animate.base import PoseAnimation

"""
    Complex animation with multiple view of
    a locomotion sequence
"""


@dataclass
class CompleteAnimation:
    locomotion: Locomotion
    egocentric_locomotion: Locomotion
    fps: Optional[int] = None
    bodyparts: Optional[List[str]] = None

    def _check_inputs(self):
        """
            Ensures input formats are as expected
        """
        if not self.locomotion.view == "allocentric":
            raise ValueError("First Locomotion instance should be allocentric")
        if not self.egocentric_locomotion.view == "egocentric":
            raise ValueError("Second Locomotion instance should be egocentric")
        if not len(self.locomotion) == len(self.egocentric_locomotion):
            raise ValueError(
                "The two locomotion instances should be of equal length"
            )

    def _init_figure(self) -> Tuple[plt.Figure, dict]:
        """
            Initializes an empty figure
        """
        f = plt.figure(figsize=(12, 8))
        axes = f.subplot_mosaic(
            """
                AE
            """
        )

        for ax in axes.values():
            ax.axis("equal")
            ax.set(xlabel="cm", ylabel="cm")

        return f, axes

    def on_frame_end(self, axes: dict):
        """
            Called at the end of each frame to add additional elements to the animation
            and style axes
        """
        # draw CoM
        axes["A"].plot(
            self.locomotion.com.x,
            self.locomotion.com.y,
            lw=2,
            color=self.locomotion.com,
        )

    def animate(self, save_path: Union[str, Path]):
        """
            Creates and saves the animation
        """
        if self.fps is None:
            # TODO remove this and add mypy skip bleow
            raise ValueError
        self._check_inputs()

        # create figure and camera
        f, axes = self._init_figure()
        camera = Camera(f)

        # create base animations for allocentric and egocentric views
        allocentric_anim = PoseAnimation(
            self.locomotion, self.fps, axes["A"], self.bodyparts
        )
        egocentric_anim = PoseAnimation(
            self.egocentric_locomotion, self.fps, axes["E"], self.bodyparts
        )

        # run frames
        logger.debug(
            f"Creating a Complete Animation with {allocentric_anim.n_frames_tot}"
        )
        for framen in track(
            range(allocentric_anim.n_frames_tot),
            transient=True,
            description="Creating animation",
        ):
            # plot the animal's pose
            allocentric_anim.make_next_frame()
            egocentric_anim.make_next_frame()

            # add additional elements
            self.on_frame_end(axes)

            camera.snap()

        # save
        logger.debug("   ... saving")
        animation = camera.animate(interval=1000 / self.fps)
        animation.save(save_path, fps=self.fps)
        logger.debug(f'Animation created, saved at: "{save_path}"')
