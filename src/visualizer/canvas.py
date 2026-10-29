from model.state import State
import matplotlib.pyplot as plt
import numpy as np
import pickle
from mpl_toolkits.mplot3d import Axes3D
from dataclasses import dataclass
from pathlib import Path
from model.state import PackagePlacement
from model.problem import Problem
from type.dimension import Dimension
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Button
from visualizer.visualization_data import ChartConfig, MetricConfig

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
            left=0.06, right=0.96, top=0.875, bottom=0.05,
            hspace=0.48, wspace=0.28
        )
        self.package_color_lookup_table = package_color_lookup_table
        self._truck_problem = None
        self._truck_index = 0
        self._state_views = {}
        self._truck_buttons = []
        self._truck_label = None
        self._population_buttons = []
        self._saved_states = {}
        self._algorithm_name = None
        self._charts = []
        self._metrics = []

    def write_algorithm_name(self, algorithm_name: str):
        self._algorithm_name = algorithm_name
        self.fig.suptitle(algorithm_name, fontsize=16, fontweight="bold", y=0.985)
    
    def draw_line_chart(self, chart_input : ChartInput, grid_location : GridLocation):
        ax = self.fig.add_subplot(self.gs[grid_location.row, grid_location.col])
        ax.plot(chart_input.numbers, marker = "o")
        ax.set_title(chart_input.title)
        ax.set_xlabel(chart_input.x_label)
        ax.set_ylabel(chart_input.y_label)
    
    def draw_charts(self, charts: list[ChartConfig]):
        self._charts = charts
        if len(charts) > 2:
            raise ValueError("The current layout supports at most two charts")

        for i, chart in enumerate(charts):
            location = self.gs[1, :] if len(charts) == 1 else self.gs[1, i]
            ax = self.fig.add_subplot(location)

            for series in chart.series:
                options = {"label": series.label}
                if series.color is not None:
                    options["color"] = series.color
                ax.plot(series.get_x_values(), series.values, **options)

            ax.set_title(chart.title, fontsize=10)
            ax.set_xlabel(chart.x_label)
            ax.set_ylabel(chart.y_label)
            ax.grid(alpha=0.2)

            if len(chart.series) > 1:
                ax.legend(fontsize=8)
                
    def draw_metrics(self, metrics: list[MetricConfig]):
        self._metrics = metrics
        ax = self.fig.add_subplot(self.gs[2, :])
        ax.axis("off")

        if not metrics:
            return

        columns = min(4, len(metrics))
        rows = (len(metrics) + columns - 1) // columns

        for i, metric in enumerate(metrics):
            x = (i % columns + 0.5) / columns
            y = 1 - (i // columns + 0.5) / rows
            value = f"{metric.value} {metric.unit}".strip()

            ax.text(x, y, f"{metric.label}\n{value}", ha="center", va="center", fontsize=9, linespacing=1.3, transform=ax.transAxes)

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

    def dump(self, filename: str | Path) -> None:
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "width": self.fig.get_figwidth(),
            "height": self.fig.get_figheight(),
            "row": self.row,
            "column": self.column,
            "package_colors": self.package_color_lookup_table,
            "algorithm_name": self._algorithm_name,
            "states": self._saved_states,
            "charts": self._charts,
            "metrics": self._metrics,
        }
        with output_path.open("wb") as file:
            pickle.dump(data, file)

    @staticmethod
    def load(filename: str | Path) -> "Canvas":
        with Path(filename).open("rb") as file:
            data = pickle.load(file)

        canvas = Canvas(
            data["width"],
            data["height"],
            data["row"],
            data["column"],
            data["package_colors"],
        )
        canvas.write_algorithm_name(data["algorithm_name"])
        for column_idx, state_data in sorted(data["states"].items()):
            canvas.visualize_state(
                state_data["problem"],
                state_data["state"],
                state_data["title"],
                column_idx,
                state_data["population"],
            )
        canvas.draw_charts(data["charts"])
        canvas.draw_metrics(data["metrics"])
        return canvas

    def visualize_state(self, problem: Problem, state: State,
                        title: str, column_idx: int, population: list[State] | None = None):
        if not problem.trucks:
            raise ValueError("At least one truck is required")
        if population is not None and not population:
            raise ValueError("Population cannot be empty")

        self._saved_states[column_idx] = {
            "problem": problem,
            "state": state,
            "title": title,
            "population": population,
        }
        
        if self._truck_problem is None:
            self._truck_problem = problem
            self._truck_label = self.fig.text(0.5, 0.931, "", ha="center", va="center", fontsize=10)
            if len(problem.trucks) > 1:
                ax_prev = self.fig.add_axes([0.345, 0.915, 0.045, 0.032])
                ax_next = self.fig.add_axes([0.610, 0.915, 0.045, 0.032])
                prev_button = Button(ax_prev, "<")
                next_button = Button(ax_next, ">")
                prev_button.on_clicked(lambda event: self._change_truck(-1))
                next_button.on_clicked(lambda event: self._change_truck(1))
                self._truck_buttons = [prev_button, next_button]

        has_population = population is not None
        panel = gridspec.GridSpecFromSubplotSpec(
            5 if has_population else 4, 1, subplot_spec=self.gs[0, column_idx],
            height_ratios=[0.35, 0.47, 3.15, 1.4, 0.4] if has_population else [0.35, 3.15, 1.4, 0.4],
            hspace=0.28
        )
        
        ax_title = self.fig.add_subplot(panel[0])
        ax_title.axis("off")
        ax_title.text(0.5, 0.5, title, ha="center", va="center", fontsize=12, fontweight="bold")

        truck_row = 2 if has_population else 1
        ax_truck = self.fig.add_subplot(panel[truck_row], projection="3d")
        ax_outside = self.fig.add_subplot(panel[truck_row + 1])
        ax_value = self.fig.add_subplot(panel[truck_row + 2])
        ax_value.axis("off")
        value_text = ax_value.text(0.5, 0.5, "", ha="center", va="center", fontsize=11, fontweight="bold")

        selected_index = max(range(len(population)), key=lambda i: problem.calculate_objective_value(population[i])) if has_population else None
        if has_population:
            state = population[selected_index]

        view = {
            "state": state, "population": population, "selected_index": selected_index,
            "best_index": selected_index, "ax_truck": ax_truck,
            "value_text": value_text, "population_label": None,
            "outside_ids": state.get_outside_package_ids()
        }
        self._state_views[column_idx] = view
        view["draw_outside"] = self._draw_packages_outside(ax_outside, problem, view["outside_ids"])

        if has_population:
            selector = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=panel[1], width_ratios=[1, 5, 1], wspace=0.05)
            ax_prev = self.fig.add_subplot(selector[0])
            ax_text = self.fig.add_subplot(selector[1])
            ax_next = self.fig.add_subplot(selector[2])
            ax_text.axis("off")
            view["population_label"] = ax_text.text(0.5, 0.5, "", ha="center", va="center", fontsize=9)
            prev_button = Button(ax_prev, "<")
            next_button = Button(ax_next, ">")
            prev_button.on_clicked(lambda event, col=column_idx: self._change_individual(col, -1))
            next_button.on_clicked(lambda event, col=column_idx: self._change_individual(col, 1))
            self._population_buttons.extend([prev_button, next_button])

        self._render_state(column_idx)
        
    def _change_individual(self, column_idx: int, direction: int):
        view = self._state_views[column_idx]
        if view["population"] is None:
            return
        view["selected_index"] = (view["selected_index"] + direction) % len(view["population"])
        view["state"] = view["population"][view["selected_index"]]
        self._render_state(column_idx)

    def _render_state(self, column_idx: int):
        view = self._state_views[column_idx]
        value = self._truck_problem.calculate_objective_value(view["state"])
        view["value_text"].set_text(f"State Value: {value}")
        if view["population_label"] is not None:
            idx = view["selected_index"]
            best = " (Best)" if idx == view["best_index"] else ""
            view["population_label"].set_text(f"Individual {idx + 1}/{len(view['population'])}{best}")
        view["outside_ids"][:] = view["state"].get_outside_package_ids()
        view["draw_outside"](reset=True)
        self._draw_selected_truck()

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

        def draw(reset=False):
            if reset:
                start[0] = 0
            total = len(outside_packages_id)
            start[0] = min(start[0], max(0, total - page_size))
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
            total = len(outside_packages_id)
            if total <= page_size:
                return
            step = 3 if event.button == "down" else -3
            next_start = max(0, min(total - page_size, start[0] + step))

            if next_start != start[0]:
                start[0] = next_start
                draw()
                self.fig.canvas.draw_idle()

        draw()
        self.fig.canvas.mpl_connect("scroll_event", on_scroll)
        return draw
            

    def _change_truck(self, direction: int):
        self._truck_index = (self._truck_index + direction) % len(self._truck_problem.trucks)
        self._draw_selected_truck()

    
    def _draw_selected_truck(self):
        truck = self._truck_problem.trucks[self._truck_index]
        for view in self._state_views.values():
            ax = view["ax_truck"]
            state = view["state"]
            elev, azim = ax.elev, ax.azim
            ax.clear()
            ax.set_title(str(truck.id), fontsize=9)
            self._draw_packages_in_truck(ax, truck.id, state.get_inside_package_ids(truck.id), self._truck_problem, state)
            ax.view_init(elev=elev, azim=azim)

        if self._truck_label is not None:
            self._truck_label.set_text(f"Truck {self._truck_index + 1}/{len(self._truck_problem.trucks)}: {truck.id}")
        self.fig.canvas.draw_idle()