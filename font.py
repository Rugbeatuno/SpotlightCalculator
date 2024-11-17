import sys
from PyQt5.QtWidgets import QApplication
import pyqtgraph as pg
import numpy as np
from calc import evaluate_expression, format_equation, conversions
import time

# Initialize the application
app = QApplication(sys.argv)

# Create a window
win = pg.GraphicsLayoutWidget(
    show=True, title="Cartesian Plane with Tick Marks on Graph")
win.resize(800, 600)
win.setWindowTitle("PyQtGraph Cartesian Plane with Tick Marks")

# Add a plot with equal scaling for X and Y axes
plot = win.addPlot(title="Click to Select a Point")
plot.setAspectLocked(lock=True)  # Lock aspect ratio to 1:1
plot.showGrid(x=True, y=True)    # Enable the grid

# Set a range for the Cartesian plane
plot.setXRange(-10, 10)
plot.setYRange(-10, 10)

# Add the X and Y axes intersecting at the origin
plot.addLine(x=0, pen=pg.mkPen('k'))  # Y-axis
plot.addLine(y=0, pen=pg.mkPen('k'))  # X-axis

# Add tick marks directly on the axes
tick_length = 0.2
tick_pen = pg.mkPen('k', width=2)

# Generate tick positions and draw them on the graph
for i in range(-10, 11):  # X-axis ticks
    if i != 0:  # Skip the origin
        plot.addItem(pg.InfiniteLine(pos=(i, 0), angle=90, pen=tick_pen))
for i in range(-10, 11):  # Y-axis ticks
    if i != 0:  # Skip the origin
        plot.addItem(pg.InfiniteLine(pos=(0, i), angle=0, pen=tick_pen))


scatter = pg.ScatterPlotItem(size=10, brush='b')
plot.addItem(scatter)


def calculate_points(plot, equation):
    s = time.perf_counter()
    resolution = 1000
    x_range, _ = plot.getViewBox().viewRange()
    x_points = np.linspace(x_range[0], x_range[1], resolution)
    str_eqution = format_equation(equation, variables={'x': 'x'})
    c = {**conversions, **{'x': x_points}}
    print(c)
    result = eval(str_eqution, {'x': x_points})
    print(result)
    y_points = [evaluate_expression(equation, variables={
        'x': i
    }) for i in x_points]

    print(time.perf_counter() - s)
    curve = plot.plot(x_points, y_points, pen=pg.mkPen(
        color=(105, 174, 196), width=3), name="Sine Wave")


calculate_points(plot, '10x')


def on_mouse_click(event):
    if plot.sceneBoundingRect().contains(event.scenePos()):
        mouse_point = plot.vb.mapSceneToView(event.scenePos())
        clicked_x = mouse_point.x()
        clicked_y = mouse_point.y()

        # Find the closest data point
        idx = (np.abs(x - clicked_x)).argmin()
        closest_x = x[idx]
        closest_y = y[idx]

        # Update scatter plot with the selected point
        scatter.setData([closest_x], [closest_y])

        # Print the selected point
        print(f"Selected Point: x={closest_x}, y={closest_y}")


# Connect the click event
plot.scene().sigMouseClicked.connect(on_mouse_click)

# Run the application
if __name__ == "__main__":
    sys.exit(app.exec_())
