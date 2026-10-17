from model.truck import Truck
from model.package import Package
from model.state import State

class Problem:
    def __init__(self, trucks : list[Truck], packages : list[Package]):
        self.trucks = trucks
        self.packages = packages

    def generate_initial_state() -> State:
        return State

    def calculate_objective_value() -> float:
        return 0.0