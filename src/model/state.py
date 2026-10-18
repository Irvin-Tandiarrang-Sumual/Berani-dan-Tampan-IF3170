import random

from type.coordinate import Coordinate

from dataclasses import dataclass

@dataclass
class State:
    inside_package_ids_per_truck : dict[str, list[(str, Coordinate)]]
    outside_package_ids : list[int]