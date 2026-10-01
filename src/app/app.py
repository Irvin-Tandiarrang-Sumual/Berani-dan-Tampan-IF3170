from localsearch.local_search_factory import LocalSearchAlgorithmFactory
from reader.reader import Reader
from visualizer.visualizer import Visualizer

class App:
    def __init__(self, args : list[str]):
        self.algorithm = args[1]
        self.inputFile = args[2]

    def run(self):
        try:
            reader = Reader(self.inputFile)
            initialState = reader.loadState()
        except FileNotFoundError:
            print(f"File {self.inputFile} doesn't exist")
            print(f"Put your file inside the tests directory")
            return
        
        localSearchFactory = LocalSearchAlgorithmFactory()
        try:
            localsearch = localSearchFactory.getLocalSearchAlgorithm(self.algorithm, initialState)
        except ValueError:
            print(f"Selected algorithm {self.algorithm} doesn't exist")
            return

        states = localsearch.execute()

        # visualizer = Visualizer(states)
        # visualizer.visualize()
