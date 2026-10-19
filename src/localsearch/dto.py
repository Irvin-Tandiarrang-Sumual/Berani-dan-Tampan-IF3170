from dataclasses import dataclass
from model.state import State
from abc import ABC, abstractmethod
from visualizer.canvas import ChartInput
from visualizer.canvas import GridLocation
from visualizer.canvas import Canvas

@dataclass
class LocalSearchResult(ABC):
    initial_state : State
    final_state : State
    objective_values_history_per_iteration: list[float]
    final_objective_value_result : float
    duration_seconds : float

    @abstractmethod
    def visualize(self, width : int = 10, height : int = 8):
        pass

@dataclass
class SimulatedAnnealingResult(LocalSearchResult):
    algorith_name : str = "Simulated Annealing"
    acceptance_history_per_iteration : list[float]
    stuck_frequency : int

    def visualize(self, width : int, height : int):
        canvas = Canvas(width, height, 3, 2)
        
        canvas.write_algorithm_name(self.algorith_name)
        canvas.visualize_state(self.initial_state, "Initial State",
                            GridLocation(0, 0))
        canvas.visualize_state(self.final_state, "Final State",
                            GridLocation(0, 1))
        canvas.draw_line_chart(ChartInput(self.objective_values_history_per_iteration,
                                    "Objective Values per Iteration", "Iteration", "Objective values"),
                                    GridLocation(1,0))
        canvas.draw_line_chart(ChartInput(self.acceptance_history_per_iteration,
                                    "Acceptance History per Iteration", "Iteration", "Acceptance"),
                                    GridLocation(1,1))
        canvas.write_sidebar_note(f"""Final Objective Value = {self.final_objective_value_result}\n
                                            Duration (in seconds) = {self.duration_seconds}\n
                                            Stuck Frequency = {self.stuck_frequency}\n""")
        canvas.show()