import time
import math

from random import random

from localsearch.local_search import LocalSearch
from model.problem import Problem
from model.state import State
from dto import SteepestAscentResult


class SteepestAscent(LocalSearch):
    def __init__(self, problem : Problem, maxIteration, maxNeighbour : int):
        super().__init__(problem)
        self.maxIteration = maxIteration
        self.maxNeighbour = maxNeighbour


    def execute(self) -> SteepestAscentResult:
        result = SteepestAscentResult
        current_state = self.problem.generate_initial_state()
        result.initialState = current_state
        max_obj_value = self.problem.calculate_objective_value(current_state)
        best_state = current_state

        iteration = 0
        start = time.time()

        result.final_objective_value_result = -1

        while(True): 
            current_state = self.problem.generate_best_neighbor_state(best_state)
            current_objective_value = current_state.problem.calculate_objective_value(current_state)
            
            if (self._is_terminate(max_obj_value, current_objective_value)):
                best_state = current_state
                max_obj_value = current_objective_value
            else:
                end = time.time()
                result.duration_seconds = (end - start)
                result.finalState = best_state
                result.num_of_iterations = iteration
                result.final_objective_value_result = max_obj_value
                return result

            result.objective_values_history_per_iteration.append(current_objective_value)
            iteration += 1
            
    
    def _is_reached_max_iter(self, nowIter, maxIter: int):
        return nowIter>=maxIter
    
    def _is_all_neighbour(self):
        return True
    
    def _is_terminate(self, oldVal, newVal: int):
        return oldVal > newVal
    
    
    