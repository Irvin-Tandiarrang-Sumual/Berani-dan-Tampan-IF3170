from localsearch.genetic_algorithm import GeneticAlgorithm
from localsearch.simulated_annealing import SimulatedAnnealing
from localsearch.local_search import LocalSearch
from model.problem import Problem

class LocalSearchAlgorithmFactory:
    def getLocalSearchAlgorithm(self, type: str, problem: Problem, **kwargs) -> LocalSearch:
        if type == "simulated_annealing":
            return SimulatedAnnealing(problem)
        if type == "genetic_algorithm":
            return GeneticAlgorithm(problem, **kwargs)
        raise ValueError(f"Unknown algorithm: {type}")
