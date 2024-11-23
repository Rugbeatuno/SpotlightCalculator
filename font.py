import sys
from PyQt5.QtWidgets import QApplication
import pyqtgraph as pg
import numpy as np
from calc import evaluate_expression, format_equation, conversions
import time
import os
import math

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

def in_range(lower, upper, num):
    return lower < num < upper


computed_y = {}


def calc_resolution(lower, upper):
    return 1600
    extent = upper - lower
    if extent < 20:
        return 500

    return int(extent * 20)


def calculate_points(plot, equation):
    # the goal is to always have EX: 1000 points of the curve displayed within the window
    # the challenge is that take x^2 within (-10, 10) 1-1 window
    # after x=4, the curve is already off the page and there is no reason to continue plotting
    # lets find the x-range min and max that appear within the range
    global curves
    for c in curves:
        plot.removeItem(c)

    x_range, y_range = plot.getViewBox().viewRange()
    resolution = calc_resolution(y_range[0], y_range[1])
    print('res', resolution)

    x_range_points = np.linspace(x_range[0], x_range[1], 100)
    x_lower = x_range[0]
    x_upper = x_range[1]

    expression = format_equation(equation)
    conversions['x'] = x_range_points
    res = eval(expression, conversions)

    for index in range(1, len(res)):
        if in_range(y_range[0], y_range[1], res[index]):
            x_lower = x_range_points[index - 1]
            break
    for index in range(len(res) - 2, -1, -1):
        if in_range(y_range[0], y_range[1], res[index]):
            x_upper = x_range_points[index + 1]
            break

    x_points = np.linspace(x_lower, x_upper, resolution)
    s = time.perf_counter()
    conversions['x'] = x_points
    results = eval(expression, conversions)
    points = list(zip(x_points, results))
    print(time.perf_counter() - s)

   
    # for any points_y 2x the viewport just set it to 2x the viewport
    for index, point in enumerate(points):
        view_range = y_range[1] - y_range[0]
        if point[1] >= y_range[1] + view_range:
            points[index] = (point[0], y_range[1] + view_range)
        if point[1] <= y_range[0] - view_range:
            points[index] = (point[0], y_range[1] - view_range)

    point_segments = [[]]
    index = 0
    points = list(set(points))
    points = sorted(points, key=lambda x: x[0])
    # for i in points:
    #     print(i)
    for i in range(len(points) - 1):
        if not in_range(y_range[0], y_range[1], points[i][1]) and not in_range(y_range[0], y_range[1], points[i + 1][1]):
            point_segments[index].append(points[i])
            point_segments.append([])
            index += 1
        else:
            point_segments[index].append(points[i])

    s = time.perf_counter()
    print(f'segments: {len(point_segments)}')
    for p in point_segments:
        if len(p) <= 1:
            continue
        print(len(p))

        x_points, y_points = zip(*p)  # Unzip x and y values

        f = time.perf_counter()
        curves.append(
            plot.plot(x_points, y_points, pen=pg.mkPen(
                color=(105, 174, 196), width=2))
        )
        print(time.perf_counter() - f, 'plot')
    print(time.perf_counter() - s, 'fdsa')

def graphing_engine(plot, equation):
    global curves
    for c in curves:
        plot.removeItem(c)

    # subdivide the plot into x subdivisions (100)
    # the bounds of the subdivisions should overlap to reduce the number of computations
    # calculate the slope between the 2 endpoints, the higher the slope the more points should be calculated
    # the lower the slope, less steep the less aggressivly changing, draw fewer points, asymptotes should have a lot of points
    subdivisions = 100
    std_resolution = math.ceil(800 / subdivisions)
    x_range, y_range = plot.getViewBox().viewRange()
    x_range_points = np.linspace(x_range[0], x_range[1], subdivisions)
    conversions['x'] = x_range_points
    y_values = eval(equation, conversions)
    slopes = np.diff(y_values) / np.diff(x_range_points)
    slopes_pos = abs(slopes) + 2
    slopes_int = slopes_pos.astype(int)
    slopes_log = np.log(slopes_int)

    # Generate dynamic points within each interval
    x_dynamic = []

    s = time.perf_counter()
    for i in range(len(slopes_int)):
        # Define start and end of the interval
        x_start = x_range_points[i]
        x_end = x_range_points[i + 1]
        
        # Determine the number of points based on slopes_int
        num_points = max(int(slopes_log[i] * std_resolution), std_resolution)
        x_dynamic.extend(np.linspace(x_start, x_end, num_points))

    x_dynamic = np.array(x_dynamic)
    conversions['x'] = x_dynamic
    y_interval = eval(equation, conversions)
    
    # Filter out invalid entries (e.g., "undefined")
    valid_mask = [str(y) != "Undefined" for y in y_interval]
    x_interval_filtered = x_dynamic[valid_mask]
    y_interval_filtered = y_interval[valid_mask]

    print(time.perf_counter() - s)
    s = time.perf_counter()
    # Convert to NumPy arrays for further processing if needed
    point_segments = [[]]
    index = 0
    points = list(zip(x_interval_filtered, y_interval_filtered))
    points = sorted(points, key=lambda x: x[0])
    for i in range(len(points) - 1):
        if not in_range(y_range[0], y_range[1], points[i][1]) and not in_range(y_range[0], y_range[1], points[i + 1][1]):
            point_segments[index].append(points[i])
            point_segments.append([])
            index += 1
        else:
            point_segments[index].append(points[i])

    
    for p in point_segments:
        if len(p) <= 1:
            continue

        x_points, y_points = zip(*p)  # Unzip x and y values

        f = time.perf_counter()
        curves.append(
            plot.plot(x_points, y_points, pen=pg.mkPen(
                color=(105, 174, 196), width=2))
        )
    print(time.perf_counter() - s, 'plot')
   
   

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
    graphing_engine(plot, format_equation('cscx'))
    # calculate_points(plot, '(x+2)^3*(x-1)')
    # calculate_points(plot, 'cscx')
    # calculate_points(plot, 'x^2')
    # calculate_points(plot, '10sin(x)/x')


# Connect the click event
plot.scene().sigMouseClicked.connect(on_mouse_click)
vb.sigRangeChanged.connect(viewbox_changed)
# calculate_points(plot, 'cscx')


# Run the application
if __name__ == "__main__":
    sys.exit(app.exec_())
