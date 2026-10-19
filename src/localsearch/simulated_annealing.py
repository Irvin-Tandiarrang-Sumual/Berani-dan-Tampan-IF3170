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
                minTemperature : float = 0.1,
                maxIteration : int = 100):
        super().__init__(problem)

        self.temperature = temperature
        self.minTemperature = minTemperature
        self.maxIteration = maxIteration

    def execute(self) -> SimulatedAnnealingResult:
        result = SimulatedAnnealingResult()

        current_state = self.problem.generate_initial_state()
        result.initial_state = current_state

        iteration = 0
        start = time.time()

        result.final_objective_value_result = -1

        while(True):
            self._exponential_cooling(iteration)

            if self._is_stop_condition(iteration):
                end = time.time()
                result.duration_seconds = (end - start)
                return result

            current_objective_value = self.problem.calculate_objective_value(current_state)

            if self._is_new_best_objective_value(result.final_objective_value_result, current_objective_value):
                result.final_objective_value_result = current_objective_value
                result.final_state = current_state

            next_state = self.problem.generate_next_random_state(current_state)
            next_objective_value= self.problem.calculate_objective_value(next_state)

            objective_value_difference = next_objective_value - current_objective_value

            acceptance_probability = 1.0
            if self._is_move_to_better(objective_value_difference):
                current_state = next_state
            else:
                acceptance_probability = self._calculate_acceptance_probability(objective_value_difference)
                if self._is_worse_accepted(acceptance_probability):
                    current_state = next_state
                else:
                    result.stuck_frequency += 1

            result.objective_values_history_per_iteration.append(current_objective_value)
            result.acceptance_history_per_iteration.append(acceptance_probability)
            iteration += 1

    def _is_move_to_better(self, objective_value_difference : float):
        return objective_value_difference >= 0

    def _is_stop_condition(self, iteration) -> bool:
        return self.temperature < self.minTemperature and iteration < self.maxIteration

    def _exponential_cooling(self, iteration : int, alpha = 0.95):
        self.temperature = self.temperature * (alpha ** iteration)

    def _calculate_acceptance_probability(self, objective_value_difference: float) -> float:
        return math.exp(- objective_value_difference / self.temperature)

    def _is_worse_accepted(self, acceptance_probability : float) -> bool:
        return acceptance_probability < random()

    def _is_new_best_objective_value(self, best_objective_value : float, new_objective_value : float) -> bool:
        return best_objective_value < new_objective_value