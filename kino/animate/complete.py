import matplotlib.pyplot as plt
from typing import List, Tuple, Optional

from kino.locomotion import Locomotion
from kino.animate.base import (
    PoseAnimation,
    AnimationCore,
    VectorAnimation,
    ScalarAnimation,
)
from kino.draw import colors

"""
    Complex animation with multiple view of
    a locomotion sequence
"""


class CompleteAnimation(AnimationCore):
    def __init__(
        self,
        locomotion: Locomotion,
        egocentric_locomotion: Locomotion,
        fps: int = 1,
        bodyparts: Optional[List[str]] = None,
    ):
        super().__init__(locomotion.fps, fps, len(locomotion))
        self.locomotion = locomotion
        self.egocentric_locomotion = egocentric_locomotion
        self.bodyparts = bodyparts

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
                AAEE
                AAEE
                SSTT
            """
        )

        for ax in "AE":
            axes[ax].axis("equal")
            axes[ax].set(xlabel="cm", ylabel="cm")

        return f, axes

    def on_animation_start(self):
        # check inputs format
        self._check_inputs()

        # crate figure
        self.figure, self.axes = self._init_figure()

        # create base animation elements - pose
        allocentric_anim = PoseAnimation(
            self.locomotion, self.fps, self.axes["A"], self.bodyparts
        )
        egocentric_anim = PoseAnimation(
            self.egocentric_locomotion,
            self.fps,
            self.axes["E"],
            self.bodyparts,
        )

        # create vectors animation elements
        allo_velocity_anim = VectorAnimation(
            self.locomotion.com.velocity,
            self.locomotion.com,
            vector_length=2,
            data_fps=self.locomotion.fps,
            animation_fps=self.fps,
            ax=self.axes["A"],
            plot_kwargs=dict(color=colors.velocity, width=4,),
        )

        allo_accel_anim = VectorAnimation(
            self.locomotion.com.acceleration,
            self.locomotion.com,
            vector_length=1,
            data_fps=self.locomotion.fps,
            animation_fps=self.fps,
            ax=self.axes["A"],
            plot_kwargs=dict(color=colors.acceleration, width=4,),
        )

        # create scalars animation elements
        speed_anim = ScalarAnimation(
            self.locomotion.com.speed,
            self.locomotion.fps,
            self.fps,
            self.axes["S"],
            plot_kwargs=dict(color=colors.velocity, lw=2),
            time_range=1,
        )

        avel_anim = ScalarAnimation(
            self.locomotion.com.thetadot,
            self.locomotion.fps,
            self.fps,
            self.axes["T"],
            plot_kwargs=dict(color=colors.thetadot, lw=2),
            time_range=1,
        )

        # keep track of all animators
        self.animators = [
            allocentric_anim,
            egocentric_anim,
            allo_velocity_anim,
            allo_accel_anim,
            speed_anim,
            avel_anim,
        ]

    def make_next_frame(self) -> bool:
        # update all animation elements
        for animator in self.animators:
            animator.update_frames_index()
            animator.make_next_frame()
            animator.interpolation_idx += 1
        return True

    def on_frame_end(self):
        """
            Called at the end of each frame to add additional elements to the animation
            and style axes
        """
        # draw CoM
        self.axes["A"].plot(
            self.locomotion.com.x,
            self.locomotion.com.y,
            lw=2,
            color=self.locomotion.com.color,
        )
