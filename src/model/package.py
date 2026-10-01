from type.dimension import Dimension
from type.orientation import Orientation

class Package:
    def __init__(self, id : str, dimension : Dimension,
                orientation : Orientation, value : int,
                weight : int, isFragile : bool, ETA : int):
        self.id = id
        self.dimension = dimension
        self.orientation = Orientation
        self.value = value
        self.weight = weight
        self.isFragile = isFragile
        self.ETA = ETA