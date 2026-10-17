import random

from model.package import Package
from model.truck import Truck
from type.dimension import Dimension
from type.coordinate import Coordinate

class State:
    def __init__(self, insidePackage, outsidePackage: list[(Package, Coordinate)], truck: Truck):
        # pastikan kalau udah di insidepackage ga akan di outside package, jadi untuk definisi state baru outsidePackage diisi []
        self.insidePackage = insidePackage
        self.outsidePackage = outsidePackage
        self.truck = truck

    def generate_next_random_state(self) -> State:
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
        
            