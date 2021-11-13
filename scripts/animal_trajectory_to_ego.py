import sys

sys.path.append("./")

import pandas as pd
import matplotlib.pyplot as plt


from kino.animal import mouse
from kino.locomotion import Locomotion
from kino.draw import DrawAnimal

"""
    Plots the pose of the mouse at a few frames in the allocentric and egocentric
    reference frame
"""
frame = 100

tracking = pd.read_hdf("scripts/example_tracking.h5")

# get allo/ego trajectories
locomotion = Locomotion(mouse, tracking, fps=60)
egocentric = locomotion.to_egocentric()

# project the position of the center of mass to egocentric reference frame
com_2_ego = egocentric.project_to_egocentric_at_frame(locomotion.com, frame)

# plot
f, axes = plt.subplots(figsize=(12, 8), ncols=2)

DrawAnimal.at_frame(mouse, locomotion, frame, axes[0])
DrawAnimal.at_frame(mouse, egocentric, frame, axes[1])

axes[1].plot(
    com_2_ego.x[frame - 20 : frame + 20],
    com_2_ego.y[frame - 20 : frame + 20],
    color=com_2_ego.color,
)

axes[0].set(title="Allocentric")
axes[1].set(title="Egocentric", xlim=[-8, 8], ylim=[-8, 8])

for ax in axes:
    ax.axis("equal")

plt.show()
