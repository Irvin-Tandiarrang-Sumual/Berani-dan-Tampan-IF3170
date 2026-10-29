from type.dimension import Dimension

class Truck:
    _id_count = 1
    def __init__(self, dimension : Dimension, maxCapacity : int):
        self.dimension = dimension
        self.maxCapacity = maxCapacity

        self.id = f"Truck-{Truck._id_count}"
        Truck._id_count += 1