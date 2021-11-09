import matplotlib.pyplot as plt

from kino.locomotion import Locomotion


def plot_locomotion_2D(locomotion: Locomotion, ax: plt.Axes):
    """
        Draws a 2D trace with the locomotion trajectory of each bodypart
    """

    ax.axis("equal")

    for bp in locomotion.bodyparts.values():
        lw = 2 if bp.name == "body" else 1
        alpha = 1 if bp.name == "body" else 0.5
        zorder = 2 if bp.name == "body" else 1

        ax.plot(bp.x, bp.y, color=bp.color, lw=lw, alpha=alpha, zorder=zorder)
