from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from model.problem import Problem
from model.state import State
from visualizer.canvas import Canvas
from visualizer.visualization_data import (ChartConfig, ChartSeries, MetricConfig, VisualizationData)


@dataclass
class LocalSearchResult(ABC):
    initial_state: State | None = None
    final_state: State | None = None
    objective_values_history_per_iteration: list[float] = field(default_factory=list)
    final_objective_value_result: float | None = None
    duration_seconds: float = 0.0

    @abstractmethod
    def _get_charts(self) -> list[ChartConfig]:
        pass

    @abstractmethod
    def _get_extra_metrics(self) -> list[MetricConfig]:
        pass

    def _get_state_labels(self) -> tuple[str, str]:
        return "Initial State", "Final State"

    def _get_populations(self) -> tuple[list[State] | None, list[State] | None]:
        return None, None

    def to_visualization_data(self, problem: Problem) -> VisualizationData:
        if self.initial_state is None or self.final_state is None:
            raise ValueError("Initial and final states must be available for visualization")

        initial_label, final_label = self._get_state_labels()
        initial_population, final_population = self._get_populations()
        final_value = problem.calculate_objective_value(self.final_state)

        metrics = [
            MetricConfig("Final Objective Value", final_value),
            MetricConfig("Duration", f"{self.duration_seconds:.3f}", "s"),
            *self._get_extra_metrics(),
        ]

        return VisualizationData(
            algorithm_name=self.algorithm_name,
            problem=problem,
            initial_state=self.initial_state,
            final_state=self.final_state,
            initial_objective_value=problem.calculate_objective_value(self.initial_state),
            final_objective_value=final_value,
            duration_seconds=self.duration_seconds,
            charts=self._get_charts(),
            metrics=metrics,
            initial_state_label=initial_label,
            final_state_label=final_label,
            initial_population=initial_population,
            final_population=final_population,
        )

    def visualize(self, problem: Problem, width: int = 15, height: int = 12) -> None:
        data = self.to_visualization_data(problem)
        canvas = Canvas(width, height, 3, 2, problem.package_colors)
        canvas.write_algorithm_name(data.algorithm_name)
        canvas.visualize_state(problem, data.initial_state, data.initial_state_label, 0, data.initial_population)
        canvas.visualize_state(problem, data.final_state, data.final_state_label, 1, data.final_population)
        canvas.draw_charts(data.charts)
        canvas.draw_metrics(data.metrics)
        canvas.show()


@dataclass
class SimulatedAnnealingResult(LocalSearchResult):
    algorithm_name : str = "Simulated Annealing"
    acceptance_history_per_iteration: list[float] = field(default_factory=list)
    stuck_frequency : float = 0.0

    def _get_charts(self) -> list[ChartConfig]:
        return [
            ChartConfig(
                "Objective Values per Iteration", "Iteration", "Objective Value",
                [ChartSeries("Objective Value", self.objective_values_history_per_iteration)],
            ),
            ChartConfig(
                "Acceptance Probability per Iteration", "Iteration", "Probability",
                [ChartSeries("Acceptance Probability", self.acceptance_history_per_iteration)],
            ),
        ]

    def _get_extra_metrics(self) -> list[MetricConfig]:
        return [MetricConfig("Stuck Frequency", self.stuck_frequency)]


@dataclass
class GeneticAlgorithmResult(LocalSearchResult):
    algorithm_name: str = "Genetic Algorithm"
    population_size: int = 20
    max_iterations: int = 100
    max_fitness_history: list[float] = field(default_factory=list)
    avg_fitness_history: list[float] = field(default_factory=list)
    initial_population: list[State] = field(default_factory=list)
    final_population: list[State] = field(default_factory=list)
    seed: int | None = None
    best_ever_state: State | None = None
    best_ever_fitness: float | None = None
    problem: Problem | None = None

    def _get_state_labels(self) -> tuple[str, str]:
        return "Initial State", "Final State"

    def _get_populations(self) -> tuple[list[State], list[State]]:
        return self.initial_population, self.final_population

    def _get_charts(self) -> list[ChartConfig]:
        return [
            ChartConfig(
                "Objective Values per Iteration", "Iteration", "Objective Value",
                [
                    ChartSeries("Maximum", self.max_fitness_history),
                    ChartSeries("Average", self.avg_fitness_history),
                ],
            )
        ]

    def _get_extra_metrics(self) -> list[MetricConfig]:
        return [
            MetricConfig("Population Size", self.population_size),
            MetricConfig("Iterations", self.max_iterations),
        ]

@dataclass
class SteepestSidewaysResult(LocalSearchResult):
    num_of_iterations : int
