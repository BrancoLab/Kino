import sys

sys.path.append("./")

import pandas as pd
import matplotlib.pyplot as plt


from kino.animal import mouse
from kino.locomotion import Locomotion
from kino.animate import VectorAnimation


"""
    Example on how to animate a vector variable
"""


tracking = pd.read_hdf("scripts/example_tracking.h5")


locomotion = Locomotion(mouse, tracking, fps=60)

f, ax = plt.subplots(figsize=(6, 8))

animator = VectorAnimation(
    locomotion.bodyparts["body"].velocity,
    # trajectory = locomotion.body,
    data_fps=locomotion.fps,
    animation_fps=30,
    ax=ax,
    plot_kwargs=dict(width=4, color="red"),
)
animator.animate("cache/vector_animation.mp4")
