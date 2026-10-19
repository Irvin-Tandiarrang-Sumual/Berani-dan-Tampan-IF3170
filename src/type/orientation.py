from dataclasses import dataclass
from itertools import permutations

from type.dimension import Dimension


@dataclass(frozen=True)
class Orientation:
    """Map setiap dimensi original package (w, l, h) ke truck axis (x, y, z)."""

    w: str
    l: str
    h: str

    def __post_init__(self) -> None:
        if {self.w, self.l, self.h} != {"x", "y", "z"}:
            raise ValueError("Orientation must use x, y, and z exactly once")

    def get_oriented_dimensions(self, dimension: Dimension) -> Dimension:
        """Return ukuran efektif x, y, z as Dimension(w, l, h)."""
        sizes = {
            self.w: dimension.w,
            self.l: dimension.l,
            self.h: dimension.h,
        }
        return Dimension(sizes["x"], sizes["y"], sizes["z"])

    def rotate(self, axis: str) -> "Orientation":
        """Return rotasi 90 derajat"""
        axis_mapping = {
            "x": {"x": "x", "y": "z", "z": "y"},
            "y": {"x": "z", "y": "y", "z": "x"},
            "z": {"x": "y", "y": "x", "z": "z"},
        }
        if axis not in axis_mapping:
            raise ValueError("Rotation axis must be x, y, or z")
        mapping = axis_mapping[axis]
        return Orientation(mapping[self.w], mapping[self.l], mapping[self.h])

    @staticmethod
    def all_orientations() -> list["Orientation"]:
        """Return semua package orientasi."""
        return [Orientation(*axes) for axes in permutations(("x", "y", "z"))]
