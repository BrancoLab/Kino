import sys

sys.path.append("./")

import pandas as pd


from kino.animal import mouse
from kino.locomotion import Locomotion
from kino.animate import CompleteAnimation

"""
    Creates a slowmo animation of the locomotion bout
    in the allocentric and egocentric views
"""

tracking = pd.read_hdf("scripts/example_tracking.h5")


locomotion = Locomotion(mouse, tracking, fps=60)

for bp in locomotion.bodyparts.values():
    bp.thetadot[0] = 0

egocentric = locomotion.to_egocentric()

anim = CompleteAnimation(
    locomotion,
    egocentric,
    fps=60,
    bodyparts=["right_fl", "right_hl", "left_fl", "left_hl", "com"],
)
anim.animate("cache/complete_locomotion.mp4")
