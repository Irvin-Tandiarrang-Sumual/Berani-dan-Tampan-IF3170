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
class SteepestSidewaysStochasticResult(LocalSearchResult):
    num_of_iterations : int
    
@dataclass
class RandomRestartResult(LocalSearchResult):
    num_of_restarts : int
    iterations_per_restarts : list[int]