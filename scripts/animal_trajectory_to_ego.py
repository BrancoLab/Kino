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

tracking = pd.read_hdf("scripts/example_tracking.h5")


locomotion = Locomotion(mouse, tracking, fps=60)
egocentric = locomotion.to_egocentric()

f, axes = plt.subplots(figsize=(12, 8), ncols=2)

# draw allocentric
frames = [20, 40, 60]
DrawAnimal.at_frame(mouse, locomotion, frames, axes[0])
DrawAnimal.at_frame(mouse, egocentric, frames, axes[1])

print(egocentric.body_axis.vector.angle2[frames])

axes[0].set(title="Allocentric")
axes[1].set(title="Egocentric", xlim=[-8, 8], ylim=[-8, 8])

for ax in axes:
    ax.axis("equal")

plt.show()
