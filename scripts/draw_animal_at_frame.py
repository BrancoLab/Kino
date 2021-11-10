import sys

sys.path.append("./")

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from kino.animal import mouse
from kino.locomotion import Locomotion
from kino.draw import DrawAnimal


tracking = pd.read_hdf("scripts/example_tracking.h5")


locomotion = Locomotion(mouse, tracking, fps=60)

f, ax = plt.subplots(figsize=(8, 10))

DrawAnimal.at_frame(mouse, locomotion, np.arange(0, 230, 10), ax)

plt.show()
