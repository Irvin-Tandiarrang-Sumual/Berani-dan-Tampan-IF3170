import json
from pathlib import Path
from model.problem import Problem
from model.truck import Truck
from model.package import Package
from type.dimension import Dimension
from type.orientation import Orientation

class Reader:
    def __init__(self, filename : str):
        self.filepath = Path(__file__).parent.parent.parent / "tests" / filename
        
    def loadProblem(self) -> Problem:
        with open(self.filepath, "r") as file:
            data = json.load(file)
        return Problem(
            self._load_trucks(data["trucks"]),
            self._load_packages(data["packages"])
        )

    def _load_trucks(self, trucks : list[dict]) -> list[Truck]:
        t = []
        for truck in trucks:
            t.append(Truck(
                Dimension(
                    truck["dimension"]["w"],
                    truck["dimension"]["l"],
                    truck["dimension"]["h"]
                ), truck["maxCapacity"]
            ))
        return t

    def _load_packages(self, packages : list[dict]) -> list[Package]:
        p = []
        for package in packages:
            p.append(Package(
                package["id"],
                Dimension(
                    package["dimension"]["w"],
                    package["dimension"]["l"],
                    package["dimension"]["h"]
                ),
                Orientation(
                    package["orientation"]["w"],
                    package["orientation"]["l"],
                    package["orientation"]["h"]
                ),
                package["value"],
                package["weight"],
                package["isFragile"],
                package["ETA"]
            ))
        return p