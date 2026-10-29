from copy import deepcopy
from dataclasses import dataclass

from type.coordinate import Coordinate
from type.orientation import Orientation

@dataclass(frozen=True)
class PackagePlacement:
    truck_id: str | None
    coordinate: Coordinate | None
    orientation: Orientation

    def __post_init__(self) -> None:
        if (self.truck_id is None) != (self.coordinate is None):
            raise ValueError("truck_id and coordinate must both be set or both be None")

    @property
    def is_inside(self) -> bool:
        return self.truck_id is not None


@dataclass
class State:
    placements: dict[str, PackagePlacement]

    def copy(self) -> "State":
        return deepcopy(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, State):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def get_inside_package_ids(self, truck_id: str) -> list[str]:
        return [
            package_id
            for package_id, placement in self.placements.items()
            if placement.truck_id == truck_id
        ]

    def get_outside_package_ids(self) -> list[str]:
        return [
            package_id
            for package_id, placement in self.placements.items()
            if not placement.is_inside
        ]

    def to_dict(self) -> dict[str, dict]:
        result = {}
        for package_id, placement in self.placements.items():
            coordinate = placement.coordinate
            orientation = placement.orientation
            result[package_id] = {
                "truck_id": placement.truck_id,
                "coordinate": None if coordinate is None else {
                    "x": coordinate.x,
                    "y": coordinate.y,
                    "z": coordinate.z,
                },
                "orientation": {
                    "w": orientation.w,
                    "l": orientation.l,
                    "h": orientation.h,
                },
            }
        return result

    def get_inside_packages_per_truck(self) -> dict[str, list[PackagePlacement]]:
        packages_per_truck  : dict[str, list]= {}
        for packaged_id, placement in self.placements.items():
            if packaged_id:
                packages_per_truck[placement.truck_id].append(placement)

        return packages_per_truck