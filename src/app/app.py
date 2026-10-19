import argparse

from localsearch.local_search_factory import LocalSearchAlgorithmFactory
from reader.reader import Reader

class App:
    def __init__(self, args: list[str]):
        parser = argparse.ArgumentParser(description="Local Search Visualizer")
        parser.add_argument("algorithm", choices=["simulated_annealing", "genetic_algorithm"])
        parser.add_argument("input_file", help="JSON filename inside tests/")
        parser.add_argument("--population-size", type=int, default=20)
        parser.add_argument("--iterations", type=int, default=100)
        parser.add_argument("--seed", type=int, default=None)
        self.args = parser.parse_args(args[1:])

    def run(self):
        try:
            problem = Reader(self.args.input_file).load_problem()
        except FileNotFoundError:
            print(f"File {self.args.input_file} doesn't exist")
            print("Put your file inside the tests directory")
            return

        factory = LocalSearchAlgorithmFactory()
        try:
            if self.args.algorithm == "genetic_algorithm":
                localsearch = factory.getLocalSearchAlgorithm(
                    self.args.algorithm,
                    problem,
                    population_size=self.args.population_size,
                    max_iterations=self.args.iterations,
                    seed=self.args.seed,
                )
            else:
                localsearch = factory.getLocalSearchAlgorithm(self.args.algorithm, problem)
        except ValueError as exc:
            print(f"Invalid algorithm configuration: {exc}")
            return

        result = localsearch.execute()
        result.visualize(problem, 15, 12)
