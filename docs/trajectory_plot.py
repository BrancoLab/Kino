import sys

sys.path.append("./")

import numpy as np
import matplotlib.pyplot as plt


from kino.geometry import Trajectory
from kino.draw import colors
from kino.draw.gliphs import Arrows

"""
    Plot the basic elements of a Kino trajectory, for docs.
"""

f, ax = plt.subplots(figsize=(16, 9))

x = np.linspace(0, np.pi, 100)
y = np.cos(x)

traj = Trajectory(x, y, name="my trajectory", smoothing_window=1)


# draw trajectory and vectors
ax.plot(traj.x, traj.y, color=traj.color, label=traj.name, lw=2)

Arrows(
    traj.x,
    traj.y,
    traj.tangent.angle,
    L=0.1,
    label="tangent",
    ax=ax,
    step=10,
    color=colors.tangent,
    width=5,
    outline=True,
)
Arrows(
    traj.x,
    traj.y,
    traj.normal.angle,
    L=0.1,
    label="normal",
    ax=ax,
    step=10,
    color=colors.normal,
    width=5,
    outline=True,
)


ax.legend()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.set(xticks=[0, np.pi], yticks=[-1, 0, 1], xlabel="X - cm", ylabel="Y - cm")

f.savefig("./docs/trajectory.png")
