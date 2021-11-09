from typing import Any
import matplotlib.pyplot as plt


def draw(object: Any, *args, ax: plt.Axes = None, **kwargs) -> plt.Axes:
    """
        Plots any class with a __draw__ method
    """
    ax = ax or plt.gca()
    ax.axis("equal")

    object.__draw__(ax, *args, **kwargs)

    return ax
