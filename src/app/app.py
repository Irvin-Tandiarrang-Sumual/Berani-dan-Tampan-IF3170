import argparse

from localsearch.local_search_factory import LocalSearchAlgorithmFactory
from reader.reader import Reader

class App:
    def __init__(self, args : list[str]):
        self.algorithm = args[1]
        self.inputFile = args[2]

        self.kwargs = self._construct_kwargs(args[3:])

    def run(self):
        try:
            problem = Reader(self.args.input_file).load_problem()
        except FileNotFoundError:
            print(f"File {self.args.input_file} doesn't exist")
            print("Put your file inside the tests directory")
            return

        try:
            localsearch = LocalSearchAlgorithmFactory.getLocalSearchAlgorithm(self.algorithm, problem, **self.kwargs)
        except ValueError:
            print(f"Selected algorithm {self.algorithm} doesn't exist")
            return

        result = localsearch.execute()
        result.visualize(problem, 15, 12)

    def _construct_kwargs(self, optional_args : list[str]):
        kw = {}
        for i in range(0, len(optional_args), 2):
            if i + 1 < len(optional_args) and optional_args[i].startswith('--'):
                key = optional_args[i].lstrip('-')
                value_in_str = optional_args[i + 1]
                
                try:
                    if '.' in value_in_str:
                        value = float(value_in_str)
                    else:
                        value = int(value_in_str)
                except ValueError:
                    value = value_in_str
                kw[key] = value
        return kw
