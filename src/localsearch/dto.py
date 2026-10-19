from dataclasses import dataclass
from model.state import State

@dataclass
class LocalSearchResult:
    initialState : State
    finalState : State
    objective_values_history_per_iteration: list[float]
    final_objective_value_result : float
    duration_seconds : float

@dataclass
class SimulatedAnnealingResult(LocalSearchResult):
    acceptance_history_per_iteration : list[float]
    stuck_frequency : int
    
@dataclass
class SteepestSidewaysResult(LocalSearchResult):
    num_of_iterations : int