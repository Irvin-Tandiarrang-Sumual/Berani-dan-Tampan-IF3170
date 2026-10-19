from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection
from matplotlib.ticker import MaxNLocator

from model.problem import Problem
from model.state import State
from model.truck import Truck


class TruckVisualizer:
    """Menggambar satu truk beserta paket di dalamnya."""

    def __init__(self, problem: Problem):
        self.problem = problem

    def draw(self, ax: Axes3D, state: State, truck: Truck) -> None:
        width = truck.dimension.w
        length = truck.dimension.l
        height = truck.dimension.h

        if min(width, length, height) <= 0:
            raise ValueError("Truck dimensions must be positive")

        self._draw_floor(ax, width, length)

        for package_id in state.get_inside_package_ids(truck.id):
            package = self.problem.package_map[package_id]
            placement = state.placements[package_id]

            dimension = placement.orientation.get_oriented_dimensions(
                package.dimension
            )
            coordinate = placement.coordinate

            if coordinate is None:
                raise ValueError(f"Inside package {package_id} has no coordinate")

            ax.bar3d(
                coordinate.x,
                coordinate.y,
                coordinate.z,
                dimension.w,
                dimension.l,
                dimension.h,
                color=self.problem.package_colors[package_id],
                edgecolor="#202020",
                linewidth=0.45,
                alpha=0.85,
                shade=True
            )

            ax.text(
                coordinate.x + dimension.w / 2,
                coordinate.y + dimension.l / 2,
                coordinate.z + dimension.h,
                package_id,
                ha="center",
                va="bottom",
                fontsize=7
            )

        self._draw_boundaries(ax, width, length, height)

        ax.set_xlim(0, width)
        ax.set_ylim(0, length)
        ax.set_zlim(0, height)
        ax.set_box_aspect((width, length, height))

        ax.set_xlabel("X (width)")
        ax.set_ylabel("Y (length)")
        ax.set_zlabel("Z (height)")

        for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
            axis.set_major_locator(MaxNLocator(nbins=5, integer=True))
            axis.pane.fill = False

        ax.view_init(elev=22, azim=-60)

    @staticmethod
    def _draw_floor(ax: Axes3D, width: int, length: int) -> None:
        floor = [[
            (0, 0, 0),
            (width, 0, 0),
            (width, length, 0),
            (0, length, 0)
        ]]

        ax.add_collection3d(
            Poly3DCollection(
                floor,
                facecolors="#b6c8d5",
                alpha=0.12,
                edgecolors="none"
            )
        )

    @staticmethod
    def _draw_boundaries(
        ax: Axes3D,
        width: int,
        length: int,
        height: int
    ) -> None:
        corners = {
            "000": (0, 0, 0),
            "100": (width, 0, 0),
            "010": (0, length, 0),
            "110": (width, length, 0),
            "001": (0, 0, height),
            "101": (width, 0, height),
            "011": (0, length, height),
            "111": (width, length, height)
        }

        edges = [
            ("000", "100"),
            ("000", "010"),
            ("100", "110"),
            ("010", "110"),
            ("001", "101"),
            ("001", "011"),
            ("101", "111"),
            ("011", "111"),
            ("000", "001"),
            ("100", "101"),
            ("010", "011"),
            ("110", "111")
        ]

        segments = [
            [corners[start], corners[end]]
            for start, end in edges
        ]

        ax.add_collection3d(
            Line3DCollection(
                segments,
                colors="#3d5265",
                linewidths=1.2,
                alpha=0.85
            )
        )
