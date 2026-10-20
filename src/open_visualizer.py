import sys
from pathlib import Path
from visualizer.canvas import Canvas


filename = sys.argv[1]
filepath = Path(__file__).parent.parent / "output" / filename

canvas = Canvas.load(filepath)
canvas.show()