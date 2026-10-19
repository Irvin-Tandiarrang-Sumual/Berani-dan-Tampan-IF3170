from localsearch.simulated_annealing import SimulatedAnnealing
from localsearch.local_search import LocalSearch
from model.problem import Problem

class LocalSearchAlgorithmFactory:
    def getLocalSearchAlgorithm(self, type : str, problem : Problem) -> LocalSearch:
        if type == "simulated_annealing":
            return SimulatedAnnealing(problem)
        else:
            raise ValueError()