import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle as Rectangle_patch
from matplotlib.patches import Polygon as Polygon_patch

from typing import Union

from myterial import blue_grey_dark, grey_dark


class Arrow:
    """
        Draws an arrow at a point and angle
    """

    def __init__(
        self,
        x: float,
        y: float,
        theta: float,  # in degrees
        L: float = 1,  # length
        width: float = 4,
        head_width: float = None,
        color: str = blue_grey_dark,
        zorder: int = 100,
        ax: plt.Axes = None,
        outline: bool = False,  # draw a larger darker arrow under the main one
        label: str = None,
        alpha: float = 1,
        **kwargs,
    ):
        if outline:
            widths = [width + 1, width]
            colors = ["k", color]
            labels = [None, label]
        else:
            widths = [width]
            colors = [color]
            labels = [label]

        ax = ax or plt.gca()

        # compute arrow position
        theta = np.radians(theta)
        angle = np.deg2rad(30)

        x_start = x
        y_start = y
        x_end = x + L * np.cos(theta)
        y_end = y + L * np.sin(theta)
        if head_width is None:
            head_width = 0.5 * L

        theta_hat_L = theta + np.pi - angle
        theta_hat_R = theta + np.pi + angle

        x_hat_start = x_end
        x_hat_end_L = x_hat_start + head_width * np.cos(theta_hat_L)
        x_hat_end_R = x_hat_start + head_width * np.cos(theta_hat_R)

        y_hat_start = y_end
        y_hat_end_L = y_hat_start + head_width * np.sin(theta_hat_L)
        y_hat_end_R = y_hat_start + head_width * np.sin(theta_hat_R)

        # draw
        for width, color, label in zip(widths, colors, labels):
            ax.plot(
                [x_start, x_end],
                [y_start, y_end],
                color=color,
                linewidth=width,
                zorder=zorder,
                label=label,
                alpha=alpha,
                **kwargs,
            )
            ax.plot(
                [x_hat_start, x_hat_end_L],
                [y_hat_start, y_hat_end_L],
                color=color,
                linewidth=width,
                zorder=zorder,
                alpha=alpha,
            )
            ax.plot(
                [x_hat_start, x_hat_end_R],
                [y_hat_start, y_hat_end_R],
                color=color,
                linewidth=width,
                zorder=zorder,
                alpha=alpha,
            )


class Arrows:
    """
        Draws an arrow at a point and angle
    """

    def __init__(
        self,
        x: list,
        y: list,
        theta: list,  # in degrees
        label=None,
        step: int = 1,  # draw arrow every step
        L: Union[list, np.ndarray, float] = 1,
        color: Union[str, list] = "k",
        **kwargs,
    ):

        # make sure L and color are iterable
        if isinstance(L, (int, float)):
            L = [L] * len(x)
        if isinstance(color, str):
            color = [color] * len(x)

        # draw each arrow
        for i in range(len(x)):
            if i > 0:
                label = None
            if i % step == 0:
                Arrow(
                    x[i],
                    y[i],
                    theta[i],
                    label=label,
                    L=L[i],
                    color=color[i],
                    **kwargs,
                )


class Dot:
    def __init__(
        self,
        x: float,
        y: float,
        ax: plt.Axes = None,
        zorder=100,
        s=100,
        color="k",
        **kwargs,
    ):
        ax = ax or plt.gca()
        ax.scatter(x, y, zorder=zorder, s=s, color=color, **kwargs)


class Dots:
    def __init__(
        self,
        x: np.ndarray,
        y: np.ndarray,
        ax: plt.Axes = None,
        zorder=100,
        s=100,
        color="k",
        step: int = 1,
        **kwargs,
    ):
        ax = ax or plt.gca()
        ax.scatter(
            x[::step], y[::step], zorder=zorder, s=s, color=color, **kwargs
        )


class Rectangle:
    def __init__(
        self,
        x_0,
        x_1,
        y_0,
        y_1,
        ax: plt.Axes = None,
        color=blue_grey_dark,
        **kwargs,
    ):
        ax = ax or plt.gca()
        rect = Rectangle_patch(
            (x_0, y_0), x_1 - x_0, y_1 - y_0, color=color, **kwargs
        )
        ax.add_patch(rect)


class Polygon:
    def __init__(
        self, *points, ax: plt.Axes = None, color=grey_dark, **kwargs,
    ):
        """
            Given a list of tuples/lists of XY coordinates of each point, 
            this class draws a polygon
        """
        ax = ax or plt.gca()

        xy = np.vstack(points)

        patch = Polygon_patch(xy, color=color, **kwargs)
        ax.add_patch(patch)


if __name__ == "__main__":
    from numpy.random import uniform

    X = uniform(0, 10, 5)
    Y = uniform(0, 20, 5)
    T = uniform(0, 360, 5)

    f, ax = plt.subplots(figsize=(7, 10))

    for x, y, t in zip(X, Y, T):
        Arrow(ax, x, y, t, 2)

    plt.show()
