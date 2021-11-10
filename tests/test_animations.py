import sys

sys.path.append("./")

import pandas as pd
import matplotlib.pyplot as plt


from kino.animal import mouse
from kino.locomotion import Locomotion
from kino.animate import PoseAnimation, VectorAnimation, ScalarAnimation


tracking = pd.read_hdf("scripts/example_tracking.h5")


locomotion = Locomotion(mouse, tracking, fps=60)


def test_pose():
    f, ax = plt.subplots(figsize=(6, 8))

    animator = PoseAnimation(
        locomotion,
        fps=30,
        ax=ax,
        bodyparts=["right_fl", "right_hl", "left_fl", "left_hl", "com"],
    )
    animator.animate("cache/base_locomotion.mp4", save=False)


def test_scalar():
    f, ax = plt.subplots(figsize=(6, 8))

    animator = ScalarAnimation(
        locomotion.bodyparts["body"].speed,
        data_fps=locomotion.fps,
        animation_fps=30,
        ax=ax,
        plot_kwargs=dict(lw=2, color="red"),
    )
    animator.animate("cache/scalar_animation.mp4", save=False)


def test_vector():
    f, ax = plt.subplots(figsize=(6, 8))

    animator = VectorAnimation(
        locomotion.bodyparts["body"].velocity,
        data_fps=locomotion.fps,
        animation_fps=30,
        ax=ax,
        plot_kwargs=dict(width=4, color="red"),
    )
    animator.animate("cache/vector_animation.mp4", save=False)
