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

        while(True): # buka loop kalau ternyata butuh 1 iterasi saja
            current_objective_value = self.problem.calculate_objective_value(current_state)
            
            generate_neighbour_ctr = 0 # in case needed to check is_all_neighbour
            max_neighbour_obj_value = current_objective_value
            max_neighbour_state = current_state
            current_neighbour = current_state
            
            while (True):
                current_neighbour_objective_value = 0
                # generate next neighbour
                
                # nanti diganti dengan obj valuenya
                if current_neighbour_objective_value > max_neighbour_obj_value:
                    max_neighbour_obj_value = current_neighbour_objective_value
                    max_neighbour_state = current_neighbour

                if (self._is_all_neighbour()):
                    break
            
            if (self._is_peak_or_flat(max_obj_value, max_neighbour_obj_value)):
                best_state = max_neighbour_state
                max_obj_value = max_neighbour_obj_value
                return result
            
            if (self._is_reached_max_iter(iteration, self.maxIteration)):
                # cek lagi ini dibutuhkan atau ngga nanti
                end = time.time()
                result.duration_seconds = (end - start)
                return result
            
            next_state = self.problem.generate_next_state(current_state)
            next_objective_value= self.problem.calculate_objective_value(next_state)

            current_state = next_state
            result.objective_values_history_per_iteration.append(current_objective_value)
            iteration += 1

    
    def _is_reached_max_iter(self, nowIter, maxIter: int):
        return nowIter>=maxIter
    
    def _is_all_neighbour(self):
        return True
    
    def _is_peak_or_flat(self, oldVal, newVal: int):
        return newVal >= oldVal
    
    def _is_terminate(self, nowIter, maxIter, oldVal, newVal: int):
        return self._is_reached_max_iter(nowIter, maxIter) or self._is_peak_or_flat(oldVal, newVal)
    
    