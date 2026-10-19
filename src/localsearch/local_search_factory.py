from localsearch.simulated_annealing import SimulatedAnnealing
from localsearch.steepest_sideways_hc import SteepestSideways
from localsearch.local_search import LocalSearch
from model.state import Problem

class LocalSearchAlgorithmFactory:
    def getLocalSearchAlgorithm(self, type : str, problem : Problem) -> LocalSearch:
        if type == "simulated_annealing":
            return SimulatedAnnealing(problem)
        elif type == "steepest":
            return SteepestSideways(problem)
        elif type == 'sideways':
            while (True):
                max_side_move = input('Input maximum sideways move: ')
                if max_side_move:
                    break
                print('Input invalid!')
            return SteepestSideways(problem, max_side_move)
        else:
            raise ValueError()