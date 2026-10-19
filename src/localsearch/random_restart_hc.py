import time
import math

from random import random

from localsearch.local_search import LocalSearch
from model.problem import Problem
from model.state import State
from localsearch.dto import RandomRestartResult

# Asumsi Random Restart dilakukan dengan me-restart Steepest Ascent Hill Climbing berkali-kali, karena menurut sumber https://www.datacamp.com/tutorial/hill-climbing-algorithm-for-ai-in-python, saat memilih neighbor, hill climbing yang dilakukan BUKAN cek semua suksesor, melainkan cek hingga suksesor baru tidak lagi menghasilkan nilai yang lebih baik saja. 
# Asumsi ini berdasarkan salindia perkuliahan

class RandomRestartHC(LocalSearch):
    def __init__(self, problem : Problem, max_restart : int):
        super().__init__(problem)
        self.max_restart = max_restart

    def execute(self) -> RandomRestartResult:
        result = RandomRestartResult
        current_state = self.problem.generate_initial_state()
        result.initialState = current_state
        max_obj_value = self.problem.calculate_objective_value(current_state)
        best_state = current_state

        iteration = 0
        start = time.time()

        result.final_objective_value_result = -1
        
        num_of_restarts = 0
        
        is_restart = False

        while(True): 
            current_state = self.problem.generate_best_neighbor_state(best_state)
            current_objective_value = current_state.problem.calculate_objective_value(current_state)

            result.objective_values_history_per_iteration.append(current_objective_value)
            iteration += 1
            
            if (current_objective_value <= max_obj_value):
                is_restart = True
            
            if (is_restart and num_of_restarts <= self.max_restart):
                num_of_restarts += 1
                result.iterations_per_restarts.append(iteration)
                
                iteration = 0
                current_state = self.problem.generate_initial_state()
                result.initialState = current_state
                max_obj_value = self.problem.calculate_objective_value(current_state)
                best_state = current_state
            else:
                end = time.time()
                result.duration_seconds = (end - start)
                result.finalState = best_state
                result.final_objective_value_result = max_obj_value
                return result