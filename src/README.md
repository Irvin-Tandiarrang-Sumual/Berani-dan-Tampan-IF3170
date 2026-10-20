# IF3170_G10_BeraniDanTampan

## Usage
Template:
`python main.py <algorithm_type> <input_filename>`

Example (dari `root`):

`python main.py simulated_annealing dummy-data-example.json`

Opsi lain menjalankan Simulated Annealing:
`python main.py simulated_annealing dummy-data-example.json --temperature 100 --alpha 0.95 --min_temperature 0.1 --max_iterations 100`

Opsi lain menjalankan Genetic Algorithm
`python main.py genetic_algorithm dummy-data-example.json --population_size 20 --max_iterations 100 --seed 42`

Opsi menjalankan Sideways Algorithm
`python main.py sideways dummy-data-example.json`

Opsi menjalankan Random Restart Algorithm
`python main.py random_restart dummy-data-example.json`

Opsi menjalankan Stochastic Hill Climbing Algorithm
`python main.py stochastic dummy-data-example.json`

Opsi menjalankan Steepest Ascent Hill Climbing Algorithm
`python main.py steepest dummy-data-example.json`

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