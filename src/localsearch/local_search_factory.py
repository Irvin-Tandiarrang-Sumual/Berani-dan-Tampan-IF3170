from localsearch.simulated_annealing import SimulatedAnnealing
from localsearch.local_search import LocalSearch
from model.state import State

class LocalSearchAlgorithmFactory:
    def getLocalSearchAlgorithm(self, type : str, initialState : State) -> LocalSearch:
        if type == "simulated_annealing":
            return SimulatedAnnealing(initialState)
        else:
            raise ValueError()