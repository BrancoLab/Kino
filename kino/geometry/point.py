
import numpy as np
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float

    @property
    def xy(self): 
        return np.array([self.x, self.y])