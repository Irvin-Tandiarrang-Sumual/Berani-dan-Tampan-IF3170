from types.dimension import Dimension

class Truck:
    def __init__(self, dimension : Dimension, maxCapacity : int):
        self.dimension = dimension
        self.maxCapacity = maxCapacity