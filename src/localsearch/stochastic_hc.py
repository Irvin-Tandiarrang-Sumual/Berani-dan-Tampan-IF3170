import time
import math

from random import random

from localsearch.local_search import LocalSearch
from model.problem import Problem
from model.state import State
from localsearch.dto import SteepestSidewaysStochasticResult

class StochasticHC(LocalSearch):
    def __init__(self, problem : Problem):
        super().__init__(problem)

    def execute(self) -> SteepestSidewaysStochasticResult:
        result = SteepestSidewaysStochasticResult
        current_state = self.problem.generate_initial_state()
        result.initialState = current_state
        max_obj_value = self.problem.calculate_objective_value(current_state)
        best_state = current_state

        iteration = 0
        start = time.time()

        result.final_objective_value_result = -1
        
        is_terminate = False

        while(True): 
            current_state = self.problem.generate_next_random_state(best_state)
            current_objective_value = current_state.problem.calculate_objective_value(current_state)

            result.objective_values_history_per_iteration.append(current_objective_value)
            iteration += 1
            is_terminate = (current_objective_value<=max_obj_value)
            
            if (is_terminate):
                end = time.time()
                result.duration_seconds = (end - start)
                result.finalState = best_state
                result.num_of_iterations = iteration
                result.final_objective_value_result = max_obj_value
                return result
            else:
                best_state = current_state
                max_obj_value = current_objective_value