import sys

sys.path.append("./")

import pandas as pd
import matplotlib.pyplot as plt


from kino.animal import mouse
from kino.locomotion import Locomotion
from kino.animate.base import BaseAnimation


tracking = pd.read_hdf("scripts/example_tracking.h5")


locomotion = Locomotion(mouse, tracking, fps=60)
locomotion.compute_center_of_mass("right_fl", "right_hl", "left_fl", "left_hl")

f, ax = plt.subplots(figsize=(6, 8))

animator = BaseAnimation(
    locomotion,
    fps=30,
    ax=ax,
    bodyparts=["right_fl", "right_hl", "left_fl", "left_hl", "com", "com"],
)
animator.animate("cache/base_locomotion.mp4")
