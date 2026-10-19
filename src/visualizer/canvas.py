from model.state import State
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from dataclasses import dataclass
from model.state import PackagePlacement
from model.problem import Problem
from type.dimension import Dimension
import matplotlib.gridspec as gridspec

@dataclass
class GridLocation:
    row : int
    col : int

@dataclass
class ChartInput:
    numbers : list[float]
    title : str
    x_label :str
    y_label : str

class Canvas:
    def __init__(self, width : int, height : int,
                row : int, column : int,
                package_color_lookup_table : dict[str, str]):
        self.row = row
        self.column = column
        self.fig = plt.figure(width, height)
        self.gs = gridspec.GridSpec(row, column)
        self.package_color_lookup_table = package_color_lookup_table

    def write_algorithm_name(self, algorithm_name : str):
        plt.suptitle(algorithm_name)
    
    def draw_line_chart(self, chart_input : ChartInput, grid_location : GridLocation):
        ax = self.fig.add_subplot(self.gs[grid_location.row, grid_location.col])
        ax.plot(chart_input.numbers, marker = "o")
        ax.set_title(chart_input.title)
        ax.set_xlabel(chart_input.x_label)
        ax.set_ylabel(chart_input.y_label)

    def write_sidebar_note(self, note : str):
        ax = self.fig.add_subplot(self.gs[:, self.column - 1])
        ax.axis("off")
        ax.text(
            0.5, 0.5, note, fontsize = 12, va = "center", linespacing = 1.5
        )

    def write_bottom_note(self, note : str):
        ax = self.fig.add_subplot(self.gs[self.row - 1, :])
        ax.axis("off")
        ax.text(
            0.5, 0.5, note, fontsize = 12, va = "center", linespacing = 1.5
        )

    def write_top_right_note(self, note :str):
        ax = self.fig.add_subplot(self.gs[self.row - 1, self.column - 1])
        ax.axis("off")
        ax.text(
            0.5, 0.5, note, fontsize = 12, va = "center", linespacing = 1.5
        )

    def show():
        plt.tight_layout()
        plt.show()

    def visualize_state(self, problem : Problem, state : State, row_idx : int):
        packages_outside_truck_id = state.get_outside_package_ids()
        
        gs_sub = gridspec.GridSpecFromSubplotSpec(1, len(problem.trucks) + 1, subplot_spec=self.gs[1, :], wspace=0.5, hspace=0.5)

        inner_col_idx = 0
        for truck in problem.trucks:
            package_inside_truck_ids = state.get_inside_package_ids()
            ax_3d = self.fig.add_subplot(gs_sub[0, inner_col_idx], projection = "3d")
            self._draw_packages_in_truck(ax_3d, truck.id, package_inside_truck_ids, problem,
                                    state)
            inner_col_idx += 1

        ax_3d = self.fig.add_subplot(gs_sub[0, inner_col_idx], projection = "3d")
        self._draw_package_outside(ax_3d, problem, packages_outside_truck_id)

    def _draw_packages_in_truck(self, ax_3d : Axes3D, truck_id : str, inside_packages : list[str],
                        problem : Problem, state : State):

        for package_id in inside_packages:
            self._draw_package_inside(ax_3d,
                        problem.package_map[package_id].dimension,
                        package_id, state.placements[package_id])

    def _draw_package_inside(self, ax_3d : Axes3D, package_dimension : Dimension,
                package_id : str, package_placement : PackagePlacement):
        
        ax_3d.bar3d(x=package_placement.coordinate.x, y=package_placement.coordinate.y,
                z=package_placement.coordinate.z, dx=package_dimension.w,
                dy=package_dimension.l, dz=package_dimension.h,
                color=self.package_color_lookup_table[package_id], edgecolor='black', alpha=0.5)
        
    def _draw_packages_outside(self, ax_3d : Axes3D, problem : Problem,
                        outside_packages_id : list[str]):

        x_start_point = 0
        for package_id in outside_packages_id:
            self._draw_package_outside(ax_3d, problem.package_map[package_id].dimension, package_id,
                            x_start_point,)
            x_start_point += problem.package_map[package_id].dimension.l

    def _draw_package_outside(self, ax_3d : Axes3D, package_dimension : Dimension,
                package_id : str, x_start_point : int):
        
        ax_3d.bar3d(x=x_start_point, y=0,
                z=0, dx=package_dimension.w,
                dy=package_dimension.l, dz=package_dimension.h,
                color=self.package_color_lookup_table[package_id], edgecolor='black', alpha=0.5)