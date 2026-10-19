from dataclasses import dataclass, field

from model.problem import Problem
from model.state import State


@dataclass
class ChartSeries:
    label: str
    values: list[float]
    x_values: list[int] | None = None
    color: str | None = None

    def __post_init__(self):
        if self.x_values is not None and len(self.x_values) != len(self.values):
            raise ValueError("x_values and values must have the same length")

    def get_x_values(self) -> list[int]:
        return self.x_values if self.x_values is not None else list(range(len(self.values)))


@dataclass
class ChartConfig:
    title: str
    x_label: str
    y_label: str
    series: list[ChartSeries] = field(default_factory=list)


@dataclass
class MetricConfig:
    label: str
    value: str | int | float
    unit: str = ""


@dataclass
class VisualizationData:
    algorithm_name: str
    problem: Problem
    initial_state: State
    final_state: State
    initial_objective_value: float
    final_objective_value: float
    duration_seconds: float
    charts: list[ChartConfig] = field(default_factory=list)
    metrics: list[MetricConfig] = field(default_factory=list)
    initial_state_label: str = "Initial State"
    final_state_label: str = "Final State"
    input_file: str | None = None
    run_label: str | None = None
