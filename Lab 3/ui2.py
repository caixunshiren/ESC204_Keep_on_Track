import sys
import random
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


import matplotlib.pyplot as plt
import numpy as np
import time


XLIM = [0,1]
YLIM = [0,1]
MAX_DISPLAY_SIZE = 20

start_time = time.time()


def fetch_data():
 
    with open("light.txt") as f:
        contents = f.read()
        if contents == '':
            LIGHT = []
            TIMEL = []
        else:
            LIGHT = [float(i.split(' ')[0]) for i in contents.split('\n')[:-1]]
            TIMEL = [float(i.split(' ')[1]) for i in contents.split('\n')[:-1]]
    with open("heat.txt") as f:
        contents = f.read()
        if contents == '':
            HEAT = []
            TIMEH = []
        else:
            HEAT = [float(i.split(' ')[0]) for i in contents.split('\n')[:-1]]
            TIMEH = [float(i.split(' ')[1]) for i in contents.split('\n')[:-1]]

    TIMEL = [n-TIMEL[0] for n in TIMEL]
    TIMEH = [n-TIMEH[0] for n in TIMEH]
    return (TIMEL, TIMEH,  LIGHT, HEAT)
    


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=15, height=15, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(311)
        self.axes2 = fig.add_subplot(313)
        plt.tight_layout()
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=7, height=25, dpi=100)
        self.setCentralWidget(self.canvas)

        self.update_plot()

        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        # Drop off the first y element, append a new one.
        # self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes2.cla()
        # self.canvas.axes.plot(self.xdata, self.ydata, 'r')
        TIMEL, TIMEH, LIGHT, HEAT = fetch_data()

        self.canvas.axes.plot(TIMEL, LIGHT, 'r')
        self.canvas.axes2.plot(TIMEH, HEAT, 'b')
        self.canvas.axes.set_title("Light Intensity vs. Time")
        self.canvas.axes.set_xlabel('Time (s)')
        self.canvas.axes2.set_title("Heat vs. Time")
        self.canvas.axes2.set_xlabel('Time (s)')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

def run_ui():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()