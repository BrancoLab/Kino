import sys

sys.path.append("./")

import pandas as pd
import matplotlib.pyplot as plt


from kino.animal import mouse
from kino.locomotion import Locomotion
import kino.draw.locomotion as draw_locomotion


tracking = pd.read_hdf("scripts/example_tracking.h5")


locomotion = Locomotion(mouse, tracking, fps=60)

f, ax = plt.subplots(figsize=(8, 10))
draw_locomotion.plot_locomotion_2D(locomotion, ax)

plt.show()
