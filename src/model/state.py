from model.truck import Truck
from model.package import Package

class State:
    def __init__(self, trucks : list[Truck], packages : list[Package]):
        self.trucks = trucks
        self.packages = packages