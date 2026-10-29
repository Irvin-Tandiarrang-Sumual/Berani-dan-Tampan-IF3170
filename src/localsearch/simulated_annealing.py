import time
import math

from random import random

from localsearch.local_search import LocalSearch
from model.problem import Problem
from localsearch.dto import SimulatedAnnealingResult

# Reference
## Exponential Cooling for Temperature Reference : https://algorithmafternoon.com/books/simulated_annealing/chapter02/

class SimulatedAnnealing(LocalSearch):
    def __init__(self, problem : Problem,
                temperature : float = 100,
                min_temperature : float = 0.1,
                alpha : float = 0.95,
                max_iteration : int = 100):
        super().__init__(problem)
        
        self.temperature = temperature
        self.min_temperature = min_temperature
        self.max_iteration = max_iteration
        self.alpha = alpha

    def execute(self) -> SimulatedAnnealingResult:
        result = SimulatedAnnealingResult()

        current_state = self.problem.generate_initial_state()
        current_objective_value = self.problem.calculate_objective_value(current_state)

        result.initial_state = current_state.copy()

        result.final_state = current_state.copy()
        result.final_objective_value_result = current_objective_value

        iteration = 0
        stuck_count = 0
        start = time.time()

        while(self._is_running(iteration)):
            next_state = self.problem.generate_next_random_state(current_state)
            next_objective_value= self.problem.calculate_objective_value(next_state)

            objective_value_difference = next_objective_value - current_objective_value

            acceptance_probability = 1.0
            if self._is_move_to_better(objective_value_difference):
                current_state = next_state
                current_objective_value = next_objective_value
            else:
                acceptance_probability = self._calculate_acceptance_probability(objective_value_difference)
                if self._is_worse_accepted(acceptance_probability):
                    current_state = next_state
                    current_objective_value = next_objective_value
                else:
                    stuck_count += 1

            if self._is_new_best_objective_value(result.final_objective_value_result, current_objective_value):
                result.final_objective_value_result = current_objective_value
                result.final_state = current_state.copy()

            result.objective_values_history_per_iteration.append(current_objective_value)
            result.acceptance_history_per_iteration.append(acceptance_probability)
            iteration += 1
            self._exponential_cooling()

        end = time.time()
        result.duration_seconds = (end - start)
        result.stuck_frequency = stuck_count / iteration if iteration > 0 else 0.0
        return result

    def _is_move_to_better(self, objective_value_difference : float):
        return objective_value_difference >= 0

    def _is_running(self, iteration) -> bool:
        return self.temperature >= self.min_temperature and iteration < self.max_iteration

    def _exponential_cooling(self):
        self.temperature *= self.alpha

    def _calculate_acceptance_probability(self, objective_value_difference: float) -> float:
        return math.exp(objective_value_difference / self.temperature)

    def _is_worse_accepted(self, acceptance_probability : float) -> bool:
        return acceptance_probability > random()

    def _is_new_best_objective_value(self, best_objective_value : float, new_objective_value : float) -> bool:
        return best_objective_value < new_objective_value