from model.truck import Truck
from model.package import Package
from model.state import State

from type.coordinate import Coordinate
from random import random

class Problem:
    def __init__(self, trucks : list[Truck], packages : list[Package]):
        self.trucks = trucks
        self.packages = packages
        
        self.truck_map = {truck.id: truck for truck in self.trucks}
        self.package_map = {package.id: package for package in self.packages}

    def calculate_objective_value(self, state : State) -> int:
        value_sum = 0
        for _, package_ids in state.inside_packages_per_truck.items():
            for package_id in package_ids:
                value_sum += self.package_map[package_id].value
        return value_sum

    def generate_initial_state() -> State:
        return State

    def generate_next_random_state(self, current_state : State) -> State:
        return State()

    def generate_next_state(self) -> State:
        # greedy untuk tentuin koordinat sama penuh penuhin dimensi truk
        # pake randomizer buat tentuin dirotate atau ngga
        
        # kode sementara
        if not allPackage:
            print("package kosong")
            return 0
        
        dimTruck = self.truck.dimension
        allPackage = self.insidePackage[0].append(self.outsidePackage[0])
        listCoordinate = []
        for package in allPackage:
            dimPackage = package.dimension
            x_package = random.randrange(0, dimTruck.l - dimPackage.l)
            y_package = random.randrange(0, dimTruck.h - dimPackage.h)
            z_package = random.randrange(0, dimTruck.w - dimPackage.z)
            listCoordinate.append(Coordinate(x_package, y_package, z_package))
            
            # nanti cek intersect and collision, sama melayang
            
        allPackage[1] = listCoordinate
        # ambil package pertama, taruh di luar
        self.outsidePackage[0] = allPackage.pop(0)
        self.insidePackage[0] = allPackage
        
        return self