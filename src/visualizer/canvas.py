from model.state import State
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from dataclasses import dataclass
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
                row : int, column : int):
        self.row = row
        self.column = column
        self.fig = plt.figure(width, height)
        self.gs = gridspec.GridSpec(row, column)

    def write_algorithm_name(self, algorithm_name : str):
        plt.suptitle(algorithm_name)
    
    def draw_line_chart(self, chart_input : ChartInput, grid_location : GridLocation):
        ax = self.fig.add_subplot(self.gs[grid_location.row, grid_location.col])
        ax.plot(chart_input.numbers, marker = "o")
        ax.set_title(chart_input.title)
        ax.set_xlabel(chart_input.x_label)
        ax.set_ylabel(chart_input.y_label)

    def write_sidebar_note(self, note : str):
        ax = self.fig.add_subplot(self.gs[:, self.column])
        ax.axis("off")
        ax.text(
            0.5, 0.5, note, fontsize = 12, va = "center", linespacing = 1.5
        )
        
    def show():
        plt.tight_layout()
        plt.show()

    def visualize_state(self, state : State, grid_location : GridLocation):
        # def make_ax(grid=False):
        #     fig = plt.figure()
        #     ax = fig.add_subplot(projection='3d')
        #     ax.set_xlabel("x")
        #     ax.set_ylabel("y")
        #     ax.set_zlabel("z")
        #     ax.grid(grid)
        #     return ax

        # filled = np.array([
        #     [[1, 0, 1], [0, 0, 1], [0, 1, 0]],
        #     [[0, 1, 1], [1, 0, 0], [1, 0, 1]],
        #     [[1, 1, 0], [1, 1, 1], [0, 0, 0]]
        # ])

        # ax = make_ax()
        # ax.voxels(filled, facecolors='#1f77b430', edgecolors='gray', shade=False)
        # plt.show()
        pass