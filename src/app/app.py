from localsearch.local_search_factory import LocalSearchAlgorithmFactory
from reader.reader import Reader

class App:
    def __init__(self, args : list[str]):
        self.algorithm = args[1]
        self.inputFile = args[2]

    def run(self):
        try:
            reader = Reader(self.inputFile)
            problem = reader.loadState()
        except FileNotFoundError:
            print(f"File {self.inputFile} doesn't exist")
            print(f"Put your file inside the tests directory")
            return
        
        localSearchFactory = LocalSearchAlgorithmFactory()
        try:
            localsearch = localSearchFactory.getLocalSearchAlgorithm(self.algorithm, problem)
        except ValueError:
            print(f"Selected algorithm {self.algorithm} doesn't exist")
            return

        result = localsearch.execute()

        result.visualize()
