import time
import math

from random import random

from localsearch.local_search import LocalSearch
from model.problem import Problem
from model.state import State
from localsearch.dto import SidewaysResult


class SidewaysHC(LocalSearch):
    def __init__(self, problem : Problem, max_side_move : int = 5):
        super().__init__(problem)
        self.max_side_move = max_side_move

    def execute(self) -> SidewaysResult:
        result = SidewaysResult()
        current_state = self.problem.generate_initial_state()
        result.initial_state = current_state.copy()
        max_obj_value = self.problem.calculate_objective_value(current_state)
        best_state = current_state

        iteration = 0
        start = time.time()

        result.final_objective_value_result = -1
        result.objective_values_history_per_iteration.append(max_obj_value)
        is_terminate = False
        
        side_move = 0

        while(True): 
            current_state = self.problem.generate_best_neighbor_state(best_state)
            current_objective_value = self.problem.calculate_objective_value(current_state)

            result.objective_values_history_per_iteration.append(current_objective_value)
            iteration += 1
            
            if current_objective_value == max_obj_value:
                side_move += 1
                is_terminate = (current_objective_value<max_obj_value) or (current_objective_value == max_obj_value and side_move <= self.max_side_move)
            
            if (is_terminate):
                end = time.time()
                result.duration_seconds = (end - start)
                result.final_state = best_state
                result.num_of_iterations = iteration
                result.final_objective_value_result = max_obj_value
                return result
            else:
                best_state = current_state
                max_obj_value = current_objective_value