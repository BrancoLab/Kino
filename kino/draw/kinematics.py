import matplotlib.pyplot as plt
import numpy as np

from kino.steps import Paw
from kino.geometry import Trajectory


class Steps:
    @staticmethod
    def overlay_on_speed_trace(paw: Paw, ax: plt.Axes):
        """
            Overlay the start/end of the steps on a paw's speed trace
        """
        color = paw.trajectory.color
        speed = paw.normalized_speed

        # mark starts / end
        ax.plot(speed, color=color, lw=0.5)
        ax.axhline(paw.speed_th, zorder=-1, color="k", ls="--", lw=0.5)
        ax.scatter(
            paw.swings_start,
            speed[paw.swings_start],
            color=color,
            s=25,
            ec=color,
            lw=1,
            alpha=0.5,
            zorder=100,
        )

        ax.scatter(
            paw.swings_end,
            speed[paw.swings_end],
            color="white",
            s=25,
            ec=color,
            lw=1,
            alpha=0.5,
            zorder=100,
        )

        # mark trace
        for start, stop in zip(paw.swings_start, paw.swings_end):
            ax.plot(
                np.arange(start, stop + 1),
                speed[start : stop + 1],
                lw=2,
                color=color,
            )

    @staticmethod
    def sticks_and_balls(
        paw: Paw, ax: plt.Axes, trajectory: Trajectory = None
    ):
        """
            Do a o---o  balls and stick plot marking the
            start/end of each swing phase based on XY of
            a trajectory
        """

        if trajectory is None:
            trajectory = paw.trajectory
        color = trajectory.color
        x, y = trajectory.x, trajectory.y

        # mark starts
        ax.scatter(
            x[paw.swings_start],
            y[paw.swings_start],
            color=color,
            s=25,
            ec=color,
            lw=1,
            zorder=100,
        )

        ax.scatter(
            x[paw.swings_end],
            y[paw.swings_end],
            color="white",
            s=25,
            ec=color,
            lw=1,
            zorder=100,
        )

        for start, stop in zip(paw.swings_start, paw.swings_end):
            ax.plot(
                [x[start], x[stop]], [y[start], y[stop]], lw=2, color=color
            )
