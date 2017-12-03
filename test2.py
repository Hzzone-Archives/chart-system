import sys
import random

import matplotlib
matplotlib.use("Qt5Agg")

from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QScrollArea

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import utils
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from random import *
from PyQt5.QtWidgets import *





class Canvas(FigureCanvas):

    def __init__(self, parent=None):
        self.figure = Figure()
        super(Canvas, self).__init__(self.figure)

        ax = self.figure.add_subplot(111)
        data = utils.read_file("/Users/HZzone/Desktop/test.py")
        self.figure.set_size_inches(100, 100, forward=True)
        ax.plot(range(0, 20), data[:20], linewidth=1.0)
        self.draw()

class Main(QWidget):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.canvas = QScrollArea(self)
        self.canvas.setWidget(MyWindow(self))
        self.canvas.setWidgetResizable(False)
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)


app = QApplication([])
main = Main()
main.show()
app.exec_()