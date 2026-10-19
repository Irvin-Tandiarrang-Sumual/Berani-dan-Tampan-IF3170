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
    def __init__(self, width: int, height: int,
             row: int, column: int,
             package_color_lookup_table: dict[str, str]):
        self.row = row
        self.column = column
        self.fig = plt.figure(figsize=(width, height))
        self.gs = gridspec.GridSpec(
            row, column, figure=self.fig,
            height_ratios=[5, 2.2, 0.8],
            left=0.06, right=0.96, top=0.92, bottom=0.05,
            hspace=0.48, wspace=0.28
        )
        self.package_color_lookup_table = package_color_lookup_table

    def write_algorithm_name(self, algorithm_name: str):
        self.fig.suptitle(algorithm_name, fontsize=16, fontweight="bold", y=0.975)
    
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

    def write_bottom_note(self, note: str):
        ax = self.fig.add_subplot(self.gs[2, :])
        ax.axis("off")
        ax.text(0.5, 0.5, note, ha="center", va="center", fontsize=10, linespacing=1.4, transform=ax.transAxes)

    def write_top_right_note(self, note :str):
        ax = self.fig.add_subplot(self.gs[self.row - 1, self.column - 1])
        ax.axis("off")
        ax.text(
            0.5, 0.5, note, fontsize = 12, va = "center", linespacing = 1.5
        )

    def show(self):
        plt.show()

    def visualize_state(self, problem: Problem, state: State,
                        title: str, column_idx: int):
        # Initial State di kiri, Final State di kanan
        panel = gridspec.GridSpecFromSubplotSpec(
            4, 1, subplot_spec=self.gs[0, column_idx],
            height_ratios=[0.3, 3.2, 1.4, 0.4],
            hspace=0.25
        )

        # Judul state
        ax_title = self.fig.add_subplot(panel[0])
        ax_title.axis("off")
        ax_title.text(0.5, 0.5, title, ha="center", va="center", fontsize=13, fontweight="bold")

        # Visualisasi truk
        trucks_grid = gridspec.GridSpecFromSubplotSpec(1, len(problem.trucks), subplot_spec=panel[1], wspace=0.25)

        for i, truck in enumerate(problem.trucks):
            ax = self.fig.add_subplot(trucks_grid[0, i], projection="3d")
            ax.set_title(str(truck.id), fontsize=9)
            self._draw_packages_in_truck(
                ax, truck.id, state.get_inside_package_ids(truck.id),
                problem, state
            )

        # Paket di luar truk
        ax_outside = self.fig.add_subplot(panel[2])
        self._draw_packages_outside(ax_outside, problem, state.get_outside_package_ids())

        # Total objective value state
        ax_value = self.fig.add_subplot(panel[3])
        ax_value.axis("off")
        value = problem.calculate_objective_value(state)
        ax_value.text(0.5, 0.5, f"State Value: {value}", ha="center", va="center", fontsize=11, fontweight="bold")

    def _draw_packages_in_truck(self, ax_3d: Axes3D, truck_id: str, inside_packages: list[str], problem: Problem, state: State):
        dim = problem.truck_map[truck_id].dimension
        w, l, h = dim.w, dim.l, dim.h

        for package_id in inside_packages:
            placement = state.placements[package_id]
            size = placement.orientation.get_oriented_dimensions(problem.package_map[package_id].dimension)
            x, y, z = placement.coordinate.x, placement.coordinate.y, placement.coordinate.z

            ax_3d.bar3d(x, y, z, size.w, size.l, size.h, color=self.package_color_lookup_table[package_id], edgecolor="black", alpha=0.7)
            ax_3d.text(x + size.w / 2, y + size.l / 2, z + size.h, package_id, ha="center", fontsize=7)

        for z in (0, h):
            ax_3d.plot([0, w, w, 0, 0], [0, 0, l, l, 0], [z] * 5, color="black", alpha=0.6)

        for x in (0, w):
            for y in (0, l):
                ax_3d.plot([x, x], [y, y], [0, h], color="black", alpha=0.6)

        ax_3d.set_xlim(0, w)
        ax_3d.set_ylim(0, l)
        ax_3d.set_zlim(0, h)
        ax_3d.set_box_aspect((w, l, h))
        ax_3d.set_xlabel("X")
        ax_3d.set_ylabel("Y")
        ax_3d.set_zlabel("Z")

        
    
    def _draw_packages_outside(self, ax, problem: Problem, outside_packages_id: list[str]):
        page_size = 8
        start = [0]
        total = len(outside_packages_id)

        def draw():
            ax.clear()
            ax.axis("off")
            ax.set_title(f"Outside Packages ({total})", fontsize=10)

            if total == 0:
                ax.text(0.5, 0.5, "No outside packages", ha="center", va="center", transform=ax.transAxes)
                return

            visible = outside_packages_id[start[0]:start[0] + page_size]
            for i, package_id in enumerate(visible):
                package = problem.package_map[package_id]
                dimension = package.dimension
                y = 0.90 - i * 0.105

                ax.plot(0.05, y, marker="s", markersize=7, color=self.package_color_lookup_table[package_id], transform=ax.transAxes)

                ax.text(0.12, y, f"{package_id} | {dimension.w}x{dimension.l}x{dimension.h} | Value: {package.value}", fontsize=8, va="center", transform=ax.transAxes)

            if total > page_size:
                ax.text(0.05, 0.01, f"{start[0] + 1}-{min(start[0] + page_size, total)} of {total} (scroll to view)", fontsize=8, transform=ax.transAxes)

        def on_scroll(event):
            if event.inaxes is not ax:
                return
            step = 3 if event.button == "down" else -3
            next_start = max(0, min(total - page_size, start[0] + step))

            if next_start != start[0]:
                start[0] = next_start
                draw()
                self.fig.canvas.draw_idle()

        draw()
        if total > page_size:
            self.fig.canvas.mpl_connect("scroll_event", on_scroll)
