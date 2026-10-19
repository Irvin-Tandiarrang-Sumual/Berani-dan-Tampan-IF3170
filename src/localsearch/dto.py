from dataclasses import dataclass, field
from model.state import State
from abc import ABC, abstractmethod
from visualizer.canvas import ChartInput
from visualizer.canvas import GridLocation
from visualizer.canvas import Canvas
from model.problem import Problem
from typing import Optional
@dataclass
class LocalSearchResult(ABC):
    initial_state : Optional[State] = None
    final_state : Optional[State] = None
    objective_values_history_per_iteration: list[float] = field(default_factory=list)
    final_objective_value_result : Optional[float] = field(default_factory=list)
    duration_seconds : float = 0

    @abstractmethod
    def visualize(self, width : int = 10, height : int = 8):
        pass

@dataclass
class SimulatedAnnealingResult(LocalSearchResult):
    algorithm_name : str = "Simulated Annealing"
    acceptance_history_per_iteration: list = field(default_factory=list)
    stuck_frequency : int = 0

    def visualize(self, problem: Problem, width: int, height: int):
        canvas = Canvas(width, height, 3, 2, problem.package_colors)
        canvas.write_algorithm_name(self.algorithm_name)

        canvas.visualize_state(problem, self.initial_state, "Initial State", 0)
        canvas.visualize_state(problem, self.final_state, "Final State", 1)

        canvas.draw_line_chart(
            ChartInput(self.objective_values_history_per_iteration, "Objective Values per Iteration", "Iteration", "Objective Value"),
            GridLocation(1, 0)
        )

        canvas.draw_line_chart(
            ChartInput(self.acceptance_history_per_iteration, "Acceptance History per Iteration", "Iteration", "Acceptance"),
            GridLocation(1, 1)
        )

        canvas.write_bottom_note(
            f"Final Objective Value: {self.final_objective_value_result}    |    "
            f"Duration: {self.duration_seconds:.3f} s    |    "
            f"Stuck Frequency: {self.stuck_frequency}"
        )
        canvas.show()