import sys
from PyQt5.QtWidgets import QApplication
import pyqtgraph as pg
import numpy as np
from calc import evaluate_expression, format_equation, conversions
import time
import os


pg.setConfigOptions(useOpenGL=True)
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
pg.setConfigOptions(antialias=True)

# Initialize the application
app = QApplication(sys.argv)

# Create a window
win = pg.GraphicsLayoutWidget(
    show=True, title="Cartesian Plane with Tick Marks on Graph")
win.resize(800, 600)
win.setWindowTitle("PyQtGraph Cartesian Plane with Tick Marks")

# Add a plot with equal scaling for X and Y axes
plot = win.addPlot(title="Click to Select a Point")
# plot.setAspectLocked(lock=True)  # Lock aspect ratio to 1:1
plot.showGrid(x=True, y=True, alpha=0.3)    # Enable the grid

# Set a range for the Cartesian plane
plot.setXRange(-10, 10)
plot.setYRange(-10, 10)

gray = (128, 128, 128)
# Add the X and Y axes intersecting at the origin
plot.addLine(x=0, pen=pg.mkPen(color=gray))  # Y-axis
plot.addLine(y=0, pen=pg.mkPen(color=gray))  # X-axis

# Add tick marks directly on the axes
tick_length = 0.2
tick_pen = pg.mkPen(color=gray, width=2)

vb = plot.getViewBox()

curves = []
# Generate tick positions and draw them on the graph
# for i in range(-10, 11):  # X-axis ticks
#     if i != 0:  # Skip the origin
#         plot.addItem(pg.InfiniteLine(pos=(i, 0), angle=90, pen=tick_pen))
# for i in range(-10, 11):  # Y-axis ticks
#     if i != 0:  # Skip the origin
#         plot.addItem(pg.InfiniteLine(pos=(0, i), angle=0, pen=tick_pen))


# scatter = pg.ScatterPlotItem(size=10, brush='b')
# plot.addItem(scatter)


def calculate_points(plot, equation):
    # the goal is to always have EX: 1000 points of the curve displayed within the window
    # the challenge is that take x^2 within (-10, 10) 1-1 window
    # after x=4, the curve is already off the page and there is no reason to continue plotting
    # lets find the x-range min and max that appear within the range
    global curves
    for c in curves:
        plot.removeItem(c)

    s = time.perf_counter()
    resolution = 1000
    x_range, y_range = plot.getViewBox().viewRange()

    x_range_points = np.linspace(x_range[0], x_range[1], 100)
    x_lower = x_range[0]
    x_upper = x_range[1]

    def find_bound(start, end):
        mid = (start + end) / 2
        if y_range[0] <= evaluate_expression(equation, variables={'x': mid}) <= y_range[1]:
            return find_bound(start, mid)
        else:
            return find_bound(mid, end)

    expression = format_equation(equation)

    p = time.perf_counter()
    for i in range(1, len(x_range_points)):
        if y_range[0] <= eval(expression.replace('x', f'({x_range_points[i]})'), conversions) <= y_range[1]:
            x_lower = x_range_points[i - 1]
            break
    for i in range(len(x_range_points) - 2, -1, -1):
        if y_range[0] <= eval(expression.replace('x', f'({x_range_points[i]})'), conversions) <= y_range[1]:
            x_upper = x_range_points[i + 1]
            break
    x_points = np.linspace(x_lower, x_upper, resolution)

    y_points = []
    for x in x_points:
        expression_with_var = expression.replace('x', f'({x})')
        y_points.append(eval(expression_with_var, conversions))

    print(time.perf_counter() - p, 'calc')
    points = np.array(list(zip(x_points, y_points)))
    for (x, y) in points:
        if y > y_range[1]:
            print(x)
    # # Condition: Points within the specified range
    # condition = (points[:, 1] > y_range[0]) & (points[:, 1] < y_range[1])

    # # Find indices where the condition is False (splitting points)
    # split_indices = np.where(~condition)[0]

    # # Adjust split_indices to include 1 index before and after
    # expanded_indices = set()
    # for idx in split_indices:
    #     expanded_indices.add(idx - 1)  # Include 1 index before
    #     expanded_indices.add(idx)     # Include the original index
    #     expanded_indices.add(idx + 1)  # Include 1 index after

    # # Ensure indices are within bounds
    # expanded_indices = sorted(
    #     idx for idx in expanded_indices if 0 <= idx < len(points))

    # # Split points into segments based on the adjusted indices
    # segments = np.split(points, expanded_indices)

    # for segment in segments:
    #     if len(segment) == 1:
    #         continue
    #     x_segment = segment[:, 0]
    #     y_segment = segment[:, 1]
    curves.append(
        plot.plot(x_points, y_points, pen=pg.mkPen(
            color=(105, 174, 196), width=3))
    )


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


def viewbox_changed():
    calculate_points(plot, 'cscx')
    # calculate_points(plot, 'x^2')
    # calculate_points(plot, '10sin(x)/x')


# Connect the click event
plot.scene().sigMouseClicked.connect(on_mouse_click)
vb.sigRangeChanged.connect(viewbox_changed)

# Run the application
if __name__ == "__main__":
    sys.exit(app.exec_())
