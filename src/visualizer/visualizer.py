from model.state import State
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


class Visualizer:
    def visualize(self, states : list[State]):
        def make_ax(grid=False):
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_zlabel("z")
            ax.grid(grid)
            return ax

        filled = np.array([
            [[1, 0, 1], [0, 0, 1], [0, 1, 0]],
            [[0, 1, 1], [1, 0, 0], [1, 0, 1]],
            [[1, 1, 0], [1, 1, 1], [0, 0, 0]]
        ])

        ax = make_ax()
        ax.voxels(filled, facecolors='#1f77b430', edgecolors='gray', shade=False)
        plt.show()