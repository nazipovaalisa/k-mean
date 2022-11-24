import math
import numpy as np


class point:

    def __init__(self, name: str, coords: np.array([])):
        self.name = name
        self.coords = coords

    def distance(self, e):
        return np.linalg.norm(self.coords - e.coords)

