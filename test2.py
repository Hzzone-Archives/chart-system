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


class Canvas(FigureCanvas):

    def __init__(self, parent=None):
        self.figure = Figure()
        super(Canvas, self).__init__(self.figure)

        ax = self.figure.add_subplot(1, 1, 1)
        data = utils.read_file("/Users/HZzone/Desktop/test.py")
        # self.figure.set_size_inches(18.5, 10.5, forward=True)
        ax.plot(range(0, len(data)), data, linewidth=2.0)
        self.draw()

    def add_subplot(self, data=[]):
        rows = len(self.figure.axes) + 1
        for index, axes in enumerate(self.figure.axes, start=1):
            axes.change_geometry(rows, 1, index)

        ax = self.figure.add_subplot(rows, 1, index+1)
        ax.plot(data)
        self.figure.set_figheight(self.figure.get_figheight()*1.25)
        self.draw()

class Main(QWidget):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.canvas = QScrollArea(self)
        self.canvas.setWidget(Canvas(self))
        self.canvas.setWidgetResizable(False)
        # print(self.size())
        # print(dir(self.size()))
        # new_size = QtCore.QSize(200, self.canvas.size().height())
        # self.setBaseSize((200, self.canvas.size()))
        # self.setBaseSize(new_size)

        # for x in range(1):
        #     self.canvas.widget().add_subplot()
        #     self.canvas.widget().adjustSize()


        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)


app = QApplication([])
main = Main()
main.show()
app.exec_()