import matplotlib.pyplot as plt

from myterial import blue_grey_dark

from kino.locomotion import Locomotion
from kino.draw.gliphs import Arrows
from kino.draw import colors


def plot_locomotion_2D(locomotion: Locomotion, ax: plt.Axes):
    """
        Draws a 2D trace with the locomotion trajectory of each bodypart
    """

    ax.axis("equal")

    # plot com
    ax.plot(
        locomotion.com.x, locomotion.com.y, color="k", lw=1, alpha=1, zorder=2
    )

    # plot longitudinal and normal acceleration
    acc_longitudinal = locomotion.com.longitudinal_acceleration
    acc_norm = locomotion.com.normal_acceleration

    acc_colors = colors.map_color(acc_longitudinal, name="bwr")

    Arrows(
        locomotion.com.x,
        locomotion.com.y,
        locomotion.com.tangent.angle,
        L=acc_longitudinal / acc_longitudinal.max() * 2,
        width=3,
        outline=True,
        color=acc_colors,
        ax=ax,
        label="longitudinal acc.",
    )

    Arrows(
        locomotion.com.x,
        locomotion.com.y,
        locomotion.com.normal.angle,
        L=acc_norm / acc_norm.max() * 2,
        width=2,
        outline=True,
        color=blue_grey_dark,
        zorder=-1,
        ax=ax,
        label="normal acc.",
    )
