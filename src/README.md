# IF3170_G10_BeraniDanTampan

## Usage
Template:
`python main.py <algorithm_type> <input_filename>`

Example:
`python main.py simulated_annealing dummy-data-example.json`

Notes :
- `algorithm_type` : the types are listed on the `local_search_factory.py`, to add new type just add another in the if-else branch
- `input_filename` : currently all the input must be on the `tests` directory to be detected

State(
    placements = {
        "Package-1": PackagePlacement(...),
        "Package-2": PackagePlacement(...),
        "Package-3": PackagePlacement(...)
    }
)

PackagePlacement(
    truck_id="Truck-1",
    coordinate=Coordinate(0, 0, 0),
    orientation=Orientation("x", "y", "z")
)

dalam:
PackagePlacement(
    truck_id="Truck-1",
    coordinate=Coordinate(0, 0, 0),
    orientation=Orientation("x", "y", "z")
)

luar:
PackagePlacement(
    truck_id=None,
    coordinate=None,
    orientation=Orientation("x", "y", "z")
)