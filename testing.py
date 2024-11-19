import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication

from pyqtgraph.Qt import QtGui, QtCore
import sys

# Create a QApplication instance
app = QApplication(sys.argv)


# Create a PlotWidget
pw = pg.PlotWidget()
pw.show()

# Generate data points for csc(x)
x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
y = 1 / np.sin(x)

# Plot the data
plot = pw.plot(x, y, pen='r')

# Add gridlines
pw.showGrid(x=True, y=True)

# Set labels for the axes
pw.setLabel('left', 'csc(x)')
pw.setLabel('bottom', 'x')

# Run the application
app.exec_()
