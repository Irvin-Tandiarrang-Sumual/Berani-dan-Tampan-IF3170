from localsearch.genetic_algorithm import GeneticAlgorithm
from localsearch.simulated_annealing import SimulatedAnnealing
from localsearch.genetic_algorithm import GeneticAlgorithm
from localsearch.steepest_sideways_hc import SteepestSideways
from localsearch.local_search import LocalSearch
from model.problem import Problem

class LocalSearchAlgorithmFactory:
    def getLocalSearchAlgorithm(self, type : str, problem : Problem, **kwargs) -> LocalSearch:
        if type == "simulated_annealing":
            sa_input = {"problem": problem}
            
            if "temperature" in kwargs:
                sa_input["temperature"] = kwargs["temperature"]
            if "min_temperature" in kwargs:
                sa_input["min_temperature"] = kwargs["min_temperature"]
            if "alpha" in kwargs:
                sa_input["alpha"] = kwargs["alpha"]
            if "max_iteration" in kwargs:
                sa_input["max_iteration"] = kwargs["max_iteration"]
                
            return SimulatedAnnealing(**sa_input)

        elif type == "genetic_algorithm":
            ga_input = {"problem": problem}
            

            if "population_size" in kwargs:
                ga_input["population_size"] = kwargs["population_size"]
                
            if "max_iterations" in kwargs:
                ga_input["max_iterations"] = kwargs["max_iterations"]
                
            if "seed" in kwargs:
                ga_input["seed"] = kwargs["seed"]
                
            return GeneticAlgorithm(**ga_input)

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