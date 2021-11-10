import matplotlib.pyplot as plt
from celluloid import Camera
from typing import Union, List
from loguru import logger
from pathlib import Path
import numpy as np

from kino.progress import track
from kino.locomotion import Locomotion
from kino.draw import DrawAnimal, gliphs
from kino.geometry import Vector, Trajectory


class AnimationCore:
    """
        Core animation functionality
    """

    def __init__(
        self,
        original_fps: int,
        animation_fps: int,
        n_original_frames: int = 1,
    ):

        # TODO REMOVE and ignore mypy warning
        self.figure = plt.figure()

        # compute the number of interpolated frame for each original frame
        self.n_interpolated = int(original_fps / animation_fps)
        if self.n_interpolated < 1:
            raise ValueError(
                f"Cannot generate animation at {animation_fps} fps given original data fps of: {original_fps}"
            )
        self.P = (
            np.linspace(0, 1, self.n_interpolated)
            if self.n_interpolated > 1
            else [1]
        )
        self.fps = animation_fps

        # compute the total number of frames (original * interpolation)
        self.n_frames_tot = int(n_original_frames * len(self.P))

        # initialize animation parameters
        self.frame_idx = 0
        self.interpolation_idx = 0
        self.n_original_frames = n_original_frames

    def on_animation_start(self):
        return

    def make_next_frame(self) -> bool:
        return False

    def on_frame_end(self):
        return

    def update_frames_index(self):
        """
            Updates frame and interpolation indices
        """
        # reset interpolation index
        if self.interpolation_idx >= len(self.P):
            self.interpolation_idx = 0
            self.frame_idx += 1

    def animate(self, save_path: Union[str, Path], save: bool = True):
        """
            Create the animation and save it to file
        """
        self.on_animation_start()

        # initialize camera
        camera = Camera(self.figure)

        # run
        logger.debug(
            f"Creating animation with {self.n_frames_tot} frames | fps: {self.fps}"
        )
        for framen in track(
            range(self.n_frames_tot),
            transient=True,
            description="Creating animation",
        ):
            self.update_frames_index()

            running = self.make_next_frame()

            self.on_frame_end()
            self.interpolation_idx += 1
            camera.snap()

            if not running:
                break

        # save
        if save:
            logger.debug("   ... saving")
            animation = camera.animate(interval=1000 / self.fps)
            animation.save(save_path, fps=self.fps)
            logger.debug(f'Animation created, saved at: "{save_path}"')


class PoseAnimation(AnimationCore):
    """
        Base class to animate a Locomotion trajectory showing
        the animal's pose at each frame.
        (either egocentric or allocentric reference frames)
    """

    def __init__(
        self,
        locomotion: Locomotion,
        fps: int = None,
        ax: plt.Axes = None,
        bodyparts: List[str] = None,
    ):
        self.locomotion = locomotion
        fps = fps or locomotion.fps
        self.bps_to_draw = bodyparts or list(self.locomotion.bodyparts.keys())
        self.ax = ax or plt.gca()
        self.figure = self.ax.figure

        super().__init__(locomotion.fps, fps, len(locomotion))

    def make_next_frame(self) -> bool:
        if (
            self.frame_idx >= len(self.locomotion) - 2
        ):  # -2 because of interpolation
            return False

        # get interpolation factor
        p = self.P[self.interpolation_idx]

        # draw the interpolated position of the animal
        DrawAnimal.at_frame_interpolated(
            self.locomotion.animal, self.locomotion, self.frame_idx, p, self.ax
        )
        return True


class ScalarAnimation(AnimationCore):
    """
        Animates a scalar (1d np.array)
    """

    def __init__(
        self,
        scalar: np.array,
        data_fps: int = 1,
        animation_fps: int = 1,
        ax: plt.Axes = None,
        plot_kwargs: dict = {},
        time_range: float = 1,  # number of seconds before/after t=0 to display
    ):

        super().__init__(data_fps, animation_fps, len(scalar))

        self.scalar = scalar
        self.ax = ax or plt.gca()
        self.figure = self.ax.figure
        self.plot_kwargs = plot_kwargs

        # compute window width
        self.wnd = int(time_range * data_fps)
        self.time_range = time_range

    def make_next_frame(self) -> bool:
        """
            Shows the data in a sliding time window
            around the current frame
        """
        t = self.frame_idx
        x = np.arange(-self.wnd, self.wnd, 1)

        # prepare XY data for plotting
        if t == 0:
            return True
        elif t < self.wnd:
            pad = 2 * self.wnd - t
            # less than half-window has elapsed
            y = np.zeros_like(x)
            y[pad:] = self.scalar[:t]
        elif t > self.n_original_frames - self.wnd:
            # less than half-window from end
            pad = 2 * self.wnd - len(self.scalar[t - self.wnd :])
            y = np.zeros_like(x)
            y[:-pad] = self.scalar[t - self.wnd :]
        else:
            y = self.scalar[t - self.wnd : t + self.wnd]

        # plot
        self.ax.plot(x, y, **self.plot_kwargs)
        self.ax.axvline(0, lw=2, color=[0.4, 0.4, 0.4], ls="--", zorder=-1)
        self.ax.set(xticks=[-self.wnd, 0, self.wnd])

        return True


class VectorAnimation(AnimationCore):
    """
        Draws a vector as an arrow for each frame.
        If a trajectory is passed, the vector is 
        anchored to the trajectory, otherwise it's
        centered at the origin
    """

    def __init__(
        self,
        vector: Vector,
        trajectory: Trajectory = None,
        vector_length: float = None,  # fix vec len or let it vary
        data_fps: int = 1,
        animation_fps: int = 1,
        ax: plt.Axes = None,
        plot_kwargs: dict = {},
        time_range: float = 1,  # number of seconds before/after t=0 to display
    ):

        super().__init__(data_fps, animation_fps, len(vector))

        self.vector = vector
        self.trajectory = trajectory
        self.ax = ax or plt.gca()
        self.figure = self.ax.figure
        self.plot_kwargs = plot_kwargs
        self.vector_length = vector_length

        # compute window width
        self.wnd = int(time_range * data_fps)
        self.time_range = time_range

    def make_next_frame(self) -> bool:
        """
            Just plot an arrow as the vector
        """
        # get xy position
        if self.trajectory is None:
            x, y = 0, 0
        else:
            x = self.trajectory[self.frame_idx].x
            y = self.trajectory[self.frame_idx].y

        vector = self.vector[self.frame_idx]
        gliphs.Arrow(
            x,
            y,
            vector.angle,
            L=self.vector_length or vector.magnitude,
            ax=self.ax,
            **self.plot_kwargs,
        )
        return True
