import random
import time
from copy import deepcopy

from localsearch.dto import GeneticAlgorithmResult
from localsearch.local_search import LocalSearch
from model.problem import Problem
from model.state import PackagePlacement, State
from type.orientation import Orientation


class GeneticAlgorithm(LocalSearch):
    MUTATION_RATE = 0.20

    def __init__(self, problem: Problem, population_size: int = 20, max_iterations: int = 100, seed: int | None = None):
        super().__init__(problem)
        if type(population_size) is not int or population_size < 2:
            raise ValueError("population_size must be an integer >= 2")
        if type(max_iterations) is not int or max_iterations < 0:
            raise ValueError("max_iterations must be a nonnegative integer")
        self.population_size = population_size
        self.max_iterations = max_iterations
        self.seed = seed

    def _fitness(self, individual: State) -> float:
        return self.problem.calculate_objective_value(individual)

    def _initialize_population(self, rng: random.Random) -> list[State]:
        return [self.problem.generate_initial_state(rng) for _ in range(self.population_size)]

    def _select_parent(self, population: list[State], fitnesses: list[float], rng: random.Random) -> State:
        minimum = min(fitnesses)
        weights = fitnesses if minimum >= 0 else [f - minimum for f in fitnesses]
        if sum(weights) <= 0:
            return rng.choice(population)
        return rng.choices(population, weights=weights, k=1)[0]

    def _repair_placements(self, genes: dict[str, PackagePlacement], rng: random.Random) -> State:
        state = State({
            package.id: PackagePlacement(None, None, genes[package.id].orientation)
            for package in self.problem.packages
        })
        inherited_inside = [(package_id, placement) for package_id, placement in genes.items() if placement.is_inside]
        inherited_inside.sort(key=lambda item: (item[1].coordinate.z, -self.problem.package_map[item[0]].value, item[0]))

        for package_id, placement in inherited_inside:
            coordinate = deepcopy(placement.coordinate)
            candidate = self.problem._move_package(state, package_id, placement.truck_id, coordinate, placement.orientation)
            if candidate is None:
                candidate = self.problem._find_feasible_placement(state, package_id, placement.truck_id, [placement.orientation], rng)
            if candidate is not None:
                state = candidate
        return state

    def _crossover(self, first: State, second: State, rng: random.Random) -> State:
        package_ids = list(self.problem.package_map)
        if len(package_ids) < 2:
            return first.copy() if rng.random() < 0.5 else second.copy()
        crossover_point = rng.randint(1, len(package_ids) - 1)
        genes = {
            package_id: deepcopy(first.placements[package_id] if index < crossover_point else second.placements[package_id])
            for index, package_id in enumerate(package_ids)
        }
        return self._repair_placements(genes, rng)

    def _mutate(self, individual: State, rng: random.Random) -> State:
        candidate = self.problem.generate_next_random_state(individual, rng)
        return candidate if candidate is not None else individual.copy()

    def execute(self) -> GeneticAlgorithmResult:
        rng = random.Random(self.seed)
        start = time.perf_counter()
        population = self._initialize_population(rng)
        initial_population = [state.copy() for state in population]
        fitnesses = [self._fitness(state) for state in population]

        initial_best_index = max(range(len(population)), key=lambda i: fitnesses[i])
        initial_state = population[initial_best_index].copy()
        best_state = initial_state.copy()
        best_fitness = fitnesses[initial_best_index]
        max_history = [max(fitnesses)]
        avg_history = [sum(fitnesses) / len(fitnesses)]

        for _ in range(self.max_iterations):
            new_population = []

            while len(new_population) < self.population_size:
                parent_a = self._select_parent(population, fitnesses, rng)
                parent_b = self._select_parent(population, fitnesses, rng)
                offspring = self._crossover(parent_a, parent_b, rng)
                if rng.random() < self.MUTATION_RATE:
                    offspring = self._mutate(offspring, rng)
                new_population.append(offspring)

            population = new_population
            fitnesses = [self._fitness(state) for state in population]
            generation_best_index = max(range(len(population)), key=lambda i: fitnesses[i])
            if fitnesses[generation_best_index] > best_fitness:
                best_fitness = fitnesses[generation_best_index]
                best_state = population[generation_best_index].copy()
            max_history.append(max(fitnesses))
            avg_history.append(sum(fitnesses) / len(fitnesses))

        return GeneticAlgorithmResult(
            initialState=initial_state,
            finalState=best_state,
            objective_values_history_per_iteration=max_history.copy(),
            final_objective_value_result=best_fitness,
            duration_seconds=time.perf_counter() - start,
            population_size=self.population_size,
            max_iterations=self.max_iterations,
            max_fitness_history=max_history,
            avg_fitness_history=avg_history,
            initial_population=initial_population,
            final_population=[state.copy() for state in population],
            seed=self.seed
        )