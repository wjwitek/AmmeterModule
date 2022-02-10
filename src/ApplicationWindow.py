from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel
from src.utils import *

from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib import animation
from matplotlib.ticker import MaxNLocator
from pymavlink.mavutil import mavserial


class ApplicationWindow(QtWidgets.QMainWindow):
    """
    Class defining main window of application, for simplicity basically everything happens here.
    """
    def __init__(self, master: mavserial):
        """
        :param master: already connected mavserial
        """
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)
        self.master = master

        # add plot to layout
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # data
        self.currents = [5 for _ in range(120)]
        self.times = create_time_array(120)

        # add voltage and current display
        self.voltage_display = QLabel("Voltage: ")
        self.current_display = QLabel("Current: ")
        self.voltage_display.setFont(QFont('Arial, 20'))
        self.current_display.setFont(QFont('Arial, 20'))

        layout.addWidget(self.voltage_display)
        layout.addWidget(self.current_display)

        self.setup()

    def setup(self):
        """
        Declare empty plot and its parameters.
        """
        self.ax = self.fig.subplots()
        self.ax.set_aspect('auto')  # make graph fill whole matplotlib figure
        self.ax.grid(True, linestyle='-', color='0.10')

        self.plot = self.ax.plot(self.times, self.currents)
        self.plot[0].set_color('blue')

        self.ax.set_ylim(0, 10)
        self.ax.xaxis.set_major_locator(MaxNLocator(3))  # set number of visible ticks

        self.anim = animation.FuncAnimation(self.fig, self.update, interval=500)

    def update(self, i):
        """
        Get newest data from pixhawk and update plot, voltage and current.
        :param i: not used, required by FuncAnimation
        """
        voltage, current = get_data(self.master)

        # update data in arrays
        self.times.pop(0)
        self.times.append(timestamp())

        self.currents.pop(0)
        self.currents.append(current)

        # update plot
        self.ax.set_xlim([self.times[0], self.times[-1]])
        self.plot = self.ax.plot(self.times, self.currents)
        self.plot[0].set_color('blue')

        # update displayed voltage and current values
        self.current_display.setText("Current: {:.4f} A".format(current))
        self.voltage_display.setText("Voltage: {:.4f} V".format(voltage))
