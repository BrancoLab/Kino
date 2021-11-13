import sys

sys.path.append("./")

import pandas as pd
import matplotlib.pyplot as plt


from kino.animal import mouse
from kino.locomotion import Locomotion
from kino.draw import Steps


tracking = pd.read_hdf("scripts/example_tracking.h5")


locomotion = Locomotion(mouse, tracking, fps=60)
egocentric = locomotion.to_egocentric()

f = plt.figure(figsize=(20, 10))
axes = f.subplot_mosaic(
    """
        AAAE
        BBBE
        CCCF
        DDDF
    """
)
for ax in "EF":
    axes[ax].axis("equal")
paw_axes = {
    "left_fl": axes["A"],
    "right_fl": axes["B"],
    "left_hl": axes["C"],
    "right_hl": axes["D"],
}

# ----------------------------------- plot ----------------------------------- #
for n, paw in enumerate(locomotion.paws.values()):
    # plot steps in ego/allo frames
    Steps.sticks_and_balls(paw, axes["E"])
    Steps.sticks_and_balls(paw, axes["F"], egocentric.bodyparts[paw.name])

    # plot steps on speed traces
    Steps.overlay_on_speed_trace(paw, paw_axes[paw.name])


plt.show()
