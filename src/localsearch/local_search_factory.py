from localsearch.simulated_annealing import SimulatedAnnealing
from localsearch.steepest_sideways_hc import SteepestSidewaysHC
from localsearch.random_restart_hc import RandomRestartHC
from localsearch.stochastic_hc import StochasticHC
from localsearch.local_search import LocalSearch
from model.state import Problem

class LocalSearchAlgorithmFactory:
    def getLocalSearchAlgorithm(self, type : str, problem : Problem) -> LocalSearch:
        if type == "simulated_annealing":
            return SimulatedAnnealing(problem)
        elif type == "steepest":
            return SteepestSidewaysHC(problem)
        elif type == 'sideways':
            while (True):
                try:
                    max_side_move = int(input('Input maximum sideways move: '))
                except ValueError:
                    print('Input invalid! Coba lagi!')
                if max_side_move < 0:
                    break
                print('Input harus >= 0!')
            return SteepestSidewaysHC(problem, max_side_move)
        elif type == 'random_restart':
            while (True):
                try:
                    max_restart = int(input('Input maximum sideways move: '))
                except ValueError:
                    print('Input invalid! Coba lagi!')
                if max_restart < 0:
                    break
                print('Input harus >= 0. Coba lagi!')
            return RandomRestartHC(problem, max_restart)
        elif type == 'stochastic':
            return StochasticHC(problem)
        else:
            raise ValueError()