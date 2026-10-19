import random
import colorsys
from model.truck import Truck
from model.package import Package
from model.state import State, PackagePlacement

from type.orientation import Orientation
from type.coordinate import Coordinate

# Box: (x_min, y_min, z_min, x_max, y_max, z_max)
Box = tuple[int, int, int, int, int, int]

class Problem:
    def __init__(self, trucks: list[Truck], packages: list[Package]):
        self.trucks = trucks
        self.packages = packages
        self.truck_map = {truck.id: truck for truck in trucks}
        self.package_map = {package.id: package for package in packages}
        self.package_colors = self._generate_package_colors()
    
        if len(self.truck_map) != len(trucks):
            raise ValueError("Duplicate truck ID")
        if len(self.package_map) != len(packages):
            raise ValueError("Duplicate package ID")

    def _get_package_box(self, package_id: str, placement: PackagePlacement) -> Box:
        coordinate = placement.coordinate
        if coordinate is None:
            raise ValueError("An outside package does not have a box")
        dimensions = placement.orientation.get_oriented_dimensions(self.package_map[package_id].dimension)
        return (coordinate.x, coordinate.y, coordinate.z, coordinate.x + dimensions.w, coordinate.y + dimensions.l, coordinate.z + dimensions.h)
    
    def _get_boxes_per_truck(self, state: State) -> dict[str, dict[str, Box]]:
        boxes = {truck_id: {} for truck_id in self.truck_map}
        for package_id, placement in state.placements.items():
            if placement.is_inside:
                boxes[placement.truck_id][package_id] = self._get_package_box(package_id, placement)
        return boxes

    @staticmethod
    def _boxes_overlap(first: Box, second: Box) -> bool:
        return (
            first[0] < second[3] and second[0] < first[3]
            and first[1] < second[4] and second[1] < first[4]
            and first[2] < second[5] and second[2] < first[5]
        )

    @staticmethod
    def _supports(bottom: Box, top: Box) -> bool:
        return (
            bottom[5] == top[2]
            and bottom[0] < top[3] and top[0] < bottom[3]
            and bottom[1] < top[4] and top[1] < bottom[4]
        )

    def _is_package_within_bounds(self, state: State) -> bool:
        """Untuk mengecek batas truk (ukuran, bukan berat)"""
        for truck_id, boxes in self._get_boxes_per_truck(state).items():
            dimension = self.truck_map[truck_id].dimension
            if any(size <= 0 for size in (dimension.w, dimension.l, dimension.h)):
                return False
            for box in boxes.values():
                if not (0 <= box[0] < box[3] <= dimension.w and 0 <= box[1] < box[4] <= dimension.l and 0 <= box[2] < box[5] <= dimension.h):
                    return False
        return True

    def _is_packages_overlapping(self, state: State) -> bool:
        for boxes in self._get_boxes_per_truck(state).values():
            placed = list(boxes.values())
            for i in range(len(placed)):
                for j in range(i + 1, len(placed)):
                    if self._boxes_overlap(placed[i], placed[j]):
                        return True
        return False

    def _is_package_floating(self, state: State) -> bool:
        for boxes in self._get_boxes_per_truck(state).values():
            for package_id, box in boxes.items():
                if box[2] == 0:
                    continue 
                if not any(
                    other_id != package_id and self._supports(other_box, box)
                    for other_id, other_box in boxes.items()
                ):
                    return True
        return False

    def _is_fragile_supporting_another(self, state: State) -> bool:
        for boxes in self._get_boxes_per_truck(state).values():
            for package_id, box in boxes.items():
                if not self.package_map[package_id].isFragile:
                    continue
                if any(
                    other_id != package_id and self._supports(box, other_box)
                    for other_id, other_box in boxes.items()
                ):
                    return True
        return False

    def _is_truck_overloaded(self, state: State) -> bool:
        for truck in self.trucks:
            weight = sum(self.package_map[package_id].weight for package_id in state.get_inside_package_ids(truck.id))
            if weight > truck.maxCapacity:
                return True
        return False

    def is_state_valid(self, state: State) -> bool:
        if not isinstance(state, State):
            return False
        if set(state.placements) != set(self.package_map):
            return False

        for placement in state.placements.values():
            if not isinstance(placement, PackagePlacement):
                return False
            if not isinstance(placement.orientation, Orientation):
                return False
            if not placement.is_inside:
                if placement.coordinate is not None:
                    return False
                continue
            if placement.truck_id not in self.truck_map:
                return False
            coordinate = placement.coordinate
            if coordinate is None:
                return False
            if any(type(value) is not int for value in (coordinate.x, coordinate.y, coordinate.z)):
                return False

        return (
            self._is_package_within_bounds(state)
            and not self._is_packages_overlapping(state)
            and not self._is_package_floating(state)
            and not self._is_fragile_supporting_another(state)
            and not self._is_truck_overloaded(state)
        )
        
    def calculate_objective_value(self, state: State) -> int:
        if not self.is_state_valid(state):
            raise ValueError("Cannot calculate objective for an invalid state")
        return sum(
            self.package_map[package_id].value
            for package_id, placement in state.placements.items()
            if placement.is_inside
        )

    def _candidate_coordinates(self, state: State, package_id: str, truck_id: str, orientation: Orientation, rng: random.Random, max_candidates: int = 32) -> list[Coordinate]:
        """Coba posisi pada lantai, di sisi paket, dan di atas support."""
        truck = self.truck_map[truck_id]
        dimensions = orientation.get_oriented_dimensions(self.package_map[package_id].dimension)
        max_x = truck.dimension.w - dimensions.w
        max_y = truck.dimension.l - dimensions.l
        max_z = truck.dimension.h - dimensions.h
        if min(max_x, max_y, max_z) < 0:
            return []

        candidates = {(0, 0, 0)}
        support_heights = [0]
        for other_id, placement in state.placements.items():
            if other_id == package_id or placement.truck_id != truck_id:
                continue
            x0, y0, z0, x1, y1, z1 = self._get_package_box(other_id, placement)
            candidates.update(((x1, y0, 0), (x0, y1, 0), (x1, 0, 0), (0, y1, 0), (x0, y0, 0), (x1, y0, z0), (x0, y1, z0)))
            if not self.package_map[other_id].isFragile:
                support_heights.append(z1)
                candidates.update(((x0, y0, z1), (x1 - dimensions.w, y0, z1), (x0, y1 - dimensions.l, z1)))

        for _ in range(max_candidates):
            candidates.add((rng.randint(0, max_x), rng.randint(0, max_y), rng.choice(support_heights)))

        valid = sorted((x, y, z) for x, y, z in candidates if 0 <= x <= max_x and 0 <= y <= max_y and 0 <= z <= max_z)
        rng.shuffle(valid)
        return [Coordinate(x, y, z) for x, y, z in valid[:max_candidates]]

    def _find_feasible_placement(self, state: State, package_id: str, truck_id: str, orientations: list[Orientation], rng: random.Random, max_positions: int = 32) -> State | None:
        """Kembalikan salinan state dengan paket ditempatkan, jika memungkinkan"""
        choices = orientations.copy()
        rng.shuffle(choices)
        for orientation in choices:
            coordinates = self._candidate_coordinates(state, package_id, truck_id, orientation, rng, max_positions)
            for coordinate in coordinates:
                candidate = self._move_package(state, package_id, truck_id, coordinate, orientation)
                if candidate is not None:
                    return candidate
        return None

    def generate_initial_state(self, rng: random.Random | None = None) -> State:
        """Buat random feasible state dengan mengisi truk satu paket demi satu paket"""
        rng = rng if rng is not None else random.Random()
        state = State({package.id: PackagePlacement(None, None, package.orientation) for package in self.packages})
        if not self.is_state_valid(state):
            raise ValueError("Cannot construct an initial state for this problem")

        package_ids = list(self.package_map)
        rng.shuffle(package_ids)
        for package_id in package_ids:
            # Sisakan sebagian paket di luar untuk variasi solusi awal.
            if rng.random() < 0.20:
                continue
            truck_ids = list(self.truck_map)
            rng.shuffle(truck_ids)
            for truck_id in truck_ids:
                candidate = self._find_feasible_placement(state, package_id, truck_id, Orientation.all_orientations(), rng)
                if candidate is not None:
                    state = candidate
                    break
        return state

    def _swap_packages(self, state: State, first_id: str, second_id: str) -> State | None:
        """Tukar lokasi dua paket tanpa menukar orientasi"""
        if first_id not in self.package_map or second_id not in self.package_map:
            raise ValueError("Unknown package ID")
        if first_id == second_id:
            return None
        first = state.placements[first_id]
        second = state.placements[second_id]
        if not first.is_inside and not second.is_inside:
            return None
        candidate = state.copy()
        candidate.placements[first_id] = PackagePlacement(second.truck_id, second.coordinate, first.orientation)
        candidate.placements[second_id] = PackagePlacement(first.truck_id, first.coordinate, second.orientation)
        return candidate if candidate != state and self.is_state_valid(candidate) else None

    def _move_package(self, state: State, package_id: str, truck_id: str | None, coordinate: Coordinate | None, orientation: Orientation | None = None) -> State | None:
        """Pindahkan paket. (None, None) = paket dikeluarkan dari truk"""
        if package_id not in self.package_map:
            raise ValueError("Unknown package ID")
        if (truck_id is None) != (coordinate is None):
            raise ValueError("truck_id and coordinate must both be set or both None")
        if truck_id is not None and truck_id not in self.truck_map:
            raise ValueError("Unknown truck ID")
        previous = state.placements[package_id]
        new_orientation = orientation if orientation is not None else previous.orientation
        candidate = state.copy()
        candidate.placements[package_id] = PackagePlacement(truck_id, coordinate, new_orientation)
        return candidate if candidate != state and self.is_state_valid(candidate) else None

    def _rotate_package(self, state: State, package_id: str, axis: str) -> State | None:
        """Putar paket 90 derajat di posisi yang sama, jika state hasilnya valid"""
        if package_id not in self.package_map:
            raise ValueError("Unknown package ID")
        previous = state.placements[package_id]
        if not previous.is_inside:
            return None
        new_orientation = previous.orientation.rotate(axis)
        dimension = self.package_map[package_id].dimension
        old_dims = previous.orientation.get_oriented_dimensions(dimension)
        new_dims = new_orientation.get_oriented_dimensions(dimension)
        if (old_dims.w, old_dims.l, old_dims.h) == (new_dims.w, new_dims.l, new_dims.h):
            return None  # Rotasi tidak mengubah geometri paket.
        candidate = state.copy()
        candidate.placements[package_id] = PackagePlacement(previous.truck_id, previous.coordinate, new_orientation)
        return candidate if self.is_state_valid(candidate) else None

    def generate_next_random_state(self, current_state: State, rng: random.Random | None = None, max_attempts: int = 80) -> State | None:
        """Sampel satu neighbor valid melalui swap, move, atau rotate. None = tidak menemukan neighbor valid"""
        if not self.is_state_valid(current_state):
            raise ValueError("Cannot generate a neighbor from an invalid state")
        if max_attempts <= 0:
            raise ValueError("max_attempts must be positive")
        rng = rng if rng is not None else random.Random()
        inside_ids = [pid for pid, p in current_state.placements.items() if p.is_inside]
        package_ids = list(self.package_map)

        for _ in range(max_attempts):
            operation = rng.choice(("swap", "move", "rotate"))

            if operation == "swap":
                if not inside_ids or len(package_ids) < 2:
                    continue
                first_id = rng.choice(inside_ids)
                second_id = rng.choice([pid for pid in package_ids if pid != first_id])
                candidate = self._swap_packages(current_state, first_id, second_id)

            elif operation == "move":
                if not package_ids:
                    continue
                package_id = rng.choice(package_ids)
                placement = current_state.placements[package_id]
                if placement.is_inside and rng.random() < 0.25:
                    candidate = self._move_package(current_state, package_id, None, None)
                elif self.truck_map:
                    truck_id = rng.choice(list(self.truck_map))
                    candidate = self._find_feasible_placement(current_state, package_id, truck_id, [placement.orientation], rng)
                else:
                    candidate = None

            else:  # rotate
                if not inside_ids:
                    continue
                candidate = self._rotate_package(current_state, rng.choice(inside_ids), rng.choice(("x", "y", "z")))

            if candidate is not None:
                return candidate
        return None

    def _generate_package_colors(self):
        color_table = {}
        num_packages = len(self.packages)
        
        if num_packages == 0:
            return color_table

        for i, package in enumerate(self.packages):
            hue = i / num_packages
            
            rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
            red, green, blue = int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
            
            color_table[package.id] = f"#{red:02x}{green:02x}{blue:02x}"
            
        return color_table